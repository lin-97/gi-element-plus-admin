## Why

前端核心 Hook 与表单弹窗存在调试残留、字典缓存不失效、CRUD 样板代码重复、以及 animate.css 全量引入等问题，增加维护成本并影响运行时正确性与包体积。本次在既有规范框架内做 targeted 优化，不改变对外业务行为。

## What Changes

- 移除 `useTable` 中的 `console.log` 调试代码
- 字典管理增删改成功后调用 `clearDictCache`，使 `useDict` 缓存与后端数据一致
- 新增 `useFormDialog` composable，抽象 FormDialog 共有的 visible / isEdit / openAdd / openEdit / handleBeforeOk 状态机
- 将 CRUD 列表页中 `handleSearch() { search() }` 薄包装改为模板直接绑定 `search`（保留含业务逻辑的 `handleReset`）
- 移除 `main.ts` 对 `animate.css` 全量 CSS 的全局引入，改为在唯一使用处按需加载或本地 keyframes

## Capabilities

### New Capabilities

- `use-form-dialog`: 表单弹窗 composable，统一新增/编辑对话框的状态管理与提交流程

### Modified Capabilities

- `frontend-utils`: 补充 useTable 无调试输出、列表页搜索事件绑定、animate.css 按需加载等前端工具层要求
- `system-dict`: 补充字典变更后前端缓存失效要求

## Impact

- **Hook**：`src/hooks/useTable.ts`（清理）、新增 `src/hooks/useFormDialog.ts`
- **字典**：`src/views/system/dict/` 相关 FormDialog 与 index 成功回调
- **列表页**：`src/views/crud/index.vue`、`system/user/index.vue`、`system/role/index.vue`（搜索绑定简化）
- **FormDialog**：`crud/FormDialog.vue`、`system/dict/DictTypeFormDialog.vue`、`DictDataFormDialog.vue` 优先迁移；user/role/menu 等复杂弹窗视情况迁移或部分复用
- **样式/依赖**：`src/main.ts`、`src/components/AppNoticeDrawer/index.vue`；若完全本地化动画可考虑移除 `animate.css` 依赖
- **规范**：`agents/rules/frontend-standards.md` 可选补充 `useFormDialog` 与搜索绑定约定
