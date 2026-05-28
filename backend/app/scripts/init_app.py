from collections.abc import AsyncGenerator
from typing import Any

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.config.setting import settings
from app.core.docs import get_custom_ui_html
from app.core.database import redis_connect
from app.core.exceptions import handle_exception
from app.core.logger import log
from app.core.middlewares import CustomCORSMiddleware, CustomGZipMiddleware, RequestLogMiddleware

from .initialize import InitializeData, run_alembic_upgrade


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    try:
        await run_alembic_upgrade()
        await InitializeData().init_data()
        app.state.redis = await redis_connect()
        log.info("应用初始化完成")
        from app.utils.console import console_run

        console_run(database_ready=True, redis_ready=app.state.redis is not None)
    except Exception as exc:
        log.error(f"应用初始化失败: {exc}")
        raise
    yield
    redis = getattr(app.state, "redis", None)
    if redis:
        await redis.close()


def register_exceptions(app: FastAPI) -> None:
    handle_exception(app)


def register_middlewares(app: FastAPI) -> None:
    if settings.GZIP_ENABLE:
        app.add_middleware(CustomGZipMiddleware)
    app.add_middleware(RequestLogMiddleware)
    if settings.CORS_ORIGIN_ENABLE:
        app.add_middleware(CustomCORSMiddleware)


def register_routers(app: FastAPI) -> None:
    from app.api.v1.router import api_v1_router
    from app.core.discover import get_dynamic_router

    app.include_router(api_v1_router)
    app.include_router(get_dynamic_router(), prefix="/api/v1/plugin")


def register_files(app: FastAPI) -> None:
    if settings.STATIC_ENABLE:
        settings.STATIC_ROOT.mkdir(parents=True, exist_ok=True)
        settings.UPLOAD_FILE_PATH.mkdir(parents=True, exist_ok=True)
        app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_ROOT), name="static")


def reset_api_docs(app: FastAPI) -> None:
    @app.get(str(app.swagger_ui_oauth2_redirect_url), include_in_schema=False)
    async def swagger_ui_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=str(app.openapi_url),
            title=f"{app.title} - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.SWAGGER_JS_URL,
            swagger_css_url=settings.SWAGGER_CSS_URL,
            swagger_favicon_url=settings.FAVICON_URL,
        )

    @app.get(settings.REDOC_URL, include_in_schema=False)
    async def custom_redoc_html() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=str(app.openapi_url),
            title=f"{app.title} - ReDoc",
            redoc_js_url=settings.REDOC_JS_URL,
            redoc_favicon_url=settings.FAVICON_URL,
        )

    @app.get(settings.LJDOC_URL, include_in_schema=False)
    async def custom_ljdoc_html() -> HTMLResponse:
        return get_custom_ui_html(
            openapi_url=str(app.openapi_url),
            title=f"{app.title} - LangJin UI",
            swagger_js_url=settings.CUSTOM_JS_URL,
            swagger_css_url=settings.CUSTOM_CSS_URL,
            swagger_favicon_url=settings.FAVICON_URL,
        )
