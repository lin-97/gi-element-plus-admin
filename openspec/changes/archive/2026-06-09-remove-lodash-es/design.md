## Context

当前前端依赖情况：

| 库 | 状态 | 用途 |
|---|---|---|
| `lodash-es` | 已声明，**零引用** | 仅出现在 `vite.config.ts` manualChunks |
| `xe-utils` | 活跃使用 | `eachTree`、`mapTree`、`orderBy`、`filterSortTree` |
| `es-toolkit` | 已声明，业务代码未直接使用 | 可作为备选 |
| `JSON.parse(JSON.stringify())` | `useMenu` ×1、`useMixMenu` ×3 | 路由树深拷贝 |

菜单 hooks 的深拷贝目的是在 `computed` 中安全地变换路由树（过滤、展平），避免污染 `routeStore.routes` 原始数据。路由对象为纯 JSON 结构（path、meta、children），无函数或循环引用。

## Goals / Non-Goals

**Goals:**

- 完全移除 `lodash-es` 及 `@types/lodash-es` 依赖
- 提供单一、可复用的深拷贝工具函数
- 替换菜单 hooks 中所有 `JSON.parse(JSON.stringify())` 调用
- 保持菜单渲染、路由跳转行为与改动前一致

**Non-Goals:**

- 菜单逻辑重构（展平规则、Mix 布局拆分等）
- 菜单树 computed 缓存 / memo 优化
- 修改 `gi-component` 或 `element-plus` 间接引入的 lodash 传递依赖

## Decisions

### 1. 深拷贝实现选型：xe-utils `clone`

**选择**：`import { clone } from 'xe-utils'`，调用 `clone(data, true)` 做深拷贝。

**理由**：
- 项目已在菜单处理中大量使用 `xe-utils`，风格一致，无新增依赖
- `clone` API 简洁，对纯对象树性能优于 `JSON` 序列化方案
- 路由树为 plain object，不涉及 `Date`、`Map` 等特殊类型

**备选**：
- `es-toolkit` 的 `cloneDeep`：能力等价，但引入第二套工具风格，且当前业务未使用 es-toolkit
- 保留 `JSON.parse(JSON.stringify())`：性能差，规范上应禁止
- 引入 `lodash-es` `cloneDeep`：与本次移除目标矛盾

### 2. 工具函数封装：`deepClone` in `@/utils`

**选择**：在 `src/utils/index.ts` 导出 `deepClone<T>(data: T): T`，内部委托 `xe-utils` `clone`。

**理由**：
- 调用方不直接依赖第三方 API，后续换实现只需改一处
- 与现有 `filterSortTree`、`isExternal` 等同处 `@/utils`，符合目录约定

```typescript
import { clone } from 'xe-utils'

export function deepClone<T>(data: T): T {
  return clone(data, true) as T
}
```

### 3. 替换范围

仅替换以下 4 处：

| 文件 | 行上下文 |
|---|---|
| `hooks/useMenu.ts` | `menuList` computed 内 |
| `hooks/useMixMenu.ts` | `fullMenuList`、`topMenuList`、`sideMenuList` computed 内 |

不改动 `filterSortTree` 内部逻辑（其 `filterTree` 使用 `mapTree` 原地修改，调用方仍需先深拷贝）。

### 4. Vite manualChunks 调整

从 `utils` chunk 中移除 `'lodash-es'`，保留 `['axios', 'dayjs', 'xe-utils']`。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| `xe-utils` `clone` 对特殊类型行为与 JSON 方案不同 | 路由树仅为 plain object，无特殊类型；改动后手动验证三种布局菜单 |
| `gi-component` / `element-plus` 可能间接依赖 lodash | 本次只移除项目直接依赖；传递依赖由各自包管理，不影响构建 |
| `pnpm-lock.yaml` 需同步更新 | 执行 `pnpm install` 后 lockfile 自动刷新 |

## Migration Plan

1. 新增 `deepClone` 工具函数
2. 替换 hooks 中的深拷贝调用
3. 移除 `lodash-es` 依赖并更新 `vite.config.ts`
4. 运行 `pnpm install`、`pnpm typecheck`、`pnpm lint`
5. 手动验证：left / top / mix 三种布局下菜单展示、选中态、路由跳转

回滚：恢复 `package.json` 与 hooks 改动即可，无数据迁移。

## Open Questions

（无）
