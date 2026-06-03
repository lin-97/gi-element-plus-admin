import asyncio
import json

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, func, inspect, select, text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.params.model import ParamsModel
from app.api.v1.module_system.position.model import PositionModel
from app.api.v1.module_system.role.model import RoleDeptsModel, RoleMenusModel, RoleModel
from app.api.v1.module_system.user.model import UserModel, UserPositionsModel, UserRolesModel
from app.config.path_conf import ALEMBIC_VERSION_DIR, BASE_DIR, SCRIPT_DATA_DIR
from app.config.setting import settings
from app.core.base_model import MappedBase
from app.core.database import async_db_session, async_engine, create_tables
from app.core.logger import log
from app.utils.import_util import ImportUtil
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


def _has_alembic_revisions() -> bool:
    if not ALEMBIC_VERSION_DIR.exists():
        return False
    return any(ALEMBIC_VERSION_DIR.glob("*.py"))


def _ensure_orm_metadata() -> None:
    if not MappedBase.metadata.tables:
        ImportUtil.find_models(MappedBase)


async def _core_table_exists() -> bool:
    async with async_engine.connect() as conn:

        def check(sync_conn) -> bool:
            return inspect(sync_conn).has_table(DeptModel.__tablename__)

        return await conn.run_sync(check)


async def run_alembic_upgrade() -> None:
    ensure_database_exists()
    cfg = Config(str(BASE_DIR / "alembic.ini"))

    if _has_alembic_revisions():
        await asyncio.to_thread(command.upgrade, cfg, "head")
    else:
        log.warning("未发现 Alembic 迁移脚本，跳过 upgrade")

    if not await _core_table_exists():
        log.warning("核心表不存在，使用 metadata.create_all 建表")
        _ensure_orm_metadata()
        await create_tables()
        log.info("表结构初始化完成")

    await apply_schema_patches()


async def apply_schema_patches() -> None:
    """无 Alembic 迁移时的增量结构补丁（幂等）"""
    if not settings.SQL_DB_ENABLE or not await _core_table_exists():
        return

    async with async_engine.begin() as conn:

        def patch(sync_conn) -> None:
            if not inspect(sync_conn).has_table(MenuModel.__tablename__):
                return
            cols = inspect(sync_conn).get_columns(MenuModel.__tablename__)
            icon_col = next((c for c in cols if c["name"] == "icon"), None)
            if not icon_col:
                return

            db_type = settings.DATABASE_TYPE
            col_type = icon_col["type"]
            type_name = type(col_type).__name__.upper()

            if db_type == "mysql":
                length = getattr(col_type, "length", None)
                if type_name == "VARCHAR" and length is not None and length <= 255:
                    sync_conn.execute(
                        text(
                            "ALTER TABLE sys_menu MODIFY COLUMN icon TEXT "
                            "COMMENT '菜单图标（Element Plus 图标名或 SVG 字符串）'"
                        )
                    )
                    log.info("已扩展 sys_menu.icon 列为 TEXT")
            elif db_type == "postgres":
                if type_name in {"VARCHAR", "CHARACTER VARYING"}:
                    sync_conn.execute(text("ALTER TABLE sys_menu ALTER COLUMN icon TYPE TEXT"))
                    log.info("已扩展 sys_menu.icon 列为 TEXT")

        await conn.run_sync(patch)


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
