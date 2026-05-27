## Context

GI Element Plus Admin 当前具备：

- 后端 `User` 模型（`username`、`password`、`nickname`、单列 `role`、`is_active`、`created_at`）
- 认证 API（login、userinfo、logout）与 `require_admin`（`role == "admin"`）
- 前端 `usePermissionStore`（`roles`、`permissions`）、`SUPER_ADMIN_ROLE = 'role_admin'`、`hasRole`/`hasPerm`，但登录后未灌数
- 菜单 `MOCK_ASYNC_ROUTES` 仅含学生管理；过滤逻辑使用用户**单个** `role` 字符串
- 学生 CRUD 为前后端参考模板（`useTable`、批量 `POST /delete`）

本 change 在「系统管理」父菜单下新增用户管理与角色管理，建立多角色 RBAC，并与现有权限工具链对齐。

## Goals / Non-Goals

**Goals:**

- 角色 CRUD + `/role/options`（全量启用角色，供用户表单多选）
- 用户 CRUD：手机、邮箱、头像（URL）、备注、`status`、`createTime`、多角色、重置密码、启用/禁用、批量删除
- 认证返回 `roles[]`、`permissions[]`；`usePermissionStore` 在 login/fetchUserInfo 后写入
- 菜单按用户角色 code **交集**过滤；`role_admin` 超管跳过过滤并拥有 `*:*:*`
- 字段契约：`status` 为 `'0'|'1'`（1 启用、0 禁用）；对外时间字段 `createTime`（ISO 8601）
- 菜单结构：系统管理 → 用户管理、角色管理
- `deptId` 数据库预留，本期不展示

**Non-Goals:**

- 角色分配菜单/权限树（菜单仍 MOCK，手工配置 `roles`）
- 部门管理模块
- 头像文件上传
- 改造学生模块的 `created_at` 命名

## Decisions

### 1. 数据模型：多对多角色

- 新增 `sys_role`（`code` 唯一、`name`、`status`、`sort`、`remark`、`is_system`）
- 新增 `sys_user_role`（`user_id`、`role_id`，联合唯一）
- 扩展 `users`：`phone`、`email`、`avatar`、`remark`、`dept_id`（nullable）；`is_active` → `status` CHAR(1)；API 层将 DB `created_at` 序列化为 `createTime`
- 废弃对外 `users.role` 单列（迁移后删除或保留只读一版兼容，优先删除）

**理由**：满足多角色与可配置角色；与前端 `roles: string[]` 一致。

### 2. 超管约定

- 系统角色 `role_admin`（`is_system=true`，不可删、不可改 code）
- 前端 `SUPER_ADMIN_ROLE`、后端种子与 `init_db` 统一为 `role_admin`
- 拥有该角色的用户：`permissions` 含 `*:*:*`；菜单不过滤；写接口等同超管

**备选**：保留 `role == "admin"` 字符串 — 已否决，与前端常量不一致。

### 3. status 与 createTime

- `status`: `'1'` 启用，`'0'` 禁用（与菜单 `AsyncRouteItem.status` 一致）
- 禁用用户不可登录；禁用角色不再计入 userinfo 的 `roles`（即使用户关联仍存在，也不生效）
- API JSON 统一 camelCase：`createTime`；DB 列可仍为 `created_at`

### 4. API 设计

| 模块 | 路径 | 说明 |
|------|------|------|
| 角色 | `GET/POST /api/role/list` 等 | 标准 CRUD + `POST /api/role/delete` |
| 角色 | `GET /api/role/options` | `{ id, code, name }[]`，仅 `status='1'` |
| 用户 | `GET /api/user/list` | 分页，筛选项含 username、phone、status |
| 用户 | `PUT /api/user/{id}/password` | body `{ password }`，仅超管 |
| 用户 | `PUT /api/user/{id}/status` | body `{ status }` |
| 用户 | `POST /api/user/delete` | `{ ids }` 批量删除 |

列表响应格式与现有 `PageResult` 一致：`{ list, total, page, size }`。

### 5. 权限聚合（一期）

- 用户 `permissions`：各角色 code 映射到预置 permission 列表（一期可硬编码字典），超管直接 `['*:*:*']`
- 菜单项 `permission` 字段保留，按钮级 `v-hasPerm` 可用；角色↔权限配置 UI 二期再做

### 6. 前端结构

- `views/system/user/index.vue` + `FormDialog.vue`
- `views/system/role/index.vue` + `FormDialog.vue`
- `apis/user.ts`、`apis/role.ts`；`deleteUserApi(ids: string[])` 对齐 `useTable`
- 重置密码：独立 `ResetPasswordDialog`，新密码 + 确认密码
- 用户列表：头像 `el-avatar`、角色 `el-tag` 多个、状态列、操作含重置密码/切换 status

### 7. 安全规则

- 不能删除或禁用当前登录用户
- 不能删除 `is_system` 角色；不能删除仍有关联用户的角色
- 至少保留一个拥有 `role_admin` 的启用用户

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| **BREAKING** 登录响应结构变化 | 同步改 `auth.ts` 类型与 `useUserStore`；移除对单一 `role` 的依赖 |
| 菜单 MOCK 与角色 code 手工对齐 | 文档约定；二期菜单入库 + 角色授权 UI |
| 禁用角色后权限变更需重新登录才刷新菜单 | userinfo 时计算；可选登出提示 |
| SQLite/现有库无迁移框架 | 提供 `init_db` 升级脚本或 Alembic 风格一次性迁移函数 |

## Migration Plan

1. `create_all` 或迁移脚本：新增表与列；`status` 从 `is_active` 映射（True→'1'，False→'0'）
2. 插入 `role_admin`、`role_user`（可选）系统角色；`admin` 用户关联 `role_admin`
3. 删除或忽略 `users.role` 单列
4. 部署后端后部署前端；旧 token 仍有效，userinfo 返回新结构

**回滚**：保留 DB 备份；前端可暂时兼容缺失 `roles` 时默认 `[]`。

## Open Questions

- （已闭合）重置密码：管理员手动输入
- （已闭合）头像：URL
- （已闭合）角色下拉：`/role/options` 全量启用
