# Git 提交示例

## 示例 1：仅前端登录页

**变更**：`frontend/web/src/views/login/**`

```powershell
git add frontend/web/src/views/login/
git commit -m "feat: 未来科技风登录页" -m "玻璃拟态卡片、CSS 粒子背景与发光边框，拆分 composable 与场景组件"
```

## 示例 2：前后端联调（用户管理）

**变更**：`backend/app/api/` + `frontend/web/src/views/system/user/`

```powershell
git add backend/app/api/user.py backend/app/crud/user_crud.py frontend/web/src/views/system/user/ frontend/web/src/apis/user.ts
git commit -m "feat: 用户管理 CRUD 与后端接口" -m "列表分页、表单校验、角色关联"
```

## 示例 3：AI 规范与 skills

```powershell
git add agents/ AGENTS.md
git commit -m "chore: 新增 agents 通用规范与 git-commit skill"
```

## 示例 4：修复 bug

```powershell
git add frontend/web/src/router/guard.ts frontend/web/src/router/route-load-state.ts
git commit -m "fix: 登录后动态路由重复加载" -m "使用 route-load-state 标记避免二次 addRoute"
```

## 反例（不要这样做）

```powershell
# ❌ 未获用户同意就提交
git add -A; git commit -m "update"

# ❌ 提交敏感文件
git add backend/env/.env.dev

# ❌ 提交构建缓存
git add frontend/web/node_modules/.vite/

# ❌ 失败后 amend
git commit --amend  # hook 刚失败时禁止
```

## 提交说明对照

| 变更性质 | 推荐 type | 示例 subject |
|----------|-----------|--------------|
| 新列表页 | feat | feat: 菜单管理列表页 |
| 修接口 404 | fix | fix: 角色菜单树接口路径 |
| 抽 hook | refactor | refactor: 抽取 useLogin composable |
| 仅改 SCSS | style | style: 登录页科技风背景动效 |
| 加 skill | chore | chore: 新增 git-commit skill |
