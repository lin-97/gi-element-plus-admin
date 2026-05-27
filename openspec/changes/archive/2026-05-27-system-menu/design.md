## Context

GI Element Plus Admin 当前状态：

- `GET /api/menu/routes` 返回 `MOCK_ASYNC_ROUTES`（`backend/app/api/menu.py`）
- 菜单过滤使用菜单项上的 `roles[]` 与超管跳过逻辑
- `get_user_permissions` 通过 `ROLE_PERMISSION_MAP` 硬编码聚合
- 前端 `AsyncRouteItem` 契约已与 `useRouteStore` 对齐；`generateRoutes` 仅在路由 guard 首次执行；`registerAsyncRoutes` 对已存在 `name` 会 skip，无法热更新
- 用户/角色 CRUD 已完成；角色表单尚无菜单授权

本 change 在「系统管理」下新增菜单管理，并完成菜单入库 + `role_menu` + 按钮权限 + 路由热刷新。

## Goals / Non-Goals

**Goals:**

- `sys_menu` 存储完整 `AsyncRouteItem` 字段（API camelCase）
- `sys_role_menu` 授权；保存时勾选目录 **自动展开** 所有子孙（type 1/2/3）扁平写入
- type=3 按钮：`permission` 必填且库内唯一；参与 `userinfo.permissions`，**不参与**动态路由
- `/menu/routes`：超管全量；普通用户按 `role_menu` + 补全祖先节点；仅 type 1/2
- 菜单管理：整页 `el-table` 树形表格；超管写接口
- 角色表单：菜单树勾选 + `GET/PUT /role/{id}/menus`
- `refreshRoutes()`：移除旧动态路由 → `fetchUserInfo` → `getRoutesApi` → `setRoutes` → 必要时 `router.replace`
- 菜单 CRUD / 角色菜单保存 **成功后自动** `refreshRoutes`
- seed：迁移 MOCK + 学生/系统模块典型按钮 permission

**Non-Goals:**

- 在线用户广播刷新（仅当前会话）
- 菜单自动生成 `.vue` 文件
- 部门管理
- 从文件扫描自动发现路由

## Decisions

### 1. 授权模型：`sys_role_menu` 替代菜单 `roles[]`

- 关联表 `(role_id, menu_id)` 联合唯一
- 超管不写关联行，查询时视为全部菜单
- 保存角色菜单时：前端勾选目录 → 后端递归展开子孙 ID → 去重写入

**备选**：保留菜单 `roles[]` — 已否决，与角色授权 UI 双源维护。

### 2. 权限聚合：从菜单按钮读取

- `get_user_permissions`：`JOIN sys_role_menu` + `sys_menu`，`type=3` 且 `status='1'` 且 `permission` 非空 → distinct
- type=2 若配置了 `permission` 一并并入（页面级）
- 超管仍 `['*:*:*']`
- 删除 `ROLE_PERMISSION_MAP`（seed 将 `crud:list` 等写入按钮菜单）

### 3. 动态路由与按钮分离

- `/menu/routes` 仅返回 type 1/2（沿用过滤空目录逻辑）
- type=3 仅用于 `v-hasPerm` / `hasPerm`

### 4. 热刷新路由

- `useRouteStore` 维护 `dynamicRouteNames: string[]`
- `resetDynamicRoutes()`：`router.removeRoute(name)` 逐个移除
- `useUserStore.refreshRoutes()`：reset → fetchUserInfo → getRoutesApi → setRoutes → 更新 persist
- 菜单页工具栏提供手动「刷新路由」
- `router/guard` 的 `isRoutesLoaded` 与 refresh 协调（refresh 不依赖重新登录）

**备选**：强制重新登录 — 已否决。

### 5. 菜单管理 UI

- 不用 `useTable` 分页模式；独立页面 `el-table` + `tree-props`
- `FormDialog` 按 `type` 切换字段；type=3 仅 permission/排序/状态

### 6. 系统内置菜单

- `is_system=true`：系统管理根、用户/角色/菜单管理节点不可删
- 删除前校验无子节点

### 7. ID 与 API

- DB 自增 `INTEGER`；对外 JSON `id`/`parentId` 转 string 兼容 `AsyncRouteItem`

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 动态路由残留/重复 | `dynamicRouteNames` + removeRoute 后再 add |
| 删除当前所在菜单页 | 删除校验；refresh 后不存在则 redirect 首页 |
| permission 迁移遗漏 | seed 覆盖 MOCK 中所有 permission；联调 `v-hasPerm` |
| 角色勾选目录漏按钮 | 保存时后端强制展开子孙 |
| routeStore persist 陈旧 | refresh 时同步写入 persist |

## Migration Plan

1. 新增表 `sys_menu`、`sys_role_menu`
2. seed 从 `MOCK_ASYNC_ROUTES` 转换插入（含按钮节点）
3. 为 `role_user` 写入示例 `role_menu`
4. 切换 `/menu/routes` 读 DB；删除 MOCK
5. 改造 `get_user_permissions`；移除 `ROLE_PERMISSION_MAP`
6. 部署后端后部署前端

**回滚**：DB 备份；可临时恢复 MOCK 分支（不推荐长期）。

## Open Questions

- （已闭合）勾选目录自动包含子孙：是
- （已闭合）改角色菜单后自动 refreshRoutes：是
