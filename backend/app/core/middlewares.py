import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.config.setting import settings
from app.core.logger import log


class CustomCORSMiddleware(CORSMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_methods=settings.ALLOW_METHODS,
            allow_headers=settings.ALLOW_HEADERS,
            allow_credentials=settings.ALLOW_CREDENTIALS,
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        log.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        process_time = round(time.time() - start_time, 5)
        response.headers["X-Process-Time"] = str(process_time)
        log.info(f"{request.method} {request.url.path} {response.status_code} {process_time}s")
        return response


class CustomGZipMiddleware(GZipMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            minimum_size=settings.GZIP_MIN_SIZE,
            compresslevel=settings.GZIP_COMPRESS_LEVEL,
        )
