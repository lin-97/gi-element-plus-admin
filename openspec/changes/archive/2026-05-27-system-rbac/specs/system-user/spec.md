## ADDED Requirements

### Requirement: User list with required columns

The system SHALL provide `GET /api/user/list` with pagination. Each list item MUST include: `id`, `username`, `nickname`, `phone`, `email`, `avatar`, `remark`, `status`, `createTime`, and role display data (`roleIds` or `roleNames`/`roles` for tags).

#### Scenario: Filter by username and status

- **WHEN** super admin requests list with `username` and `status` query params
- **THEN** the system returns only matching users

### Requirement: User CRUD with multi-role

The system SHALL support `POST /api/user`, `PUT /api/user/{id}`, `GET /api/user/{id}`, and `POST /api/user/delete` with `{ ids }` for batch delete. Create/update MUST accept `roleIds: number[]` to assign multiple roles.

#### Scenario: Create user with roles

- **WHEN** super admin creates a user with `username`, `password`, `roleIds`, and optional profile fields
- **THEN** the user is stored with hashed password and `sys_user_role` rows for each `roleId`

#### Scenario: Update user roles

- **WHEN** super admin updates `roleIds` on an existing user
- **THEN** the system replaces role associations to match the provided list

### Requirement: User status field

User enable/disable MUST use `status`: `'1'` enabled, `'0'` disabled. The system MUST expose `PUT /api/user/{id}/status` with body `{ status }`.

#### Scenario: Disabled user cannot login

- **WHEN** a user has `status='0'` and attempts login with valid credentials
- **THEN** the system returns HTTP 401 or 403 with an appropriate message

#### Scenario: Toggle status from list

- **WHEN** super admin sets a user's `status` to `'0'` via status API
- **THEN** the user is disabled immediately for new login attempts

### Requirement: Reset password by admin

The system SHALL provide `PUT /api/user/{id}/password` accepting `{ password }`. Only super admin MAY call this endpoint. Password MUST NOT appear in list or detail responses.

#### Scenario: Admin resets password

- **WHEN** super admin submits a new password for user id 5
- **THEN** the stored hash is updated and the response does not echo the password

### Requirement: User profile fields

Users MUST support optional `phone`, `email`, `avatar` (URL string), and `remark`. `deptId` MAY be stored but MUST NOT be required or shown in UI in this change.

#### Scenario: Avatar as URL

- **WHEN** super admin saves `avatar: "https://example.com/a.png"`
- **THEN** list and detail return the same URL for display with `el-avatar`

### Requirement: User createTime in API

User API responses MUST use `createTime` (camelCase), not `created_at`.

#### Scenario: User list includes createTime

- **WHEN** super admin loads user list
- **THEN** each row includes `createTime`

### Requirement: User safety rules

The system MUST NOT allow deleting or disabling the currently authenticated user. The system MUST NOT allow removal of the last active `role_admin` holder.

#### Scenario: Self-delete blocked

- **WHEN** super admin attempts to delete their own user id
- **THEN** the system returns HTTP 400

#### Scenario: Batch delete

- **WHEN** super admin posts `/api/user/delete` with `{ ids: ["1","2"] }`
- **THEN** all specified users are deleted except when blocked by safety rules

### Requirement: User management UI location

Frontend MUST implement user management at `views/system/user/index.vue` with `FormDialog.vue`, registered under parent menu **系统管理** at route `/system/user/index`.

#### Scenario: Menu navigation

- **WHEN** super admin opens 系统管理 → 用户管理
- **THEN** the user list page loads with search, table, batch delete, and row actions including edit, reset password, and status toggle

### Requirement: Reset password UI

Frontend MUST provide a dialog for reset password with new password and confirm password fields; submission calls `PUT /api/user/{id}/password`.

#### Scenario: Password mismatch

- **WHEN** admin enters mismatched confirm password
- **THEN** the form does not submit and shows validation error

### Requirement: Role selection uses options API

User form role field MUST be a multi-select fed by `GET /api/role/options` (all enabled roles).

#### Scenario: Open user create dialog

- **WHEN** admin opens add-user dialog
- **THEN** role options are loaded from `/api/role/options` and only enabled roles are selectable
