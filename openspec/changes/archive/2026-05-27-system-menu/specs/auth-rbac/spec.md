## MODIFIED Requirements

### Requirement: Userinfo returns roles and permissions

`GET /api/auth/userinfo` MUST return user profile plus `roles: string[]` (role codes) and `permissions: string[]`. Users with `role_admin` MUST receive `permissions` containing `*:*:*`. For non-super-admin users, `permissions` MUST be the distinct union of `permission` values from enabled (`status='1'`) menu nodes of type 3 (and type 2 when `permission` is set) that are authorized to the user via `sys_role_menu` for any of the user's enabled roles.

#### Scenario: Super admin userinfo

- **WHEN** a user with `role_admin` requests userinfo
- **THEN** `roles` includes `role_admin` and `permissions` includes `*:*:*`

#### Scenario: Multi-role user permissions from menus

- **WHEN** a user has roles `role_user` and `operator` (both enabled) and `sys_role_menu` grants button permissions `crud:list` and `system:user:add`
- **THEN** `permissions` includes both `crud:list` and `system:user:add`

### Requirement: Menu routes filtered by roles

`GET /api/menu/routes` MUST authorize menu visibility using `sys_role_menu`: a type-1 or type-2 menu is visible if it is directly linked to any of the user's enabled roles, or is an ancestor of such a linked menu. Super admin (`role_admin`) MUST receive all enabled route menus without consulting `sys_role_menu`. The menu item field `roles` MUST NOT be used for filtering.

#### Scenario: User sees menus granted by role_menu

- **WHEN** menu id `11` is linked to role `role_user` and the user has `role_user`
- **THEN** menu `11` and its ancestors appear in `/api/menu/routes`

#### Scenario: User does not see unlinked menus

- **WHEN** menu id `12` is not linked to any of the user's enabled roles
- **THEN** menu `12` is not included in `/api/menu/routes`

#### Scenario: Super admin sees all

- **WHEN** user has `role_admin`
- **THEN** all enabled route menus (type 1 and 2) are returned

### Requirement: System management menu structure

The menu data source (database seed, not MOCK) MUST include parent **系统管理** (`/system`) with children:

- 用户管理 → `component: system/user/index`, path `/system/user/index`
- 角色管理 → `component: system/role/index`, path `/system/role/index`
- 菜单管理 → `component: system/menu/index`, path `/system/menu/index`

#### Scenario: Routes registered after login

- **WHEN** super admin logs in and `generateRoutes` runs
- **THEN** sidebar shows 系统管理 with 用户管理, 角色管理, and 菜单管理 entries

## ADDED Requirements

### Requirement: Frontend refresh routes after permission changes

The frontend MUST expose `refreshRoutes()` that: removes previously registered dynamic routes, calls `fetchUserInfo` to refresh `permissions`, fetches `/api/menu/routes`, and re-registers routes via `setRoutes`. After menu CRUD success or role menu assignment success, the UI MUST invoke `refreshRoutes()` automatically for the current session.

#### Scenario: Menu save triggers refresh

- **WHEN** super admin saves a menu in 菜单管理 and the API returns success
- **THEN** the frontend calls `refreshRoutes` without requiring re-login

#### Scenario: Manual refresh available

- **WHEN** super admin clicks 刷新路由 on the menu management page
- **THEN** `refreshRoutes` runs and the sidebar reflects the latest menu tree

#### Scenario: Role menu save triggers refresh

- **WHEN** super admin saves role menu permissions and the API returns success
- **THEN** the frontend calls `refreshRoutes` and updates `usePermissionStore.permissions`
