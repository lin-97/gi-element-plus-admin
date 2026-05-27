## Why

系统管理已具备用户、角色、菜单的库表化 RBAC，但业务表单中的下拉选项（如性别、启用/禁用状态）仍硬编码在前端常量中，运营无法配置，也无法与字典数据统一管理。需要新增字典类型与字典数据的主从管理页，并提供按类型编码的运行时查询，将 `GENDER`、`STATUS` 等内置字典入库，形成可配置、可复用的数据字典能力。

## What Changes

- 新增 **`sys_dict_type`**、**`sys_dict_data`** 表（1:N，删除类型时级联删除数据）
- 新增 **字典管理** 主从页面：左侧字典类型列表（无分页），右侧字典数据分页表格
- 新增字典类型/数据的超管 CRUD API，及 **`GET /api/dict/data/by-code/{code}`** 运行时接口（仅返回启用项）
- Seed 内置字典 **`GENDER`**、**`STATUS`**（`is_system=true`，不可删除）
- 类型 `code` 强制大写英文；数据 `value` 统一为字符串；类型 `code` 创建后不可修改
- 菜单 seed：在「系统管理」下增加「字典管理」及按钮权限
- 前端将 `GENDER_OPTIONS`、`STATUS_OPTIONS` 硬编码改为按 `code` 从接口加载（可封装 `useDict`）

## Capabilities

### New Capabilities

- `system-dict`: 字典类型/数据 CRUD、主从管理页、内置字典保护、级联删除、按 code 运行时查询、seed 迁移

### Modified Capabilities

- （无）现有 `auth-rbac`、`system-role`、`system-menu` 的规范行为不变；仅新增菜单入口与前端消费方式调整

## Impact

- **后端**：`models` 新增 `SysDictType`、`SysDictData`；`dict_crud`；`api/dict.py`；`dict_migration` seed；`main.py` 注册路由
- **前端**：`apis/dict.ts`；`views/system/dict/*`（主从布局）；`hooks/useDict`（可选）；改造 `student`/`role`/`user`/`menu` 等页面的状态/性别选项来源
- **菜单**：`menu_migration.py` 增加 `system:dict` 页面及按钮节点
