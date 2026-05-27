import json

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.params.model import ParamsModel
from app.api.v1.module_system.position.model import PositionModel
from app.api.v1.module_system.role.model import RoleDeptsModel, RoleMenusModel, RoleModel
from app.api.v1.module_system.user.model import UserModel, UserPositionsModel, UserRolesModel
from app.config.path_conf import BASE_DIR, SCRIPT_DATA_DIR
from app.config.setting import settings
from app.core.database import async_db_session
from app.core.logger import log
from app.core.security import get_password_hash
from app.plugin.module_student.student.model import StudentModel


def ensure_database_exists() -> None:
    if not settings.SQL_DB_ENABLE or settings.DATABASE_TYPE == "sqlite":
        return
    if settings.DATABASE_TYPE == "mysql":
        _ensure_mysql_database()
    elif settings.DATABASE_TYPE == "postgres":
        _ensure_postgres_database()


def _ensure_mysql_database() -> None:
    database = settings.MYSQL_DATABASE or settings.DATABASE_NAME
    url = URL.create(
        "mysql+pymysql",
        username=settings.MYSQL_USER or settings.DATABASE_USER,
        password=settings.MYSQL_PASSWORD or settings.DATABASE_PASSWORD,
        host=settings.MYSQL_HOST or settings.DATABASE_HOST,
        port=settings.MYSQL_PORT or settings.DATABASE_PORT,
        query={"charset": "utf8mb4"},
    )
    engine = create_engine(url, isolation_level="AUTOCOMMIT", pool_pre_ping=True)
    escaped_database = database.replace("`", "``")
    try:
        with engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{escaped_database}` "
                    "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
        log.info(f"数据库已就绪: {database}")
    finally:
        engine.dispose()


def _ensure_postgres_database() -> None:
    database = settings.POSTGRES_DATABASE or settings.DATABASE_NAME
    url = URL.create(
        "postgresql+psycopg",
        username=settings.POSTGRES_USER or settings.DATABASE_USER,
        password=settings.POSTGRES_PASSWORD or settings.DATABASE_PASSWORD,
        host=settings.POSTGRES_HOST or settings.DATABASE_HOST,
        port=settings.POSTGRES_PORT or settings.DATABASE_PORT,
        database="postgres",
    )
    engine = create_engine(url, isolation_level="AUTOCOMMIT", pool_pre_ping=True)
    escaped_database = database.replace('"', '""')
    try:
        with engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :database"),
                {"database": database},
            ).scalar()
            if not exists:
                conn.execute(text(f'CREATE DATABASE "{escaped_database}"'))
        log.info(f"数据库已就绪: {database}")
    finally:
        engine.dispose()


async def run_alembic_upgrade() -> None:
    ensure_database_exists()
    cfg = Config(str(BASE_DIR / "alembic.ini"))
    command.upgrade(cfg, "head")


class InitializeData:
    def __init__(self) -> None:
        self.models = [
            DeptModel,
            PositionModel,
            MenuModel,
            RoleModel,
            UserModel,
            UserRolesModel,
            UserPositionsModel,
            RoleMenusModel,
            RoleDeptsModel,
            DictTypeModel,
            DictDataModel,
            ParamsModel,
            StudentModel,
        ]

    async def init_data(self) -> None:
        ensure_database_exists()
        async with async_db_session() as session:
            async with session.begin():
                for model in self.models:
                    await self._init_model(session, model)

    async def _init_model(self, db: AsyncSession, model) -> None:
        count = (await db.execute(select(func.count()).select_from(model))).scalar() or 0
        if count > 0:
            return
        data = self._read_json(model.__tablename__)
        if not data:
            return
        objs = []
        for item in data:
            row = dict(item)
            if model is UserModel and "password" in row:
                row["password"] = get_password_hash(row["password"])
            objs.append(model(**row))
        db.add_all(objs)
        await db.flush()
        log.info(f"初始化 {model.__tablename__}: {len(objs)} 条")

    def _read_json(self, name: str) -> list[dict]:
        path = SCRIPT_DATA_DIR / f"{name}.json"
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))
