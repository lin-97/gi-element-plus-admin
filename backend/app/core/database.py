from collections.abc import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.config.setting import settings
from app.core.base_model import MappedBase
from app.core.exceptions import CustomException
from app.core.logger import log


def create_engine_and_session(db_url: str = settings.DB_URI) -> tuple[Engine, sessionmaker]:
    engine = create_engine(
        url=db_url,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=settings.POOL_PRE_PING,
        pool_recycle=settings.POOL_RECYCLE,
    )
    return engine, sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_async_engine_and_session(
    db_url: str = settings.ASYNC_DB_URI,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    kwargs = {
        "url": db_url,
        "echo": settings.DATABASE_ECHO,
        "pool_pre_ping": settings.POOL_PRE_PING,
        "future": True,
        "pool_recycle": settings.POOL_RECYCLE,
    }
    if settings.DATABASE_TYPE != "sqlite":
        kwargs.update(
            pool_size=settings.POOL_SIZE,
            max_overflow=settings.MAX_OVERFLOW,
            pool_timeout=settings.POOL_TIMEOUT,
        )
    async_engine = create_async_engine(**kwargs)
    async_session = async_sessionmaker(
        bind=async_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return async_engine, async_session


engine, db_session = create_engine_and_session()
async_engine, async_db_session = create_async_engine_and_session()


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    async with async_db_session() as session:
        async with session.begin():
            yield session


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(MappedBase.metadata.create_all)


async def drop_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(MappedBase.metadata.drop_all)


async def redis_connect() -> Redis | None:
    if not settings.REDIS_ENABLE:
        return None
    try:
        redis = Redis.from_url(
            settings.REDIS_URI,
            encoding="utf-8",
            decode_responses=True,
            health_check_interval=20,
        )
        await redis.ping()
        return redis
    except Exception as exc:
        log.error(f"Redis连接失败: {exc}")
        raise CustomException(msg="Redis连接失败，请检查配置或关闭 REDIS_ENABLE")
