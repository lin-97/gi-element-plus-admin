## ADDED Requirements

### Requirement: Role list with pagination

The system SHALL provide `GET /api/role/list` returning paginated roles with fields: `id`, `code`, `name`, `status`, `sort`, `remark`, `createTime`, and `isSystem` (when applicable). Response format MUST match frontend `PageResult`.

#### Scenario: Admin queries role list

- **WHEN** an authenticated super admin requests `/api/role/list` with `page` and `size`
- **THEN** the system returns `code: 200` and `data.list` containing roles ordered by `sort` then `id`

#### Scenario: Non-admin denied

- **WHEN** a user without super-admin privileges requests `/api/role/list`
- **THEN** the system returns HTTP 403

### Requirement: Role CRUD

The system SHALL support creating, updating, and batch-deleting roles via `POST /api/role`, `PUT /api/role/{id}`, and `POST /api/role/delete` with body `{ ids }`.

#### Scenario: Create role

- **WHEN** super admin submits `{ code, name, status, sort?, remark? }` with unique `code`
- **THEN** the system creates the role with `status` defaulting to `'1'` if omitted

#### Scenario: Duplicate code rejected

- **WHEN** super admin creates a role with an existing `code`
- **THEN** the system returns HTTP 400 with a clear error message

#### Scenario: Batch delete roles

- **WHEN** super admin posts `/api/role/delete` with `{ ids: [1,2] }` and no role is `isSystem` and no role has assigned users
- **THEN** the system deletes the roles and returns success

### Requirement: System role protection

The system SHALL mark `role_admin` as `isSystem=true`. System roles MUST NOT be deletable or have `code` changed.

#### Scenario: Delete system role blocked

- **WHEN** super admin attempts to delete `role_admin`
- **THEN** the system returns HTTP 400 and does not delete the role

### Requirement: Role options for user form

The system SHALL provide `GET /api/role/options` returning all roles where `status='1'`, as `{ id, code, name }[]` without pagination.

#### Scenario: Load enabled roles for dropdown

- **WHEN** super admin requests `/api/role/options`
- **THEN** the system returns only roles with `status='1'`

### Requirement: Role status field

Role enable/disable MUST use field `status` with values `'1'` (enabled) or `'0'` (disabled).

#### Scenario: Disabled role excluded from effective permissions

- **WHEN** a role has `status='0'`
- **THEN** that role's `code` MUST NOT appear in any user's `roles` array from `/api/auth/userinfo`, even if `sys_user_role` rows still exist

### Requirement: Role createTime in API

Role API responses MUST expose creation time as `createTime` (camelCase, ISO 8601 string), not `created_at`.

#### Scenario: Role list includes createTime

- **WHEN** super admin loads role list
- **THEN** each item in `data.list` includes `createTime`

### Requirement: Role menu assignment

The system SHALL provide `GET /api/role/{id}/menus` returning `{ menuIds: number[] }` representing all menu IDs assigned to the role (flattened, including descendants when a directory was selected). The system SHALL provide `PUT /api/role/{id}/menus` with body `{ menuIds: number[] }` to replace role menu links. Both endpoints MUST require super-admin.

When saving, if the client submits a directory menu ID, the server MUST expand it to include all descendant menu IDs (types 1, 2, and 3) before persisting to `sys_role_menu`.

#### Scenario: Load role menus for edit

- **WHEN** super admin requests `GET /api/role/2/menus`
- **THEN** the system returns all `menuIds` currently linked to role id 2

#### Scenario: Save role menus with directory expansion

- **WHEN** super admin submits `PUT /api/role/2/menus` with `menuIds` containing only a directory id that has two page children and three button children
- **THEN** `sys_role_menu` contains rows for the directory, both pages, and all three buttons

#### Scenario: Super admin role skips assignment

- **WHEN** super admin requests menus for role `role_admin`
- **THEN** the UI treats the role as having all menus (tree disabled or equivalent) and the API MAY return all menu ids or an empty list with documented super-admin bypass on routes

### Requirement: Role form menu permission tree

The role create/edit dialog MUST include a menu permission tree (`el-tree` with checkboxes) loaded from `GET /api/menu/tree`. On edit, checked keys MUST reflect `GET /api/role/{id}/menus`. On save (create or update flow), menu IDs MUST be persisted via `PUT /api/role/{id}/menus` after the role record exists.

#### Scenario: Edit role shows checked menus

- **WHEN** super admin opens edit for a role with assigned menus
- **THEN** the menu tree shows the role's menus as checked

#### Scenario: Save role persists menus

- **WHEN** super admin saves role menu selections
- **THEN** the system persists `sys_role_menu` and the frontend calls `refreshRoutes`
