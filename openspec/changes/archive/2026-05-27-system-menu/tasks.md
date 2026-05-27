## 1. 数据库与模型

- [x] 1.1 新增 `SysMenu`、`SysRoleMenu` 模型（字段对齐 `AsyncRouteItem` + `is_system`）
- [x] 1.2 编写 migration/seed：由 `MOCK_ASYNC_ROUTES` 转换插入（含 type=3 按钮、系统管理、菜单管理入口）
- [x] 1.3 seed 为 `role_user` 写入示例 `sys_role_menu`；`role_admin` 不写关联行

## 2. 后端 — 菜单 CRUD

- [x] 2.1 实现 `menu_crud`（树查询、CRUD、批量删除、子孙展开、系统菜单/有子节点保护）
- [x] 2.2 实现 `schemas`（MenuCreate/Update、TreeNode、BatchDelete）
- [x] 2.3 实现 `api/menu.py` 管理端点：`GET /tree`、`POST`、`PUT /{id}`、`POST /delete`（超管）
- [x] 2.4 改造 `GET /menu/routes`：读 DB、按 `role_menu` 过滤、仅 type 1/2；删除 MOCK

## 3. 后端 — 角色菜单与权限

- [x] 3.1 实现 `role_menu_crud`（查询、全量替换、目录勾选展开子孙）
- [x] 3.2 实现 `GET/PUT /api/role/{id}/menus`
- [x] 3.3 改造 `get_user_permissions`：从已授权菜单按钮聚合；移除 `ROLE_PERMISSION_MAP`
- [x] 3.4 `menu_to_dict` / formatters；注册路由

## 4. 前端 — API 与路由刷新

- [x] 4.1 扩展 `apis/menu.ts`（tree、CRUD、routes 类型）
- [x] 4.2 扩展 `apis/role.ts`（`getRoleMenusApi`、`updateRoleMenusApi`）
- [x] 4.3 `useRouteStore`：`dynamicRouteNames`、`resetDynamicRoutes`；`setRoutes` 记录 name
- [x] 4.4 `useUserStore.refreshRoutes`（reset → fetchUserInfo → getRoutesApi → setRoutes）
- [x] 4.5 协调 `router/guard` 与 persist 更新

## 5. 前端 — 菜单管理页

- [x] 5.1 创建 `views/system/menu/index.vue`（树形 `el-table`、工具栏含刷新路由）
- [x] 5.2 创建 `views/system/menu/FormDialog.vue`（按 type 1/2/3 切换字段）
- [x] 5.3 保存/删除成功后自动 `refreshRoutes`

## 6. 前端 — 角色菜单授权

- [x] 6.1 `role/FormDialog.vue` 增加菜单权限 `el-tree`（勾选目录联动子孙）
- [x] 6.2 编辑时加载 `getRoleMenusApi`；保存后 `updateRoleMenusApi` + `refreshRoutes`
- [x] 6.3 超管角色菜单树 disabled

## 7. 联调与验证

- [x] 7.1 admin 登录：侧边栏含菜单管理；菜单树 CRUD 全流程
- [x] 7.2 为 `role_user` 分配部分菜单：该用户登录仅见授权路由
- [x] 7.3 改按钮 permission / 角色菜单后：当前会话自动 refresh，`v-hasPerm` 生效
- [x] 7.4 验证系统菜单不可删、有子节点不可删、permission 唯一约束
