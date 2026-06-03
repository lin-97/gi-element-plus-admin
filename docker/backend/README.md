# 后端 Docker 部署

使用 Docker Compose 启动 MySQL、Redis 和后端 API。

## 快速开始

```bash
cd docker
cp .env.example .env
# 编辑 .env，修改密码和 SECRET_KEY

docker compose --env-file .env up -d --build
```

## 验证

```bash
docker compose ps
curl http://127.0.0.1:29891/api/v1/health
```

## 常用命令

```bash
# 查看 API 日志
docker logs gi-admin-api -f

# 重启 API
docker compose restart api

# 更新代码后重建 API 镜像
docker compose up -d --build api

# 停止（保留数据卷）
docker compose down
```

## 宝塔面板

1. 软件商店安装 **Docker 管理器**
2. Docker → **Compose** → 添加项目
3. Compose 路径：`/www/wwwroot/gi-admin-api/docker/docker-compose.yaml`
4. env 文件：`/www/wwwroot/gi-admin-api/docker/.env`
5. 构建并启动

## 说明

- 应用启动时会自动执行数据库迁移和初始化数据
- 上传文件与日志分别持久化到 `api_upload`、`api_logs` 卷
- 不要使用 `docker compose down -v`，否则会删除数据库数据
