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
