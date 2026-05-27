## 1. 数据库与模型

- [x] 1.1 新增 `Role`、`UserRole` 模型；扩展 `User`（phone、email、avatar、remark、dept_id、status）；移除或迁移单列 `role`、`is_active`
- [x] 1.2 编写迁移/初始化：`role_admin` 系统角色；`admin` 用户绑定 `role_admin`；`status` 从 `is_active` 映射
- [x] 1.3 API 序列化层统一输出 `createTime`（camelCase）与 `status`（`'0'|'1'`）

## 2. 后端 — 角色

- [x] 2.1 实现 `role_crud`（列表、CRUD、批量删除、options 仅启用角色、系统角色保护）
- [x] 2.2 实现 `schemas`（RoleCreate/Update/Response、BatchDelete）
- [x] 2.3 实现 `api/role.py` 并注册路由；写操作 `require_super_admin`
- [x] 2.4 注册 `POST /api/role/delete` 与 `GET /api/role/options`

## 3. 后端 — 用户

- [x] 3.1 扩展 `user_crud`（分页列表、CRUD、roleIds 关联、批量删除、安全规则）
- [x] 3.2 实现 `api/user.py`：`list`、`/{id}`、CRUD、`POST /delete`、`PUT /{id}/password`、`PUT /{id}/status`
- [x] 3.3 列表/详情聚合角色名称或 codes；密码永不回显

## 4. 后端 — 认证与菜单

- [x] 4.1 改造 `deps.py`：`is_super_admin` 基于 `role_admin`；替换 `role == "admin"`
- [x] 4.2 改造 `auth.py`：userinfo/login 返回 `roles[]`、`permissions[]`；禁用用户拒绝登录
- [x] 4.3 改造 `menu.py`：多角色交集过滤；新增系统管理 → 用户管理、角色管理 MOCK 路由
- [x] 4.4 `main.py` 注册 user、role 路由

## 5. 前端 — API 与 Store

- [x] 5.1 新建 `apis/role.ts`（含 `getRoleOptionsApi`）；完善 `apis/user.ts`（类型、批量删除、resetPassword、updateStatus）
- [x] 5.2 更新 `apis/auth.ts`：`UserInfo` 含 `roles`、`permissions`；登录后调用 `permissionStore.setRoles/setPermissions`
- [x] 5.3 确认 `useTable` 的 `deleteAPI` 传入 `ids[]`

## 6. 前端 — 角色管理页

- [x] 6.1 创建 `views/system/role/index.vue`（GiPageLayout + GiForm + GiTable + useTable）
- [x] 6.2 创建 `views/system/role/FormDialog.vue`（code、name、status、sort、remark）

## 7. 前端 — 用户管理页

- [x] 7.1 创建 `views/system/user/index.vue`（列：头像、用户名、手机、邮箱、角色 tags、status、createTime、备注、操作）
- [x] 7.2 创建 `views/system/user/FormDialog.vue`（多选角色来自 options、头像 URL、status 等）
- [x] 7.3 创建 `ResetPasswordDialog.vue`（新密码 + 确认密码）
- [x] 7.4 行内启用/禁用调用 status API；批量删除

## 8. 联调与验证

- [x] 8.1 使用 admin 登录：侧边栏出现系统管理；用户/角色 CRUD 全流程
- [x] 8.2 验证多角色用户菜单过滤、禁用用户无法登录、不可删自己/系统角色
- [x] 8.3 验证 `createTime`、`status` 字段在列表与接口中一致

