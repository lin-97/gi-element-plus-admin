# GI Element Plus Admin 项目简介

GI Element Plus Admin 是一个前后端分离的后台管理系统，后端基于 FastAPI，前端基于 Vue 3、Vite 和 Element Plus。项目提供用户认证、权限管理、系统配置、文件上传、运行监控、插件扩展和 Docker 部署等基础能力，适合作为后台管理系统或业务管理平台的开发脚手架。

## 技术栈

### 后端

- Python 3.12+
- FastAPI / Uvicorn
- SQLAlchemy 2.x / Alembic
- MySQL、PostgreSQL、SQLite
- Redis
- Pydantic Settings
- uv 包管理

### 前端

- Vue 3
- TypeScript
- Vite
- Element Plus
- Pinia
- Vue Router
- Axios
- ECharts
- pnpm 包管理

### 部署

- Docker
- Docker Compose
- Nginx
- MySQL
- Redis

## 项目目录结构

```text
.
├── backend/                # FastAPI 后端服务
├── frontend/               # 前端项目
│   ├── web/                # Vue 3 管理后台
│   └── app/                # 预留的应用端目录
├── docker/                 # Docker 部署配置
├── openspec/               # 项目规范与配置
└── README.md               # 项目说明文档
```

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
│   ├── plugin/             # 插件模块
│   │   ├── module_example/ # 插件开发示例，包含 plugin.toml 和 demo/controller.py
│   │   └── module_student/ # 学生业务插件示例，包含 model、schema、crud、controller
│   ├── common/             # 通用常量、响应结构、枚举
│   └── utils/              # 工具函数
└── static/                 # 静态文件与上传文件目录
```

## 前端目录结构

```text
frontend/
├── web/
│   ├── index.html          # Vite 入口 HTML
│   ├── package.json        # 前端依赖与脚本
│   ├── vite.config.ts      # Vite 配置
│   ├── public/             # 公共静态资源
│   └── src/
│       ├── apis/           # 接口请求封装
│       ├── assets/         # 图片等资源
│       ├── components/     # 通用组件
│       ├── config/         # 前端全局配置
│       ├── directives/     # 自定义指令
│       ├── hooks/          # 组合式函数
│       ├── layouts/        # 页面布局
│       ├── router/         # 路由与路由守卫
│       ├── stores/         # Pinia 状态管理
│       ├── styles/         # 全局样式
│       ├── utils/          # 工具函数
│       └── views/          # 页面视图
└── app/                    # 预留的应用端目录
```

## Docker 目录结构

```text
docker/
├── docker-compose.yaml     # MySQL、Redis、后端、Nginx 编排配置
├── .env.example            # Docker 部署环境变量示例
└── backend/
    ├── Dockerfile          # 后端服务镜像构建文件
    ├── README.md           # 后端镜像构建与部署说明
    └── request_letsencrypt.sh
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

### 前端管理后台

`frontend/web` 提供后台管理系统的页面入口，包括：

- 登录页
- 首页仪表盘
- 用户管理页面
- 通用 CRUD 示例页面
- 个人中心
- 权限路由与动态菜单
- 顶部栏、侧边栏、标签页、面包屑等后台布局组件

### 插件扩展

`app/plugin` 用于放置独立业务插件。项目会扫描 `app/plugin/module_*` 目录，读取插件配置，并自动发现插件下的 `controller.py` 路由文件。

每个插件通常包含：

- `plugin.toml`：插件元信息配置
- `__init__.py`：插件模块初始化入口
- `controller.py`：插件接口路由
- `model.py`：数据库模型
- `schema.py`：请求与响应数据结构
- `crud.py`：数据库操作封装

当前示例包括：

- `module_example`：最小插件示例，包含 `demo/controller.py`
- `module_student`：学生业务插件示例，包含 `student/model.py`、`student/schema.py`、`student/crud.py`、`student/controller.py`

插件路由会统一挂载到 `/api/v1/plugin` 下，并根据目录名自动生成业务前缀。例如 `module_student` 会挂载到 `/api/v1/plugin/student`。新增业务模块时，可以参考 `module_student/student` 的结构，把模型、接口、校验和数据访问逻辑放在插件目录内，减少对系统核心模块的侵入。

## 后端使用方法

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

## 前端使用方法

进入前端目录安装依赖：

```bash
cd frontend/web
pnpm install
```

启动开发服务：

```bash
pnpm dev
```

构建生产包：

```bash
pnpm build
```

预览生产构建：

```bash
pnpm preview
```

前端环境变量位于：

```text
frontend/web/.env.development
frontend/web/.env.production
```

常用配置项包括：

- `VITE_APP_TITLE`：应用标题
- `VITE_BASE`：前端基础路径
- `VITE_API_BASE_URL`：接口请求前缀

## Docker 使用方法

复制 Docker 环境变量示例文件：

```bash
cd docker
cp .env.example .env
```

根据实际情况修改 `docker/.env` 中的数据库、Redis、端口和密钥配置后启动：

```bash
docker compose --env-file .env up -d
```

Docker Compose 会编排以下服务：

- MySQL
- Redis
- 后端 API 服务
- Nginx

后端镜像构建与服务器部署细节可参考：

```text
docker/backend/README.md
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
