#!/usr/bin/env bash
# 后端代码更新脚本（日常发版时在服务器执行）
set -euo pipefail

APP_NAME="gi-admin-api"
APP_DIR="/www/wwwroot/gi-admin-api"

echo ">>> 拉取最新代码"
git -C "$APP_DIR" pull --ff-only origin main

echo ">>> 更新依赖"
cd "$APP_DIR/backend"
uv sync --frozen --no-dev

echo ">>> 执行数据库迁移"
uv run main.py upgrade --env=prod

echo ">>> 重启服务"
systemctl restart "${APP_NAME}"

echo ">>> 完成"
