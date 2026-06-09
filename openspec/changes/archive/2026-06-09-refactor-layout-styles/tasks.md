## 1. 基础设施

- [x] 1.1 新增 `layouts/_shared.scss`：定义 `layout-shell`、`layout-main`、`layout-content`、`horizontal-menu` mixin
- [x] 1.2 新增 `hooks/useResponsive.ts`，导出 `isXs`、`isMobile`
- [x] 1.3 在 `hooks/index.ts` 导出 `useResponsive`

## 2. 布局样式迁移

- [x] 2.1 迁移 `layouts/default/index.vue`：Block 改为 `default-layout`，使用共享 mixin
- [x] 2.2 迁移 `layouts/top/index.vue`：Block 改为 `top-layout`，使用共享 mixin
- [x] 2.3 迁移 `layouts/mix/index.vue`：Block 改为 `mix-layout`，使用共享 mixin 与 horizontal-menu mixin

## 3. 响应式 Hook 迁移

- [x] 3.1 `layouts/default/index.vue`、`layouts/mix/index.vue` 改用 `useResponsive`
- [x] 3.2 `AppHeader`、`AppHeaderActions`、`AppMenuToggle` 改用 `useResponsive`

## 4. BEM 与样式清理

- [x] 4.1 修正 `AppHeaderActions` BEM：`app-header-actions__user` / `__user-name`
- [x] 4.2 将 `.el-button--primary.is-text` 移至 `styles/index.scss`，删除组件内重复
- [x] 4.3 删除 `AppHeader` 中无用的 `&__user` 死代码

## 5. 验证

- [x] 5.1 对变更文件运行 ESLint
- [x] 5.2 手动确认三种布局桌面/移动端视觉无变化
