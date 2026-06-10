## Context

项目已有 `useTable`、`useDict` 等 Hook 与 CRUD 参考实现（`views/crud/`）。当前问题：

- `useTable.getTableData` 含 `console.log(res, 'res')` 调试残留
- `clearDictCache` 已实现但字典管理页未调用，导致 `useDict` 缓存 stale
- 6 个 FormDialog 组件重复 visible/isEdit/openAdd/openEdit/handleBeforeOk 模式
- user/role/crud 列表页存在 `handleSearch() { search() }` 无意义转发
- `main.ts` 全量引入 animate.css（~70KB），实际仅 `AppNoticeDrawer` 使用 `fadeOutRight`

约束：遵循 `agents/rules/frontend-standards.md`，Composition API + `<script setup>`，Gi 组件 kebab-case，改动范围最小化。

## Goals / Non-Goals

**Goals:**

- 清理 useTable 调试代码
- 字典 CRUD 成功后正确失效缓存
- 提供轻量 `useFormDialog` 并迁移标准 FormDialog（crud、dict 共 3 个）
- 列表页 `@search="search"` 直接绑定
- animate.css 改为按需，减小首屏 CSS

**Non-Goals:**

- 不迁移 menu/role/user 等复杂 FormDialog（含动态 rules、异步 options、特殊 open 参数）
- 不重构 `g-table-setting`、权限指令、Element Plus 全量 CSS
- 不修改后端字典 API

## Decisions

### 1. useFormDialog API 设计

采用**回调注入**而非泛型 class 封装：

```typescript
useFormDialog<TForm, TRow>({
  formRef,
  createEmptyForm,
  toFormData,
  submit: async ({ isEdit, id, data }) => { ... },
  onSuccess: () => emit('success'),
  titles: { add: '新增xxx', edit: '编辑xxx' },
})
```

**理由**：各 FormDialog 的 submit 逻辑（API 调用、payload 转换、ElMessage）差异大，回调比继承/base component 更灵活。**替代方案**：BaseFormDialog 组件 —  rejected，与 Gi 组件 slot/columns 模式耦合过深。

返回：`visible`、`isEdit`、`formData`、`dialogTitle`、`openAdd`、`openEdit`、`handleBeforeOk`，供模板与 `defineExpose` 使用。

### 2. FormDialog 迁移范围

| 文件 | 迁移 | 原因 |
|------|------|------|
| `crud/FormDialog.vue` | ✅ | 标准 CRUD |
| `DictTypeFormDialog.vue` | ✅ | 标准 CRUD |
| `DictDataFormDialog.vue` | ✅ | 标准 CRUD，submit 需 typeId |
| `user/FormDialog.vue` | ❌ | 动态 rules、roleOptions 异步加载 |
| `role/FormDialog.vue` | ❌ | 菜单树、复杂 openAdd |
| `menu/FormDialog.vue` | ❌ | openAdd(parent) 非标准签名 |

### 3. 字典缓存失效策略

在 FormDialog `@success` 与 DictTypePane 删除成功后调用 `clearDictCache(code)`：

- 类型变更：清除该 type 的 `code`
- 数据变更：从 `selectedType.code` 取 code
- 删除类型：清除被删 type 的 code；批量/不确定时 `clearDictCache()`

不在 `useDict.loadDict` 内加 TTL — 管理端变更频率低，显式失效更准确。

### 4. handleSearch 简化

模板 `@search="search"`，`handleReset` 保留（含字段清空 + `search()`）。`DictTypePane.handleSearch` 不改动（非 useTable，含 `loadTypes` 逻辑）。

### 5. animate.css 按需方案

**首选**：在 `AppNoticeDrawer/index.vue` 的 `<style>` 中写本地 `@keyframes fadeOutRight` + `.animate__*` 最小类（约 15 行），移除 `main.ts` 全局 import 及 `package.json` 的 `animate.css` 依赖。

**备选**：组件内 `import 'animate.css/source/fading_exits/fadeOutRight.css'` — 若本地 keyframes 视觉不一致再用。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| useFormDialog 过度抽象导致复杂 Dialog 难读 | 仅迁移 3 个标准 Dialog；复杂场景不强制 |
| clearDictCache 漏调导致 stale | 集中在 success 回调；删除类型在 DictTypePane 一并处理 |
| 本地 fadeOutRight 与 animate.css 视觉差异 | 对照原效果微调 duration/transform |
| submit 回调内 ElMessage 仍重复 | 可接受；各模块文案不同 |

## Migration Plan

1. 新增 `useFormDialog.ts`，从 `hooks/index.ts` 导出
2. 清理 useTable console.log
3. 迁移 3 个 FormDialog
4. 字典页接入 clearDictCache
5. 简化 crud/user/role 搜索绑定
6. animate.css 本地化 + 移除依赖
7. 运行 `pnpm typecheck` 与 `pnpm lint`

无数据库迁移；可逐 PR 合并，回滚为单文件 revert。

## Open Questions

- user/role FormDialog 是否在后续 change 中渐进迁移 — 本次不做
- 是否在 `frontend-standards.md` 补充 useFormDialog 约定 — 实现时顺手补充一行即可
