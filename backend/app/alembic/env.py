from logging.config import fileConfig

from alembic import context

# Import models for metadata registration.
from app.api.v1.module_system.dept import model as dept_model  # noqa: F401
from app.api.v1.module_system.dict import model as dict_model  # noqa: F401
from app.api.v1.module_system.log import model as log_model  # noqa: F401
from app.api.v1.module_system.menu import model as menu_model  # noqa: F401
from app.api.v1.module_system.params import model as params_model  # noqa: F401
from app.api.v1.module_system.position import model as position_model  # noqa: F401
from app.api.v1.module_system.role import model as role_model  # noqa: F401
from app.api.v1.module_system.user import model as user_model  # noqa: F401
from app.config.setting import settings
from app.core.base_model import MappedBase
from app.plugin.module_student.student import model as student_model  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.DB_URI)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = MappedBase.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DB_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine

    connectable = create_engine(settings.DB_URI, pool_pre_ping=True)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
