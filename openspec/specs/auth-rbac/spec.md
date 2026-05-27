## ADDED Requirements

### Requirement: Userinfo returns roles and permissions

`GET /api/auth/userinfo` MUST return user profile plus `roles: string[]` (role codes) and `permissions: string[]`. Users with `role_admin` MUST receive `permissions` containing `*:*:*`.

#### Scenario: Super admin userinfo

- **WHEN** a user with `role_admin` requests userinfo
- **THEN** `roles` includes `role_admin` and `permissions` includes `*:*:*`

#### Scenario: Multi-role user

- **WHEN** a user is assigned roles `editor` and `operator` (both enabled)
- **THEN** `roles` equals `["editor","operator"]` and `permissions` reflects the union of mapped permissions

### Requirement: Login response alignment

`POST /api/auth/login` success payload MUST include `user` object compatible with userinfo (including `roles`; `permissions` MAY be omitted on login if userinfo is fetched immediately after).

#### Scenario: Login then permission store

- **WHEN** frontend completes login and calls `fetchUserInfo`
- **THEN** `usePermissionStore.setRoles` and `setPermissions` are invoked with API values

### Requirement: Menu routes filtered by roles

`GET /api/menu/routes` MUST filter menu items: if `item.roles` is empty, item is visible to all authenticated users; otherwise the user MUST have at least one matching role code. Super admin MUST receive all routes without filtering.

#### Scenario: Editor sees limited menus

- **WHEN** menu item has `roles: ["editor"]` and user has `roles: ["editor"]`
- **THEN** the item is included in the response

#### Scenario: Super admin sees all

- **WHEN** user has `role_admin`
- **THEN** all enabled menu items are returned regardless of `roles` on each item

### Requirement: Super admin guard on write APIs

User and role mutation endpoints MUST require super-admin (holder of `role_admin` or equivalent guard replacing `role == "admin"`).

#### Scenario: Normal user cannot create user

- **WHEN** a user without `role_admin` calls `POST /api/user`
- **THEN** the system returns HTTP 403

### Requirement: System management menu structure

Backend menu MOCK (or equivalent) MUST include parent **系统管理** (`/system`) with children:

- 用户管理 → `component: system/user/index`, path `/system/user/index`
- 角色管理 → `component: system/role/index`, path `/system/role/index`

#### Scenario: Routes registered after login

- **WHEN** super admin logs in and `generateRoutes` runs
- **THEN** sidebar shows 系统管理 with 用户管理 and 角色管理 entries

### Requirement: Frontend permission utilities wired

After login or `fetchUserInfo`, frontend MUST populate `usePermissionStore` so `hasRole` and `hasPerm` work with `SUPER_ADMIN_ROLE` and `SUPER_ADMIN_PERMISSION` from `@/core/config`.

#### Scenario: Button hidden without permission

- **WHEN** a button uses `v-hasPerm="'system:user:add'"` and user lacks that permission
- **THEN** the button is not rendered

### Requirement: Deprecated single role field

The API MUST NOT rely on `user.role` as a single string for authorization after migration. **BREAKING** for clients expecting only `role: string`.

#### Scenario: Old client reads userinfo

- **WHEN** client expects `role: "admin"`
- **THEN** client MUST migrate to `roles: string[]` (documented in change proposal)
