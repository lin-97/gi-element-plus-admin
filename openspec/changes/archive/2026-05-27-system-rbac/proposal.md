## Why

当前项目仅有基于 `users.role` 单字符串的简易认证，缺少可运营的系统用户与角色管理能力；前端已预埋 `usePermissionStore`、`hasRole`/`hasPerm` 及菜单 `roles` 过滤，但未与后端数据打通。需要建设「系统管理」模块（用户管理 + 角色管理），支持多角色 RBAC、启用禁用、重置密码，为后续菜单权限分配与部门模块奠定基础。

## What Changes

- 新增 **角色管理** CRUD：角色 code 可配置（非固定枚举），系统内置 `role_admin` 超管角色
- 新增 **用户管理** CRUD：扩展手机、邮箱、头像（URL）、备注；多角色分配；`status` 启用/禁用；管理员手动重置密码；批量删除
- **BREAKING**：用户从单列 `role` 迁移为多对多 `user_role`；`userinfo`/登录响应改为返回 `roles[]`、`permissions[]`；废弃对外 `is_active`，统一 `status`（`'0'|'1'`）
- **BREAKING**：API 时间字段对外统一 `createTime`（camelCase），替代 `created_at`
- 认证与菜单：`/menu/routes` 按用户角色 code 交集过滤；超管 `role_admin` 拥有全部权限（`*:*:*`）
- 菜单 MOCK 增加父级 **系统管理**，子菜单：用户管理、角色管理
- 用户表单角色下拉：`GET /role/options` 返回全量启用角色
- 数据库预留 `deptId`，本期不做部门管理
- 角色分配菜单/权限树、头像上传、部门模块 — **不在本期**

## Capabilities

### New Capabilities

- `system-role`: 角色 CRUD、状态、系统角色保护、`/role/options` 下拉接口
- `system-user`: 用户 CRUD、多角色、status、createTime、重置密码、批量删除、列表字段
- `auth-rbac`: 登录/userinfo 返回 roles 与 permissions；permissionStore 灌数；菜单多角色过滤；超管守卫

### Modified Capabilities

- （无既有 openspec spec）

## Impact

- **后端**：`models` 新增 `Role`、`UserRole`；扩展 `User` 字段；`user_crud`/`role_crud`；`api/user.py`、`api/role.py`；改造 `auth.py`、`menu.py`、`deps.py`；`init_db` 种子与迁移
- **前端**：`apis/user.ts`、`apis/role.ts`、`apis/auth.ts`；`views/system/user/*`、`views/system/role/*`；`useUserStore` 接线 `usePermissionStore`；`menu.py` 对应路由组件
- **数据**：现有 `admin`/`user` 账号需迁移至 `role_admin` 及多角色关联
