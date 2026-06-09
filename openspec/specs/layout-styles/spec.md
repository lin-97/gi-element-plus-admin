# layout-styles Specification

## Purpose
TBD - created by archiving change refactor-layout-styles. Update Purpose after archive.
## Requirements
### Requirement: 布局共用样式

三个布局组件 SHALL 通过 `layouts/_shared.scss` 复用共用的 shell、main、content 及水平菜单样式 mixin，不得在各 layout 中重复定义相同规则。

#### Scenario: default 布局引用共享 mixin

- **WHEN** 查看 `layouts/default/index.vue` 的样式
- **THEN** 通过 `@use '../shared'` 引入共用 mixin
- **AND** 不包含与 `_shared.scss` 重复的 `__main` / `__content` 规则

#### Scenario: 水平菜单样式复用

- **WHEN** `AppHeader` 与 `MixLayout` 渲染水平 `el-menu`
- **THEN** 两者使用同一 horizontal-menu mixin
- **AND** 菜单高度与项高度表现一致

### Requirement: 统一响应式 Hook

布局相关组件 SHALL 使用 `useResponsive()` 获取断点状态，不得各自初始化 `useBreakpoints(breakpointsTailwind)`。

#### Scenario: 布局组件使用 useResponsive

- **WHEN** `AppHeader`、`AppMenuToggle`、`DefaultLayout`、`MixLayout` 需要判断移动端
- **THEN** 调用 `useResponsive()` 的 `isMobile` 或 `isXs`
- **AND** 断点阈值与 Tailwind 默认断点一致（sm: 640px，md: 768px）

### Requirement: 布局 BEM Block 命名

各布局组件 SHALL 使用语义化 Block 名：`default-layout`、`top-layout`、`mix-layout`，不得三个 layout 共用泛化 Block 名 `layout`。

#### Scenario: default 布局 Block 名

- **WHEN** 查看 `DefaultLayout` 模板根元素 class
- **THEN** Block 名为 `default-layout` 而非 `layout`

### Requirement: 组件 BEM 命名合规

`AppHeaderActions` 的自定义 class SHALL 以 `app-header-actions` 为 Block，不得使用 `app-header__*` 作为本组件元素名。

#### Scenario: 用户下拉区域 class

- **WHEN** 查看 `AppHeaderActions` 模板中用户下拉触发区域
- **THEN** 使用 `app-header-actions__user` 与 `app-header-actions__user-name`

### Requirement: 全局工具栏按钮样式

重复的 `.el-button--primary.is-text` 文字色覆盖 SHALL 定义在 `styles/index.scss`，布局/header 相关组件不得 scoped 重复定义。

#### Scenario: 组件内无重复定义

- **WHEN** 查看 `AppHeader` 与 `AppHeaderActions` 的 scoped 样式
- **THEN** 不存在 `.el-button--primary.is-text` 规则
- **AND** 全局样式文件中存在该规则

