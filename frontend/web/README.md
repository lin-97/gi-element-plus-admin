# GI Element Plus Admin

基于 Vue 3 + TypeScript + Element Plus 构建的企业级后台管理系统模板。

## ✨ 项目特点

### 🎯 核心技术栈

- **Vue 3** - 渐进式 JavaScript 框架，采用 Composition API
- **TypeScript** - 类型安全的 JavaScript 超集
- **Vite 7** - 下一代前端构建工具，极速热更新
- **Element Plus** - Vue 3 组件库，企业级 UI 设计
- **Pinia** - Vue 官方状态管理库
- **Vue Router 4** - Vue 路由管理器

### 🚀 功能特性

#### 权限管理

- 基于角色的访问控制（RBAC）
- 动态路由加载
- 权限指令 `v-hasPerm` 和 `v-hasRole`
- 登录/登出状态管理

#### 布局系统

- 支持多种布局模式（侧边栏、顶部导航）
- 响应式设计，适配多种屏幕尺寸
- 可折叠侧边栏
- 面包屑导航

#### 系统管理

- 用户管理（增删改查、密码重置）
- 角色管理（权限配置）
- 菜单管理（动态路由配置）
- 数据字典管理

#### 界面交互

- 标签页管理（打开、关闭、刷新）
- 主题切换（亮色/暗色模式）
- 设置抽屉
- 页面过渡动画

#### 开发体验

- 自动导入组件和 API
- ESLint + Stylelint 代码规范
- 类型检查（vue-tsc）
- 构建产物 Gzip 压缩

### 📁 项目结构

```
src/
├── apis/           # API 接口定义
├── components/     # 公共组件
├── config/         # 配置文件
├── core/           # 核心模块
│   ├── directives/ # 自定义指令
│   ├── hooks/      # 组合式函数
│   ├── stores/     # Pinia 状态管理
│   └── utils/      # 工具函数
├── hooks/          # 业务 hooks
├── icons/          # 图标配置
├── layouts/        # 布局组件
├── plugins/        # 插件配置
├── router/         # 路由配置
├── stores/         # 业务状态管理
├── styles/         # 全局样式
├── types/          # 类型定义
├── utils/          # 通用工具
└── views/          # 页面视图
```

## 🛠️ 快速开始

### 环境要求

- Node.js >= 20
- pnpm >= 8

### 安装依赖

```bash
pnpm install
```

### 开发模式

```bash
pnpm run dev
```

访问 http://localhost:5050 查看效果。

### 生产构建

```bash
pnpm run build
```

### 预览构建结果

```bash
pnpm run preview
```

### 代码检查

```bash
# 类型检查
pnpm run typecheck

# ESLint 检查
pnpm run lint

# 样式检查
pnpm run lint:style
```

## 🔧 配置说明

### 环境变量

在 `.env.development` 或 `.env.production` 中配置：

| 变量                  | 说明         | 默认值                |
| --------------------- | ------------ | --------------------- |
| VITE_BASE             | 项目基础路径 | /                     |
| VITE_API_PROXY_TARGET | API 代理目标 | http://localhost:8000 |

### 路由配置

路由定义在 `src/router/routes.ts`，支持：

- 动态路由（通过后端接口获取）
- 路由守卫（权限验证）
- 路由懒加载

### 状态管理

使用 Pinia 进行状态管理，分为：

- `useAppStore` - 应用配置
- `usePermissionStore` - 权限状态
- `useRouteStore` - 路由状态
- `useTabsStore` - 标签页状态
- `useUserStore` - 用户状态

## 📝 代码规范

### 命名规范

- 组件名：PascalCase（如 `AppHeader.vue`）
- 文件目录：kebab-case（如 `app-header`）
- 变量/函数：camelCase

### 样式规范

- 使用 SCSS 预处理器
- BEM 命名规范
- 全局变量定义在 `src/styles/var.scss`

## 📄 License

MIT
