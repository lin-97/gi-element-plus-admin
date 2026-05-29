import asyncio
import concurrent.futures
from logging.config import fileConfig

from alembic import context
from sqlalchemy import MetaData, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.path_conf import ALEMBIC_VERSION_DIR
from app.config.setting import settings
from app.core.base_model import MappedBase
from app.utils.import_util import ImportUtil

# 确保 alembic 版本目录存在
ALEMBIC_VERSION_DIR.mkdir(parents=True, exist_ok=True)

# 清除 MappedBase.metadata 中的表定义，避免重复注册
if hasattr(MappedBase, "metadata") and MappedBase.metadata.tables:
    print(f"🧹 清除已存在的表定义，当前有 {len(MappedBase.metadata.tables)} 个表")
    MappedBase.metadata = MetaData()
    print("✅️ 已重置 metadata")

# 自动查找所有模型
print("🔍 开始查找模型...")
found_models = ImportUtil.find_models(MappedBase)
print(f"📊 找到 {len(found_models)} 个有效模型")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config

# Interpret the config file for Python logging.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

target_metadata = MappedBase.metadata

alembic_config.set_main_option("sqlalchemy.url", settings.ASYNC_DB_URI)


def _run_async(coro) -> None:
    """在同步上下文中执行协程；若已有事件循环则在新线程中运行。"""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(coro)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(asyncio.run, coro).result()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = alembic_config.get_main_option("sqlalchemy.url")
    if url is None:
        raise ValueError("数据库 URL 未正确配置，请检查环境配置文件")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = alembic_config.get_main_option("sqlalchemy.url")
    if url is None:
        raise ValueError("数据库 URL 未正确配置，请检查环境配置文件")

    connectable = create_async_engine(url, poolclass=pool.NullPool)

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()

    def do_run_migrations(connection: Connection) -> None:
        def process_revision_directives(context, revision, directives) -> None:
            script = directives[0]
            all_empty = all(ops.is_empty() for ops in script.upgrade_ops_list)
            if all_empty:
                directives[:] = []
                print("❎️ 未检测到模型变更，不生成迁移文件")
            else:
                print("✅️ 检测到模型变更，生成迁移文件")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            transaction_per_migration=True,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()

    _run_async(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
