# system-dict Specification

## Purpose

系统字典管理能力：字典类型与字典数据的 CRUD、运行时按 code 查询、前端字典管理页与 useDict 消费。
## Requirements
### Requirement: Dictionary type list for administration

The system SHALL provide `GET /api/dict/type/list` returning all dictionary types (no pagination) for super-admin management. Each item MUST include `id`, `name`, `code`, `status`, `sort`, `remark`, `isSystem`, `createTime`, and `updateTime` (camelCase in JSON). Optional query parameters: `name` (fuzzy match), `status` (`'1'` or `'0'`). Results MUST be ordered by `sort` then `id`.

#### Scenario: Super admin loads type list

- **WHEN** a super admin requests `GET /api/dict/type/list`
- **THEN** the system returns `code: 200` with `data` as an array of dictionary types

#### Scenario: Filter types by status

- **WHEN** super admin requests `GET /api/dict/type/list?status=1`
- **THEN** the system returns only types with `status='1'`

#### Scenario: Non-admin denied

- **WHEN** a user without super-admin privileges requests `GET /api/dict/type/list`
- **THEN** the system returns HTTP 403

### Requirement: Dictionary type CRUD

The system SHALL support creating and updating dictionary types via `POST /api/dict/type` and `PUT /api/dict/type/{id}`. Write operations MUST require super-admin.

On create, `code` MUST match `^[A-Z][A-Z0-9_]*$` and MUST be unique. On update, `code` MUST NOT be changeable.

#### Scenario: Create dictionary type

- **WHEN** super admin submits `{ name, code: "ORDER_STATUS", status?, sort?, remark? }`
- **THEN** the system creates the type and returns success with the created record

#### Scenario: Invalid code format rejected

- **WHEN** super admin creates a type with `code` not matching `^[A-Z][A-Z0-9_]*$`
- **THEN** the system returns HTTP 400 with a clear error message

#### Scenario: Duplicate code rejected

- **WHEN** super admin creates a type with an existing `code`
- **THEN** the system returns HTTP 400 with a clear error message

#### Scenario: Update type without changing code

- **WHEN** super admin updates a type with `{ name, status, sort, remark }` including a different `code` in the body
- **THEN** the system updates allowed fields and leaves `code` unchanged

### Requirement: Dictionary type batch delete with cascade

The system SHALL support batch-deleting dictionary types via `POST /api/dict/type/delete` with body `{ ids }`. Deleting a type MUST cascade-delete all `sys_dict_data` rows for that type. Write operations MUST require super-admin.

#### Scenario: Delete type cascades data

- **WHEN** super admin deletes a non-system type that has dictionary data rows
- **THEN** the system deletes the type and all associated data rows

#### Scenario: Delete system type blocked

- **WHEN** super admin attempts to delete a type where `isSystem=true`
- **THEN** the system returns HTTP 400 and does not delete the type or its data

### Requirement: Dictionary data list with pagination

The system SHALL provide `GET /api/dict/data/list` returning paginated dictionary data for super-admin management. Query parameters MUST include `typeId` (required). Optional: `label` (fuzzy), `status`, `page`, `size`. Response MUST match frontend `PageResult` with fields `id`, `typeId`, `label`, `value` (string), `status`, `sort`, `remark`, `createTime`.

#### Scenario: Super admin loads data for selected type

- **WHEN** super admin requests `GET /api/dict/data/list?typeId=1&page=1&size=10`
- **THEN** the system returns `code: 200` with `data.list` containing only rows for that type, ordered by `sort` then `id`

#### Scenario: Missing typeId rejected

- **WHEN** super admin requests `GET /api/dict/data/list` without `typeId`
- **THEN** the system returns HTTP 400

#### Scenario: Non-admin denied

- **WHEN** a user without super-admin privileges requests `GET /api/dict/data/list`
- **THEN** the system returns HTTP 403

### Requirement: Dictionary data CRUD

The system SHALL support creating, updating, and batch-deleting dictionary data via `POST /api/dict/data`, `PUT /api/dict/data/{id}`, and `POST /api/dict/data/delete` with body `{ ids }`. `value` MUST be stored and returned as a string. Within the same `typeId`, `value` MUST be unique. Write operations MUST require super-admin.

Creating data MUST require the parent type to exist and have `status='1'`.

#### Scenario: Create dictionary data

- **WHEN** super admin submits `{ typeId, label, value: "1", status?, sort?, remark? }` for an enabled type
- **THEN** the system creates the data row and returns success

#### Scenario: Create data for disabled type rejected

- **WHEN** super admin attempts to create data for a type with `status='0'`
- **THEN** the system returns HTTP 400

#### Scenario: Duplicate value per type rejected

- **WHEN** super admin creates data with a `value` that already exists for the same `typeId`
- **THEN** the system returns HTTP 400 with a clear error message

#### Scenario: Batch delete data

- **WHEN** super admin posts `/api/dict/data/delete` with `{ ids: [1,2] }`
- **THEN** the system deletes the rows and returns success

### Requirement: Dictionary data status update

The system SHALL provide `PUT /api/dict/data/{id}/status` with body `{ status }` where `status` is `'1'` or `'0'`. Write operations MUST require super-admin.

#### Scenario: Toggle data status

- **WHEN** super admin sets `status` to `'0'` for a data row
- **THEN** the system updates the row and the row is excluded from runtime by-code queries

### Requirement: Runtime dictionary by code

The system SHALL provide `GET /api/dict/data/by-code/{code}` for any authenticated user. The response MUST be `code: 200` with `data` as `{ label, value }[]` containing only rows where parent type and data row both have `status='1'`, ordered by `sort` then `id`. If the type code does not exist, the system MUST return an empty array (not 404).

#### Scenario: Load enabled gender options

- **WHEN** an authenticated user requests `GET /api/dict/data/by-code/GENDER`
- **THEN** the system returns enabled gender label/value pairs (e.g. 男/1, 女/2)

#### Scenario: Disabled data excluded

- **WHEN** a data row has `status='0'`
- **THEN** it does not appear in the by-code response

#### Scenario: Unknown code returns empty

- **WHEN** an authenticated user requests `GET /api/dict/data/by-code/UNKNOWN`
- **THEN** the system returns `code: 200` with `data: []`

### Requirement: Seeded system dictionaries

On application startup, the system MUST seed dictionary types `GENDER` (性别) and `STATUS` (状态) with `isSystem=true` and representative data matching current frontend constants (gender: 男/1, 女/2; status: 启用/1, 禁用/0). Seed MUST be idempotent.

#### Scenario: Seed runs on startup

- **WHEN** the application starts with an empty dictionary tables
- **THEN** `GENDER` and `STATUS` types and their data rows exist

#### Scenario: Seed is idempotent

- **WHEN** the application restarts after seed has already run
- **THEN** no duplicate types or data rows are created

### Requirement: Dictionary management menu

The seeded menu tree MUST include **字典管理** under **系统管理** with `component: system/dict/index`, path `/system/dict/index`, and button permissions for type and data operations (at minimum list/add/edit/delete).

#### Scenario: Super admin sees dictionary management

- **WHEN** super admin logs in and routes are generated
- **THEN** sidebar shows 系统管理 including 字典管理

### Requirement: Dictionary management page layout

The frontend MUST provide a dictionary management page at `views/system/dict/index.vue` with a master-detail layout: left panel for dictionary types (search, status filter, CRUD toolbar, non-paginated list with selection highlight) and right panel for dictionary data (toolbar, filter form, paginated table with row actions and status switch). The right panel MUST load data only for the selected type.

#### Scenario: Select type loads data table

- **WHEN** the user selects a dictionary type in the left panel
- **THEN** the right panel queries paginated data for that `typeId`

#### Scenario: Add data disabled when type disabled

- **WHEN** the selected type has `status='0'`
- **THEN** the add-data action is disabled and the backend rejects new data for that type

### Requirement: Frontend consumes dictionaries by code

The frontend MUST load select options for gender and common status fields from `GET /api/dict/data/by-code/{code}` (via a shared helper such as `useDict`) instead of hardcoded `GENDER_OPTIONS` and `STATUS_OPTIONS` arrays. Affected areas MUST include at least: student CRUD (gender), role/user/menu forms and list filters (status).

#### Scenario: Student form uses GENDER dictionary

- **WHEN** the student create/edit form opens
- **THEN** gender options are populated from dictionary code `GENDER`

#### Scenario: Role list filter uses STATUS dictionary

- **WHEN** the role list search form renders status dropdown
- **THEN** options are populated from dictionary code `STATUS`

### Requirement: 字典变更后前端缓存失效

当超级管理员在字典管理页成功创建、更新或删除字典类型或字典数据后，前端 SHALL 调用 `clearDictCache(code)` 使对应字典 code 的 `useDict` 内存缓存失效。删除字典类型时 MUST 清除该类型 `code` 的缓存；若无法确定 code，SHALL 调用无参 `clearDictCache()` 清空全部缓存。

#### Scenario: 编辑字典类型后缓存失效

- **WHEN** 超级管理员在 `DictTypeFormDialog` 成功更新字典类型且该类型 `code` 为 `ORDER_STATUS`
- **THEN** 前端调用 `clearDictCache('ORDER_STATUS')`
- **AND** 其他页面下次 `useDict(['ORDER_STATUS'])` 时重新请求 API

#### Scenario: 增删字典数据后缓存失效

- **WHEN** 超级管理员在 `DictDataFormDialog` 成功新增或更新字典数据
- **THEN** 前端根据当前选中字典类型的 `code` 调用 `clearDictCache(code)`

#### Scenario: 删除字典类型后缓存失效

- **WHEN** 超级管理员成功删除字典类型
- **THEN** 前端清除该类型 `code` 对应缓存（或清空全部字典缓存）

#### Scenario: 其他页面字典选项更新

- **WHEN** 字典管理页完成上述变更后，用户导航至使用 `useDict` 的业务页（如用户列表的状态筛选）
- **THEN** 下拉选项反映最新字典数据，无需整页刷新

