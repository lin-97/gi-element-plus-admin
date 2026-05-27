# GI Element Plus Admin 后端简介

GI Element Plus Admin 是一个基于 FastAPI 的后台管理系统后端服务，提供用户认证、权限管理、系统配置、文件上传、运行监控和插件扩展等通用管理能力。项目采用前后端分离结构，本文主要说明 `backend` 后端部分。

## 技术栈

- Python 3.12+
- FastAPI / Uvicorn
- SQLAlchemy 2.x / Alembic
- MySQL、PostgreSQL、SQLite
- Redis
- Pydantic Settings
- uv 包管理

## 后端目录结构

```text
backend/
├── main.py                 # Typer 命令入口，负责启动服务、生成迁移、执行迁移、初始化数据
├── pyproject.toml          # 后端依赖与工具配置
├── alembic.ini             # Alembic 数据库迁移配置
├── env/                    # 不同环境的配置文件，如 .env.dev、.env.test、.env.prod
├── sql/                    # MySQL、PostgreSQL 初始化 SQL
├── app/
│   ├── api/v1/             # v1 接口路由
│   │   ├── module_system/  # 系统管理模块
│   │   ├── module_common/  # 通用能力模块
│   │   └── module_monitor/ # 系统监控模块
│   ├── core/               # 数据库、Redis、中间件、权限、日志、异常等核心能力
│   ├── config/             # 配置读取与路径配置
│   ├── scripts/            # 初始化应用与基础数据脚本
│   ├── plugin/             # 插件模块示例与扩展模块
│   ├── common/             # 通用常量、响应结构、枚举
│   └── utils/              # 工具函数
└── static/                 # 静态文件与上传文件目录
```

## 功能介绍

### 系统管理

`module_system` 提供后台管理系统的基础能力，包括：

- 登录认证、JWT Token、验证码
- 用户管理
- 角色管理
- 菜单管理
- 部门管理
- 岗位管理
- 字典管理
- 参数配置
- 操作日志

### 通用模块

`module_common` 提供公共接口能力，包括：

- 健康检查
- 文件上传与静态文件访问
- 插件信息与插件路由挂载

### 系统监控

`module_monitor` 提供服务运行状态相关接口，包括：

- 服务器资源监控
- Redis 缓存监控
- 在线用户监控
- 系统资源信息

### 插件扩展

`app/plugin` 用于放置插件模块。项目会动态发现并挂载插件路由，示例中包含 `module_example` 和 `module_student`，适合按业务模块扩展独立功能。

## 使用方法

### 1. 安装依赖

进入后端目录后安装依赖：

```bash
cd backend
uv sync
```

### 2. 配置环境变量

开发环境配置文件位于：

```text
backend/env/.env.dev
```

常用配置项包括：

- `DATABASE_TYPE`：数据库类型，支持 `mysql`、`postgres`、`sqlite`
- `MYSQL_HOST`、`MYSQL_PORT`、`MYSQL_USER`、`MYSQL_PASSWORD`、`MYSQL_DATABASE`
- `POSTGRES_HOST`、`POSTGRES_PORT`、`POSTGRES_USER`、`POSTGRES_PASSWORD`、`POSTGRES_DATABASE`
- `REDIS_ENABLE`、`REDIS_HOST`、`REDIS_PORT`
- `SECRET_KEY`、`ACCESS_TOKEN_EXPIRE_MINUTES`

### 3. 启动开发服务

```bash
cd backend
uv run main.py run --env=dev
```

服务启动时会自动：

- 检查并创建数据库
- 执行 Alembic 迁移
- 初始化基础数据
- 连接 Redis
- 注册中间件、异常处理、接口路由和静态文件

默认接口文档地址：

```text
http://localhost:8000/docs
```

### 4. 数据库迁移

模型变更后生成迁移文件：

```bash
cd backend
uv run main.py revision --env=dev
```

执行迁移：

```bash
cd backend
uv run main.py upgrade --env=dev
```

手动初始化基础数据：

```bash
cd backend
uv run main.py init-data --env=dev
```

### 5. 脚本启动

Linux / macOS 可以使用项目提供的脚本：

```bash
cd backend
./run_linux.sh
```

Windows 可以使用：

```bat
cd backend
run_win.bat
```

## 接口前缀

后端接口统一挂载在：

```text
/api/v1
```

插件接口会挂载到：

```text
/api/v1/plugin
```
