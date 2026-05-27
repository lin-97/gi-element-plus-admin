## Context

GI Element Plus Admin 当前状态：

- 用户/角色/菜单已库表化；系统管理页遵循 `GiPageLayout` + `useTable` + `FormDialog` 模式
- 业务下拉选项硬编码：`GENDER_OPTIONS`（`apis/student.ts`）、`STATUS_OPTIONS`（`apis/role.ts`）
- 无左右分栏主从页先例；菜单管理为整页树表（不用 `useTable`）
- 管理端 API 统一 `require_super_admin`；列表格式对齐 `PageResult`

本 change 新增字典类型与字典数据，提供主从管理 UI、运行时按 `code` 查询，并将 `GENDER`、`STATUS` seed 入库。

## Goals / Non-Goals

**Goals:**

- `sys_dict_type`、`sys_dict_data` 表；删除类型时 **CASCADE** 删除数据
- 字典管理主从页：左栏类型列表（搜索 + 状态筛选，**无分页**）；右栏数据 `useTable` 分页
- 类型 `code`：大写英文、唯一、**创建后不可改**；数据 `value`：字符串、同类型内唯一
- 内置字典 `GENDER`、`STATUS`：`is_system=true`，不可删除
- 超管 CRUD + 菜单 seed（`system:dict:*` 按钮权限）
- `GET /api/dict/data/by-code/{code}`：任意登录用户可读，仅 `status='1'`，按 `sort` 排序
- 前端 `useDict(code)` 或等价封装；替换 `GENDER_OPTIONS`、`STATUS_OPTIONS` 消费点

**Non-Goals:**

- 字典类型树形结构（一期扁平列表）
- 字典缓存失效的分布式通知
- 除 `GENDER`、`STATUS` 外批量迁移其它硬编码选项
- 字典数据导入/导出

## Decisions

### 1. 数据模型

```text
sys_dict_type: id, name, code (unique), status, sort, remark, is_system, timestamps
sys_dict_data: id, type_id (FK CASCADE), label, value (string), status, sort, remark, timestamps
UNIQUE(type_id, value)
```

- 删类型 → ORM/DB `ondelete=CASCADE` 删全部数据
- `is_system=true` 的类型：拒绝 `POST /dict/type/delete`

**备选**：软删除 — 已否决，与现有 role/menu 的 `status` 字段模式一致，删除用物理删 + 级联。

### 2. API 分层

| 端点 | 权限 | 说明 |
|------|------|------|
| `GET /dict/type/list` | 超管 | 查询参数：`name?`, `status?`；全量列表 |
| `POST/PUT /dict/type` | 超管 | 创建校验 code 格式；更新禁止改 code |
| `POST /dict/type/delete` | 超管 | `{ ids }`；跳过/拒绝 system 类型 |
| `GET /dict/data/list` | 超管 | `typeId` 必填；`label?`, `status?`；分页 |
| `POST/PUT /dict/data` | 超管 | `typeId` 须存在；value 同类型唯一 |
| `POST /dict/data/delete` | 超管 | `{ ids }` |
| `PUT /dict/data/{id}/status` | 超管 | 行内开关（与 role 一致） |
| `GET /dict/data/by-code/{code}` | 登录用户 | 仅启用项；code 不存在返回空数组 |

**备选**：运行时接口也限超管 — 已否决，业务表单需普通用户可读字典。

### 3. code 校验

- 正则：`^[A-Z][A-Z0-9_]*$`（至少 1 字符，首字符大写字母）
- 创建时 normalize 为大写；更新 body 忽略 `code` 字段

### 4. 前端主从布局

- 单路由 `views/system/dict/index.vue`；`GiPageLayout` 内 flex 左右栏（左 ~300px）
- 左：自管 `ref` 列表 + `selectedTypeId`；右：`useTable` + `DictDataFormDialog`
- 类型 CRUD：`DictTypeFormDialog`；左栏工具栏：搜索、新增/编辑/删除、启用/禁用筛选
- 未选类型时右栏空状态或禁用操作
- 类型禁用后：右栏可查看已有数据；**禁止新增**数据（前端禁用 + 后端校验 `type.status='1'`）

**备选**：左右各一个路由 — 已否决，交互割裂。

### 5. 运行时消费

- `hooks/useDict.ts`：`code` → `ref<DictOption[]>`，登录后请求并缓存（内存 Map，可选按 code 去重）
- 替换点：`crud` 性别、`role/user/menu` 状态筛选与表单项
- 保留类型导出（如 `GenderValue`）与字典 `value` 对齐

### 6. Seed

| code | name | is_system | 数据 |
|------|------|-----------|------|
| GENDER | 性别 | true | 男/1, 女/2 |
| STATUS | 状态 | true | 启用/1, 禁用/0 |

- `dict_migration.py` 在 `lifespan` 调用，幂等插入
- `menu_migration` 追加 `system:dict` 菜单与按钮

### 7. 菜单与权限

- 路径 `/system/dict/index`，组件 `system/dict/index`
- 按钮：`system:dict:add`, `edit`, `delete`（类型与数据共用或分 type/data 前缀 — 实现采用 `system:dict:type:*` 与 `system:dict:data:*` 更清晰）

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 改字典 value 导致历史数据含义变化 | 一期文档约定 value 稳定；UI 提示谨慎修改 |
| useDict 请求风暴 | 按 code 缓存；页面 mount 批量预取常用 code |
| 删类型误操作 | 级联删前确认框注明数据条数 |
| 左栏无分页类型过多 | 一期可接受；后续加虚拟滚动 |
| code 与前端常量不一致 | seed 与迁移在同一 PR 联调 |

## Migration Plan

1. 新增表与 migration seed（GENDER、STATUS）
2. 部署后端 API
3. 部署字典管理页 + menu seed
4. 前端切换 `useDict`；移除或废弃 `GENDER_OPTIONS`/`STATUS_OPTIONS` 常量导出
5. 验证：字典管理 CRUD、学生/用户/角色/菜单页下拉正常

**回滚**：DB 备份；前端可临时恢复硬编码常量。

## Open Questions

- （无）探索阶段已确认：一期含运行时 API + seed + 级联删 + 系统类型保护。
