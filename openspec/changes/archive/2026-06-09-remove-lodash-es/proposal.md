## Why

`lodash-es` 已列入 `package.json` 与 Vite `manualChunks`，但业务代码中无任何引用，属于冗余依赖，增加安装体积与维护成本。与此同时，菜单 hooks（`useMenu`、`useMixMenu`）使用 `JSON.parse(JSON.stringify())` 做深拷贝，性能较差且无法处理函数、循环引用等边界情况。项目已依赖 `xe-utils`（菜单树处理）与 `es-toolkit`，应统一深拷贝方案并移除 `lodash-es`。

## What Changes

- 从 `package.json` 移除 `lodash-es` 与 `@types/lodash-es`
- 从 `vite.config.ts` 的 `manualChunks.utils` 中移除 `lodash-es`
- 新增 `@/utils/clone.ts`（或等价工具函数），封装深拷贝能力
- 将 `useMenu.ts`、`useMixMenu.ts` 中的 `JSON.parse(JSON.stringify())` 替换为统一深拷贝工具
- 在 `agents/rules/frontend-standards.md` 补充深拷贝约定（禁止 `JSON.parse(JSON.stringify())`，统一使用项目工具）

## Capabilities

### New Capabilities

- `frontend-utils`: 前端工具层深拷贝规范与菜单路由克隆实现

### Modified Capabilities

（无——本次为依赖清理与实现替换，不改变对外业务行为）

## Impact

- **依赖**：`frontend/web/package.json`、`pnpm-lock.yaml`（移除 lodash-es 相关条目）
- **构建**：`frontend/web/vite.config.ts`（manualChunks 调整）
- **源码**：`src/hooks/useMenu.ts`、`src/hooks/useMixMenu.ts`、`src/utils/`（新增 clone 工具）
- **规范**：`agents/rules/frontend-standards.md`（可选补充禁止事项）
- **行为**：菜单展平、过滤、排序逻辑不变，用户无感知
