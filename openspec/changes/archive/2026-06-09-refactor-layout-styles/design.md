## Context

路径 A 后，三个 layout 仍各自维护几乎相同的 SCSS：

| 重复内容 | 出现位置 |
|---------|---------|
| `.layout` / `__main` / `__content` | default、top、mix |
| `:deep(.el-menu--horizontal)` | AppHeader、MixLayout |
| `useBreakpoints(breakpointsTailwind)` | 布局区 6+ 组件 |
| `.el-button--primary.is-text` | AppHeader、AppHeaderActions |

BEM 问题：
- `AppHeaderActions` 使用 `app-header__user`（错误 Block）
- 三个 layout 共用泛化 Block 名 `layout`

## Goals / Non-Goals

**Goals:**

- 布局共用样式单点维护
- 布局区组件统一使用 `useResponsive()`
- BEM 命名符合 `frontend-standards.md`
- 删除死代码与重复全局样式片段

**Non-Goals:**

- 菜单逻辑改动（路径 A 范围）
- `GTableSetting` 等非布局组件的断点迁移（可后续顺手改，本次不强制）
- 重构 `mix-sidebar` 滚动条 `!important` 覆盖策略
- 修改主题色、间距等视觉设计

## Decisions

### 1. 共享样式：`layouts/_shared.scss`

使用 SCSS mixin 而非全局 class，避免 scoped 穿透问题：

```scss
// layouts/_shared.scss
@mixin layout-shell {
  display: flex;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--el-fill-color-light);
}

@mixin layout-main { ... }
@mixin layout-content { ... }
@mixin horizontal-menu { ... }
```

各 layout 在 scoped 样式中：

```scss
@use '../shared' as *;

.default-layout {
  @include layout-shell;
  // layout 特有：横向 flex
}
```

### 2. Layout Block 重命名

| 原 Block | 新 Block |
|---------|---------|
| `.layout` (default) | `.default-layout` |
| `.layout` (top) | `.top-layout` |
| `.layout` (mix) | `.mix-layout` |

Element 名保持 `__main`、`__content`、`__body`（mix 特有）不变，挂在各自 Block 下。

### 3. `useResponsive` Hook

```typescript
// hooks/useResponsive.ts
export function useResponsive() {
  const bp = useBreakpoints(breakpointsTailwind)
  return {
    isXs: bp.smaller('sm'),    // < 640px
    isMobile: bp.smaller('md'), // < 768px
  }
}
```

迁移映射：
- `isXsScreen` / `smaller('sm')` → `isXs`
- `isMdScreen` / `isMobile` / `smaller('md')` → `isMobile`

迁移范围（本次）：`layouts/default`、`layouts/mix`、`AppHeader`、`AppHeaderActions`、`AppMenuToggle`。

### 4. 全局按钮文字色

在 `styles/index.scss` 追加（与现有 `.g-square-button` 并列）：

```scss
.el-button--primary.is-text {
  --el-button-text-color: var(--el-text-color-primary);
}
```

从 `AppHeader`、`AppHeaderActions` 的 scoped 样式中删除。

### 5. AppHeaderActions BEM 修正

```
app-header__user      → app-header-actions__user
app-header__user-name → app-header-actions__user-name
```

同步更新 `<template>` 与 `<style>`。

### 6. AppHeader 死代码清理

删除已无模板引用的 `&__user` / `&__user-name` 样式块。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| class 重命名影响外部自定义样式 | 项目内无第三方依赖这些 class；全局搜索确认 |
| mixin 增加间接层 | 仅 3 个 layout 使用，收益大于成本 |
| `isMdScreen` 改名为 `isMobile` 语义变化 | top 模式原 `isMdScreen` 即 md 断点，与 `isMobile` 一致 |

## Migration Plan

1. 新增 `_shared.scss` 与 `useResponsive`
2. 逐 layout 迁移样式与 class 名
3. 迁移布局相关组件断点
4. BEM 修正 + 全局样式抽取 + 死代码清理
5. 视觉回归：三种布局桌面/移动端截图对比

## Open Questions

（无）
