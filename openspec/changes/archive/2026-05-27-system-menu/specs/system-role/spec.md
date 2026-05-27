## ADDED Requirements

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
