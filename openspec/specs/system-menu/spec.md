## ADDED Requirements

### Requirement: Menu tree for administration

The system SHALL provide `GET /api/menu/tree` returning the full menu hierarchy (types 1, 2, and 3) for super-admin management. Nodes MUST include fields compatible with frontend `AsyncRouteItem` (camelCase), including `id`, `parentId`, `title`, `type`, `path`, `component`, `redirect`, `icon`, `permission`, `sort`, `status`, route meta flags, and nested `children`.

#### Scenario: Super admin loads menu tree

- **WHEN** a super admin requests `GET /api/menu/tree`
- **THEN** the system returns `code: 200` with a nested tree ordered by `sort` then `id`

#### Scenario: Non-admin denied

- **WHEN** a user without super-admin privileges requests `GET /api/menu/tree`
- **THEN** the system returns HTTP 403

### Requirement: Menu CRUD

The system SHALL support creating, updating, and batch-deleting menus via `POST /api/menu`, `PUT /api/menu/{id}`, and `POST /api/menu/delete` with body `{ ids }`. Write operations MUST require super-admin.

#### Scenario: Create directory menu

- **WHEN** super admin submits a menu with `type=1`, `title`, `path`, `component=Layout`, and `status='1'`
- **THEN** the system creates the menu and returns success

#### Scenario: Create button permission

- **WHEN** super admin submits a menu with `type=3`, non-empty `permission`, and `parentId` pointing to a `type=2` menu
- **THEN** the system creates the button node with unique `permission`

#### Scenario: Duplicate permission rejected

- **WHEN** super admin creates a button with a `permission` that already exists
- **THEN** the system returns HTTP 400 with a clear error message

#### Scenario: Delete menu with children blocked

- **WHEN** super admin attempts to delete a menu that has child nodes
- **THEN** the system returns HTTP 400 and does not delete the menu

### Requirement: System menu protection

Menus with `isSystem=true` (seeded system-management entries) MUST NOT be deletable.

#### Scenario: Delete system menu blocked

- **WHEN** super admin attempts to delete a menu where `isSystem=true`
- **THEN** the system returns HTTP 400 and does not delete the menu

### Requirement: Runtime menu routes from database

`GET /api/menu/routes` MUST build the route tree from `sys_menu` (not hardcoded MOCK). It MUST return only enabled (`status='1'`) nodes of type 1 (directory) and type 2 (page). Type 3 (button) MUST NOT appear in the response.

#### Scenario: Routes exclude buttons

- **WHEN** any authenticated user requests `/api/menu/routes`
- **THEN** no item in the response has `type=3`

#### Scenario: Empty directory pruned

- **WHEN** a type-1 directory has no visible type-2 descendants after authorization filtering
- **THEN** that directory is omitted from the response

### Requirement: Menu management page route

The seeded menu tree MUST include **菜单管理** under **系统管理** with `component: system/menu/index` and path `/system/menu/index`.

#### Scenario: Super admin sees menu management

- **WHEN** super admin logs in and routes are generated
- **THEN** sidebar shows 系统管理 including 菜单管理
