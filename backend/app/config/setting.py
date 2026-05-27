import os
from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.enums import EnvironmentEnum
from app.config.path_conf import BASE_DIR, ENV_DIR, STATIC_DIR


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_DIR / f".env.{os.getenv('ENVIRONMENT', 'dev')}",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    TITLE: str = "GI Element Plus Admin API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "GI Element Plus Admin backend service"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    ROOT_PATH: str = "/api/v1"

    LOGGER_LEVEL: str = "INFO"

    CORS_ORIGIN_ENABLE: bool = True
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    CORS_EXPOSE_HEADERS: list[str] = ["X-Process-Time", "X-Request-ID"]
    GZIP_ENABLE: bool = True
    GZIP_MIN_SIZE: int = 1000
    GZIP_COMPRESS_LEVEL: int = 6

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    TOKEN_TYPE: str = "bearer"
    TOKEN_SLIDING_EXPIRE: bool = True
    TOKEN_REQUEST_PATH_EXCLUDE: list[str] = [
        "/api/v1/auth/login",
        "/api/v1/auth/captcha/get",
        "/api/v1/health",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    SQL_DB_ENABLE: bool = True
    DATABASE_TYPE: Literal["mysql", "postgres", "sqlite"] = "mysql"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "123456"
    DATABASE_NAME: str = "gi_admin"
    MYSQL_HOST: str | None = None
    MYSQL_PORT: int | None = None
    MYSQL_USER: str | None = None
    MYSQL_PASSWORD: str | None = None
    MYSQL_DATABASE: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DATABASE: str | None = None
    DATABASE_ECHO: bool = False
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 20
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    POOL_PRE_PING: bool = True

    REDIS_ENABLE: bool = True
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB_NAME: int = 1
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    CAPTCHA_ENABLE: bool = True
    CAPTCHA_EXPIRE_SECONDS: int = 60
    REQUEST_LIMITER_ENABLE: bool = True
    REQUEST_LIMITER_REDIS_PREFIX: str = "gi-admin:request-limiter:"

    OPERATION_LOG_RECORD: bool = True
    OPERATION_RECORD_METHOD: list[str] = ["POST", "PUT", "PATCH", "DELETE"]
    IGNORE_OPERATION_FUNCTION: list[str] = ["login", "get_captcha"]

    STATIC_ENABLE: bool = True
    STATIC_URL: str = "/static"
    STATIC_DIR_NAME: str = "static"
    STATIC_ROOT: Path = STATIC_DIR
    UPLOAD_FILE_PATH: Path = STATIC_DIR / "upload"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: list[str] = [
        ".gif",
        ".jpg",
        ".jpeg",
        ".png",
        ".ico",
        ".svg",
        ".txt",
        ".pdf",
        ".xls",
        ".xlsx",
    ]

    @property
    def FASTAPI_CONFIG(self) -> dict:
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "redoc_url": self.REDOC_URL,
            "root_path": "",
        }

    @property
    def ASYNC_DB_URI(self) -> str:
        if self.DATABASE_TYPE == "mysql":
            host = self.MYSQL_HOST or self.DATABASE_HOST
            port = self.MYSQL_PORT or self.DATABASE_PORT
            user = self.MYSQL_USER or self.DATABASE_USER
            password = self.MYSQL_PASSWORD or self.DATABASE_PASSWORD
            database = self.MYSQL_DATABASE or self.DATABASE_NAME
            return (
                f"mysql+asyncmy://{user}:{quote_plus(password)}"
                f"@{host}:{port}/{database}?charset=utf8mb4"
            )
        if self.DATABASE_TYPE == "postgres":
            host = self.POSTGRES_HOST or self.DATABASE_HOST
            port = self.POSTGRES_PORT or self.DATABASE_PORT
            user = self.POSTGRES_USER or self.DATABASE_USER
            password = self.POSTGRES_PASSWORD or self.DATABASE_PASSWORD
            database = self.POSTGRES_DATABASE or self.DATABASE_NAME
            return (
                f"postgresql+asyncpg://{user}:{quote_plus(password)}"
                f"@{host}:{port}/{database}"
            )
        return f"sqlite+aiosqlite:///{BASE_DIR / f'{self.DATABASE_NAME}.db'}"

    @property
    def DB_URI(self) -> str:
        if self.DATABASE_TYPE == "mysql":
            host = self.MYSQL_HOST or self.DATABASE_HOST
            port = self.MYSQL_PORT or self.DATABASE_PORT
            user = self.MYSQL_USER or self.DATABASE_USER
            password = self.MYSQL_PASSWORD or self.DATABASE_PASSWORD
            database = self.MYSQL_DATABASE or self.DATABASE_NAME
            return (
                f"mysql+pymysql://{user}:{quote_plus(password)}"
                f"@{host}:{port}/{database}?charset=utf8mb4"
            )
        if self.DATABASE_TYPE == "postgres":
            host = self.POSTGRES_HOST or self.DATABASE_HOST
            port = self.POSTGRES_PORT or self.DATABASE_PORT
            user = self.POSTGRES_USER or self.DATABASE_USER
            password = self.POSTGRES_PASSWORD or self.DATABASE_PASSWORD
            database = self.POSTGRES_DATABASE or self.DATABASE_NAME
            return (
                f"postgresql+psycopg://{user}:{quote_plus(password)}"
                f"@{host}:{port}/{database}"
            )
        return f"sqlite:///{BASE_DIR / f'{self.DATABASE_NAME}.db'}"

    @property
    def REDIS_URI(self) -> str:
        auth = ""
        if self.REDIS_USER or self.REDIS_PASSWORD:
            auth = f"{self.REDIS_USER}:{quote_plus(self.REDIS_PASSWORD)}@"
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
