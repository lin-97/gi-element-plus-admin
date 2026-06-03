#!/usr/bin/env bash
set -euo pipefail

# 用法:
#   bash docker/backend/request_letsencrypt.sh -d a.app.yizhuanyiyuan.cn -e coderxslee@qq.com
#
# 脚本流程:
# 1) 检查并安装 acme.sh
# 2) 临时停止 Docker Nginx 服务，释放 80 端口给 standalone 校验
# 3) 使用 Let's Encrypt 签发证书
# 4) 将证书安装到 docker/nginx/ssl/server.pem 和 server.key
# 5) 异常退出时自动恢复原本运行中的 Nginx 服务

DOMAIN=""
EMAIL=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMPOSE_FILE=""
SSL_DIR="${PROJECT_ROOT}/docker/nginx/ssl"
ACME_HOME="${HOME}/.acme.sh"
ACME_BIN="${ACME_HOME}/acme.sh"
NGINX_WAS_RUNNING=0

for file in \
  "${PROJECT_ROOT}/docker-compose.yaml" \
  "${PROJECT_ROOT}/docker-compose.yml" \
  "${PROJECT_ROOT}/docker/docker-compose.yaml" \
  "${PROJECT_ROOT}/docker/docker-compose.backend-api.yaml"
do
  if [[ -f "${file}" ]]; then
    COMPOSE_FILE="${file}"
    break
  fi
done

print_help() {
  cat <<'EOF'
用法:
  bash docker/backend/request_letsencrypt.sh -d <domain> -e <email>

参数:
  -d  域名，例如 aizhongyi.abrdns.com
  -e  证书通知邮箱（Let's Encrypt 推荐填写）

示例:
  bash docker/backend-api/request_letsencrypt.sh -d aizhongyi.abrdns.com -e admin@example.com
EOF
}

while getopts ":d:e:h" opt; do
  case "${opt}" in
    d) DOMAIN="${OPTARG}" ;;
    e) EMAIL="${OPTARG}" ;;
    h)
      print_help
      exit 0
      ;;
    *)
      print_help
      exit 1
      ;;
  esac
done

if [[ -z "${DOMAIN}" || -z "${EMAIL}" ]]; then
  echo "[ERROR] 参数不完整。"
  print_help
  exit 1
fi

if [[ -z "${COMPOSE_FILE}" ]]; then
  echo "[ERROR] 未找到 docker-compose.yaml、docker-compose.yml 或 docker/docker-compose.backend-api.yaml。"
  exit 1
fi

compose() {
  docker compose -f "${COMPOSE_FILE}" "$@"
}

show_port_80_owner() {
  if command -v ss >/dev/null 2>&1; then
    ss -ltnp 'sport = :80' || true
  elif command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:80 -sTCP:LISTEN || true
  elif command -v netstat >/dev/null 2>&1; then
    netstat -ltnp 2>/dev/null | grep ':80 ' || true
  else
    echo "[WARN] 未找到 ss/lsof/netstat，无法显示 80 端口占用进程。"
  fi
}

is_port_80_free() {
  if command -v ss >/dev/null 2>&1; then
    ! ss -ltn 'sport = :80' | grep -q ':80'
  elif command -v lsof >/dev/null 2>&1; then
    ! lsof -nP -iTCP:80 -sTCP:LISTEN >/dev/null 2>&1
  elif command -v netstat >/dev/null 2>&1; then
    ! netstat -ltn 2>/dev/null | grep -q ':80 '
  else
    return 0
  fi
}

wait_for_port_80_free() {
  local retries=20

  for _ in $(seq 1 "${retries}"); do
    if is_port_80_free; then
      return 0
    fi
    sleep 1
  done

  echo "[ERROR] 80 端口仍被占用，standalone 模式无法签发证书。当前占用:"
  show_port_80_owner
  echo "[ERROR] 请先停止占用 80 端口的服务，再重新执行本脚本。"
  return 1
}

remember_nginx_state() {
  local container_id
  container_id="$(compose ps -q nginx 2>/dev/null || true)"

  if [[ -n "${container_id}" ]] && docker inspect -f '{{.State.Running}}' "${container_id}" 2>/dev/null | grep -qx "true"; then
    NGINX_WAS_RUNNING=1
  elif docker ps --filter "name=^/nginx$" --format '{{.Names}}' | grep -qx "nginx"; then
    NGINX_WAS_RUNNING=1
  fi
}

restart_nginx_if_needed() {
  if [[ "${NGINX_WAS_RUNNING}" == "1" ]]; then
    echo "[INFO] 恢复 nginx 容器..."
    compose up -d nginx || docker start nginx >/dev/null 2>&1 || true
  fi
}

stop_nginx_for_challenge() {
  remember_nginx_state

  echo "[INFO] 临时停止 nginx 容器（释放80端口）..."
  compose stop nginx

  if docker ps --filter "name=^/nginx$" --format '{{.Names}}' | grep -qx "nginx"; then
    echo "[INFO] compose stop 后 nginx 仍在运行，使用 docker stop nginx 兜底..."
    docker stop nginx >/dev/null
  fi

  wait_for_port_80_free
}

on_exit() {
  local exit_code=$?
  if [[ "${exit_code}" != "0" ]]; then
    restart_nginx_if_needed
  fi
}

trap on_exit EXIT

echo "[INFO] 项目目录: ${PROJECT_ROOT}"
echo "[INFO] Compose文件: ${COMPOSE_FILE}"
echo "[INFO] 目标域名: ${DOMAIN}"
echo "[INFO] 证书目录: ${SSL_DIR}"

mkdir -p "${SSL_DIR}"

if [[ ! -x "${ACME_BIN}" ]]; then
  echo "[INFO] acme.sh 未安装，开始安装..."
  curl https://get.acme.sh | sh -s email="${EMAIL}"
fi

if [[ ! -x "${ACME_BIN}" ]]; then
  echo "[ERROR] acme.sh 安装失败，请检查网络。"
  exit 1
fi

echo "[INFO] 设置默认 CA 为 Let's Encrypt..."
"${ACME_BIN}" --set-default-ca --server letsencrypt

stop_nginx_for_challenge

echo "[INFO] 开始签发证书（standalone 模式）..."
"${ACME_BIN}" --issue -d "${DOMAIN}" --standalone --keylength ec-256 --force

echo "[INFO] 安装证书到项目目录..."
"${ACME_BIN}" --install-cert -d "${DOMAIN}" --ecc \
  --key-file "${SSL_DIR}/server.key" \
  --fullchain-file "${SSL_DIR}/server.pem"

chmod 600 "${SSL_DIR}/server.key"
chmod 644 "${SSL_DIR}/server.pem"

# echo "[INFO] 启动 nginx 容器..."
# compose up -d nginx

echo "[INFO] 证书申请并部署完成。"
echo "[INFO] 证书文件:"
echo "  - ${SSL_DIR}/server.pem"
echo "  - ${SSL_DIR}/server.key"
echo "[INFO] 可执行命令验证:"
echo "  openssl x509 -in ${SSL_DIR}/server.pem -noout -dates -issuer -subject"
