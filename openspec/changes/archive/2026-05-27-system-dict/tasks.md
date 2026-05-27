## 1. 数据库与模型

- [x] 1.1 新增 `SysDictType`、`SysDictData` 模型（`type_id` FK `ondelete=CASCADE`，`UNIQUE(type_id, value)`）
- [x] 1.2 编写 `dict_migration.py`：幂等 seed `GENDER`、`STATUS` 及示例数据（`is_system=true`）
- [x] 1.3 在 `main.py` lifespan 中调用 `migrate_system_dict`

## 2. 后端 — 字典类型

- [x] 2.1 实现 `dict_type_crud`（列表、创建、更新、批量删除、code 校验、系统类型保护、级联删）
- [x] 2.2 实现 `schemas/dict_admin.py`（Type/Data Create/Update、ListQuery）
- [x] 2.3 实现 `dict_to_dict` formatters（camelCase）
- [x] 2.4 实现 `api/dict.py` 类型端点：`GET /type/list`、`POST /type`、`PUT /type/{id}`、`POST /type/delete`（超管）

## 3. 后端 — 字典数据与运行时

- [x] 3.1 实现 `dict_data_crud`（分页列表、CRUD、批量删除、同类型 value 唯一、禁用类型禁止新增）
- [x] 3.2 实现数据端点：`GET /data/list`、`POST /data`、`PUT /data/{id}`、`POST /data/delete`、`PUT /data/{id}/status`
- [x] 3.3 实现 `GET /data/by-code/{code}`（登录用户、仅启用项、未知 code 返回 `[]`）
- [x] 3.4 注册 `dict` router 至 `main.py`

## 4. 菜单 seed

- [x] 4.1 在 `menu_migration.py` 增加「字典管理」菜单（`system/dict/index`）及 `system:dict:*` 按钮权限
- [x] 4.2 确认超管可见新菜单；必要时为演示角色授权

## 5. 前端 — API 与 useDict

- [x] 5.1 创建 `apis/dict.ts`（类型/数据 CRUD、by-code、类型定义）
- [x] 5.2 创建 `hooks/useDict.ts`（按 code 加载并缓存 `{ label, value }[]`）

## 6. 前端 — 字典管理主从页

- [x] 6.1 创建 `views/system/dict/index.vue`（左右分栏、左栏类型列表与筛选、右栏 useTable）
- [x] 6.2 创建 `views/system/dict/DictTypeFormDialog.vue`
- [x] 6.3 创建 `views/system/dict/DictDataFormDialog.vue`
- [x] 6.4 实现类型选中联动、禁用类型禁止新增数据、行内状态开关、批量删除

## 7. 前端 — 替换硬编码选项

- [x] 7.1 学生 CRUD：`GENDER` 改用 `useDict('GENDER')`；移除或废弃 `GENDER_OPTIONS` 常量
- [x] 7.2 角色/用户/菜单：`STATUS` 改用 `useDict('STATUS')`；移除或废弃 `STATUS_OPTIONS` 常量
- [x] 7.3 确认表单项、列表筛选、状态展示与字典 value 一致（字符串 `'1'`/`'0'`/`'2'`）

## 8. 联调与验证

- [x] 8.1 字典管理：类型 CRUD、级联删除、系统类型不可删、数据 CRUD 与分页
- [x] 8.2 运行时：`by-code/GENDER`、`by-code/STATUS` 仅返回启用项
- [x] 8.3 学生/角色/用户/菜单页下拉与状态展示正常
- [x] 8.4 非超管无法访问管理端点；登录用户可访问 by-code
