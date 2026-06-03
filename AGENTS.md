# AI 编码助手规范（GI Element Plus Admin）

本仓库采用 **工具无关** 的 `agents/` 目录存放开发规范与技能，供 Cursor、OpenCode、Codex 等 AI 编码助手共用。

## 通用原则

- 始终使用**简体中文**与用户沟通
- 未经用户明确要求，**不要**创建说明文档、执行 git commit / push
- 改动范围最小化，优先复用项目已有抽象

## 项目结构

| 目录 | 说明 |
|------|------|
| `frontend/web/` | Vue 3 前端，路径别名 `@/` → `src/` |
| `backend/` | FastAPI 后端 |
| `agents/` | AI 通用规范（rules）与技能（skills） |

## 规则（Rules）

编写代码前，按工作目录读取对应规则并**严格遵循全部条款**：

| 规则 | 路径 | 何时加载 |
|------|------|----------|
| 前端规范 | [`agents/rules/frontend-standards.md`](agents/rules/frontend-standards.md) | 修改 `frontend/web/**` |
| Gi 组件规范 | [`agents/rules/gi-component-vue.md`](agents/rules/gi-component-vue.md) | 修改 `frontend/web/**/*.vue` |
| 后端规范 | [`agents/rules/backend-standards.md`](agents/rules/backend-standards.md) | 修改 `backend/**` |

## 技能（Skills）

任务匹配触发词时，读取对应 skill 并按步骤执行：

| Skill | 路径 | 触发场景 |
|-------|------|----------|
| 表格/CRUD 页 | [`agents/skills/table-page/SKILL.md`](agents/skills/table-page/SKILL.md) | 新建列表页、表格页、CRUD、FormDialog |
| Git 提交 | [`agents/skills/git-commit/SKILL.md`](agents/skills/git-commit/SKILL.md) | 提交代码、git commit、push（**须用户明确要求**） |

## 参考实现

- 前端 CRUD 列表页：`frontend/web/src/views/crud/index.vue`
- 前端表单弹窗：`frontend/web/src/views/crud/FormDialog.vue`
- 前端 API 模板：`frontend/web/src/apis/student.ts`
- 后端 API 模板：`backend/app/api/student.py`

## 各工具接入方式

详见 [`agents/README.md`](agents/README.md)。规范与技能均以 `agents/` 为唯一来源，根目录 `AGENTS.md` 为统一入口。
