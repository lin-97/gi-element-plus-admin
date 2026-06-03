#!/usr/bin/env bash
# GI Element Plus Admin 后端一键部署脚本（在宝塔面板「终端」中执行）
set -euo pipefail

APP_NAME="gi-admin-api"
APP_DIR="/www/wwwroot/gi-admin-api"
REPO_URL="https://github.com/lin-97/gi-element-plus-admin.git"
API_PORT=29891
SERVICE_USER="www"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

require_root() {
  [[ $EUID -eq 0 ]] || error "请使用 root 用户在宝塔终端中执行"
}

install_deps() {
  info "检查系统依赖..."
  if command -v apt-get &>/dev/null; then
    apt-get update -qq
    apt-get install -y -qq git curl nginx
  elif command -v yum &>/dev/null; then
    yum install -y git curl nginx
  fi

  if ! command -v uv &>/dev/null; then
    info "安装 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
  fi
}

clone_or_update() {
  if [[ -d "$APP_DIR/.git" ]]; then
    info "更新代码..."
    git -C "$APP_DIR" pull --ff-only origin main
  else
    info "克隆仓库到 $APP_DIR ..."
    mkdir -p "$(dirname "$APP_DIR")"
    git clone --depth 1 "$REPO_URL" "$APP_DIR"
  fi
}

setup_env() {
  local env_file="$APP_DIR/backend/env/.env.prod"
  if [[ ! -f "$env_file" ]]; then
    mkdir -p "$APP_DIR/backend/env"
    cp "$APP_DIR/deploy/backend/.env.prod.example" "$env_file"
    warn "已创建 $env_file，请编辑数据库/Redis/SECRET_KEY 后重新运行本脚本"
    exit 0
  fi
}

install_python() {
  info "安装 Python 依赖..."
  cd "$APP_DIR/backend"
  uv sync --frozen --no-dev
}

init_database() {
  info "初始化数据库..."
  cd "$APP_DIR/backend"
  uv run main.py upgrade --env=prod
  uv run main.py init-data --env=prod || warn "init-data 可能已执行过，跳过"
}

install_systemd() {
  info "配置 systemd 服务..."
  cat > "/etc/systemd/system/${APP_NAME}.service" <<EOF
[Unit]
Description=GI Element Plus Admin API
After=network.target mysql.service redis.service

[Service]
Type=simple
User=${SERVICE_USER}
Group=${SERVICE_USER}
WorkingDirectory=${APP_DIR}/backend
Environment=ENVIRONMENT=prod
Environment=PATH=${APP_DIR}/backend/.venv/bin:/usr/local/bin:/usr/bin
ExecStart=${APP_DIR}/backend/.venv/bin/uvicorn main:create_app --host 127.0.0.1 --port 8000 --factory
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

  chown -R "${SERVICE_USER}:${SERVICE_USER}" "$APP_DIR"
  systemctl daemon-reload
  systemctl enable "${APP_NAME}"
  systemctl restart "${APP_NAME}"
}

install_nginx() {
  info "配置 Nginx 反向代理（端口 ${API_PORT}）..."
  cat > "/etc/nginx/conf.d/${APP_NAME}.conf" <<EOF
server {
    listen ${API_PORT};
    server_name _;

    client_max_body_size 20m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300s;
    }
}
EOF

  nginx -t
  systemctl reload nginx || systemctl restart nginx
}

health_check() {
  sleep 2
  if curl -sf "http://127.0.0.1:8000/api/v1/health" >/dev/null; then
    info "后端健康检查通过"
  else
    warn "健康检查未通过，请查看日志: journalctl -u ${APP_NAME} -n 50"
  fi
  if curl -sf "http://127.0.0.1:${API_PORT}/api/v1/health" >/dev/null; then
    info "Nginx 代理检查通过 (端口 ${API_PORT})"
  else
    warn "Nginx 代理检查未通过，请确认安全组已放行 ${API_PORT} 端口"
  fi
}

main() {
  require_root
  install_deps
  clone_or_update
  setup_env
  install_python
  init_database
  install_systemd
  install_nginx
  health_check
  info "部署完成！API 地址: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_IP'):${API_PORT}/api/v1"
}

main "$@"
