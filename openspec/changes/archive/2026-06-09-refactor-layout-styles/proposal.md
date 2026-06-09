## Why

路径 A（`refactor-layout-menu`）已完成菜单架构重构，但三种布局的 SCSS 仍大量重复，响应式断点在 7 个组件各自初始化，且部分组件存在 BEM 命名违规与死代码。路径 B 聚焦样式与规范一致性，在不动菜单逻辑的前提下降低维护成本、对齐 `frontend-standards.md`。

## What Changes

- 新增 `layouts/_shared.scss`：抽取 `__main`、`__content` 等共用布局样式，三个 layout 通过 `@use` 复用
- 新增 `hooks/useResponsive.ts`：统一 `isXs`、`isMobile` 等断点命名，替换布局相关组件中的重复 `useBreakpoints` 初始化
- 修正 BEM 命名：`AppHeaderActions` 的 `app-header__user` → `app-header-actions__user`；三个 layout 的 Block 改为 `default-layout`、`top-layout`、`mix-layout`
- 抽取水平菜单 `:deep` 共用样式（`app-header` 与 `mix-header`）
- 将重复的 `.el-button--primary.is-text` 提至全局样式（`styles/index.scss`），删除组件内重复定义
- 清理 `AppHeader` 中已迁移的 `&__user` 死代码

## Capabilities

### New Capabilities

- `layout-styles`: 布局样式复用、响应式 Hook、BEM 规范与全局样式抽取

### Modified Capabilities

（无——纯样式与规范整理，不改变业务行为）

## Impact

- **样式**：`layouts/_shared.scss`（新增）、`layouts/default|top|mix/index.vue`、`styles/index.scss`
- **Hooks**：`hooks/useResponsive.ts`（新增）、`hooks/index.ts`
- **组件**：`AppHeader`、`AppHeaderActions`、`AppMenuToggle`、`layouts/mix/index.vue`
- **规范**：`agents/rules/frontend-standards.md`（可选补充 `useResponsive` 约定）
- **行为**：视觉与交互不变，仅 class 名与样式组织方式调整
