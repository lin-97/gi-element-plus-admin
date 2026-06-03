# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/pyproject.toml backend/uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project


FROM python:3.12-slim AS runtime

ENV TZ=Asia/Shanghai \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=prod \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN useradd --create-home --uid 1001 --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/logs /app/static/upload /app/env \
    && chown -R appuser:appuser /app/logs /app/static/upload /app/env

COPY --from=builder --chown=appuser:appuser /build/.venv /app/.venv
COPY --chown=appuser:appuser backend/app ./app
COPY --chown=appuser:appuser backend/main.py backend/alembic.ini backend/banner.txt ./
COPY --chown=appuser:appuser backend/static ./static

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3).read()" || exit 1

CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
