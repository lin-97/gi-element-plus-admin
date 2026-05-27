## Why

系统 RBAC 一期已完成用户/角色管理，但菜单仍硬编码在 `MOCK_ASYNC_ROUTES`，权限来自 `ROLE_PERMISSION_MAP` 字典，无法运营配置。需要将菜单、按钮权限、角色授权统一入库，并支持改菜单/改角色权限后前端热刷新路由，形成可闭环的权限体系。

## What Changes

- 新增 **`sys_menu`** 树表（type：目录/菜单/按钮）与 **`sys_role_menu`** 角色-菜单关联表
- 新增 **菜单管理** CRUD 页面（整页树形表格 + FormDialog，含 type=3 按钮权限）
- **BREAKING**：`GET /api/menu/routes` 改从 DB 读取；废弃菜单项 `roles[]` 字段及 `MOCK_ASYNC_ROUTES`
- **BREAKING**：菜单过滤改为基于 `sys_role_menu`（超管 `role_admin` 跳过关联表，拥有全部菜单）
- **BREAKING**：`userinfo.permissions` 改从用户已授权菜单中 type=3 的 `permission` 字段聚合；移除对 `ROLE_PERMISSION_MAP` 的依赖（由 seed 按钮菜单替代）
- 角色管理增强：表单增加菜单权限树；勾选目录时 **自动展开** 包含其下所有菜单与按钮并扁平写入 `sys_role_menu`
- 保存菜单或角色菜单权限后：前端 **自动 `refreshRoutes`**（重置动态路由 + `fetchUserInfo` + 重新注册路由）
- 菜单管理页提供 **刷新路由** 按钮；seed 迁移现有 MOCK（学生管理 + 系统管理 + 菜单管理入口）

## Capabilities

### New Capabilities

- `system-menu`: 菜单树 CRUD、按钮 permission、系统内置菜单保护、`GET /menu/tree` 与运行时 `/menu/routes`

### Modified Capabilities

- `auth-rbac`: `/menu/routes` 数据源与 `role_menu` 过滤；`permissions` 从菜单按钮聚合；前端 `refreshRoutes`
- `system-role`: 角色分配菜单（`GET/PUT /role/{id}/menus`）；保存后触发热刷新

## Impact

- **后端**：`models` 新增 `SysMenu`、`SysRoleMenu`；`menu_crud`；扩展 `api/menu.py`；改造 `menu.py` routes 与 `get_user_permissions`；`role` API 增加 menus 端点；migration seed
- **前端**：`apis/menu.ts`；`views/system/menu/*`；`role/FormDialog` 菜单树；`useUserStore.refreshRoutes`；`useRouteStore.resetDynamicRoutes`；`router/guard` 配合
- **数据**：由 MOCK 迁移 seed；演示角色 `role_user` 示例 `role_menu` 关联
