import asyncio
import os
from typing import Annotated

import typer
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from app.common.enums import EnvironmentEnum

cli = typer.Typer()
alembic_cfg = Config("alembic.ini")


def prepare_environment(env: EnvironmentEnum) -> None:
    os.environ["ENVIRONMENT"] = env.value
    from app.config.setting import get_settings

    get_settings.cache_clear()


def create_app() -> FastAPI:
    from app.config.setting import settings
    from app.core.logger import setup_logging
    from app.scripts.init_app import (
        lifespan,
        register_exceptions,
        register_files,
        register_middlewares,
        register_routers,
    )

    setup_logging(settings.LOGGER_LEVEL)
    app = FastAPI(**settings.FASTAPI_CONFIG, lifespan=lifespan)
    register_exceptions(app)
    register_middlewares(app)
    register_routers(app)
    register_files(app)
    return app


@cli.command(name="run")
def run(
    env: Annotated[
        EnvironmentEnum,
        typer.Option("--env", help="运行环境(dev/test/prod)"),
    ] = EnvironmentEnum.DEV,
) -> None:
    prepare_environment(env)
    from app.config.setting import get_settings
    from app.core.logger import setup_logging
    from app.utils.banner import print_banner

    settings = get_settings()
    setup_logging(settings.LOGGER_LEVEL)
    print_banner(env.value)
    uvicorn.run(
        "main:create_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=env == EnvironmentEnum.DEV,
        factory=True,
    )


@cli.command(name="revision")
def revision(
    env: Annotated[
        EnvironmentEnum,
        typer.Option("--env", help="运行环境(dev/test/prod)"),
    ] = EnvironmentEnum.DEV,
) -> None:
    prepare_environment(env)
    from app.scripts.initialize import ensure_database_exists

    ensure_database_exists()
    command.revision(alembic_cfg, autogenerate=True, message="迁移脚本")


@cli.command(name="upgrade")
def upgrade(
    env: Annotated[
        EnvironmentEnum,
        typer.Option("--env", help="运行环境(dev/test/prod)"),
    ] = EnvironmentEnum.DEV,
) -> None:
    prepare_environment(env)
    from app.scripts.initialize import run_alembic_upgrade

    asyncio.run(run_alembic_upgrade())


@cli.command(name="init-data")
def init_data(
    env: Annotated[
        EnvironmentEnum,
        typer.Option("--env", help="运行环境(dev/test/prod)"),
    ] = EnvironmentEnum.DEV,
) -> None:
    prepare_environment(env)
    from app.scripts.initialize import InitializeData

    asyncio.run(InitializeData().init_data())


if __name__ == "__main__":
    cli()
