## 1. 深拷贝工具

- [x] 1.1 在 `src/utils/index.ts` 新增 `deepClone<T>(data: T): T`，内部使用 `xe-utils` 的 `clone(data, true)`
- [x] 1.2 在 `agents/rules/frontend-standards.md` 禁止事项中补充：禁止 `JSON.parse(JSON.stringify())` 做深拷贝，统一使用 `deepClone`

## 2. 替换菜单 hooks 深拷贝

- [x] 2.1 将 `hooks/useMenu.ts` 中 `JSON.parse(JSON.stringify(routeStore.routes))` 替换为 `deepClone(routeStore.routes)`
- [x] 2.2 将 `hooks/useMixMenu.ts` 中 3 处 `JSON.parse(JSON.stringify(...))` 替换为 `deepClone(...)`

## 3. 移除 lodash-es 依赖

- [x] 3.1 从 `package.json` 移除 `lodash-es`（dependencies）与 `@types/lodash-es`（devDependencies）
- [x] 3.2 从 `vite.config.ts` 的 `manualChunks.utils` 中移除 `'lodash-es'`
- [x] 3.3 在 `frontend/web` 目录执行 `pnpm install` 更新 lockfile

## 4. 验证

- [x] 4.1 运行 `pnpm typecheck` 与 `pnpm lint` 确保无报错
- [x] 4.2 手动验证 left / top / mix 三种布局：菜单展示、选中高亮、路由跳转正常
