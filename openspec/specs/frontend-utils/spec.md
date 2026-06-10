# frontend-utils Specification

## Purpose
TBD - created by archiving change remove-lodash-es. Update Purpose after archive.
## Requirements
### Requirement: 统一深拷贝工具函数

前端 SHALL 在 `@/utils` 提供 `deepClone<T>(data: T): T` 函数，基于 `xe-utils` 的 `clone` 实现深拷贝，供业务代码复用。

#### Scenario: 克隆路由树

- **WHEN** 调用方传入 `RouteRecordRaw[]` 路由树
- **THEN** 返回结构与原始数据相同但引用独立的深拷贝副本
- **AND** 修改副本不影响原始数据

#### Scenario: 禁止 JSON 序列化深拷贝

- **WHEN** 业务代码需要深拷贝纯对象/数组
- **THEN** 必须使用 `deepClone`，不得使用 `JSON.parse(JSON.stringify())`

### Requirement: 菜单 hooks 使用统一深拷贝

`useMenu` 与 `useMixMenu` SHALL 通过 `deepClone` 克隆 `routeStore.routes`，不得在 hooks 内直接使用 `JSON.parse(JSON.stringify())`。

#### Scenario: useMenu 菜单列表计算

- **WHEN** `routeStore.routes` 变化触发 `menuList` 重新计算
- **THEN** hooks 使用 `deepClone(routeStore.routes)` 获取副本后再执行过滤与展平
- **AND** `routeStore.routes` 原始数据不被修改

#### Scenario: useMixMenu 多级菜单计算

- **WHEN** `fullMenuList`、`topMenuList` 或 `sideMenuList` computed 重新计算
- **THEN** 各 computed 使用 `deepClone` 获取路由副本
- **AND** 菜单展示与路由跳转行为与改动前一致

### Requirement: 移除 lodash-es 直接依赖

前端项目 SHALL NOT 在 `package.json` 中声明 `lodash-es` 或 `@types/lodash-es` 作为直接依赖。

#### Scenario: 依赖清单检查

- **WHEN** 查看 `frontend/web/package.json` 的 dependencies 与 devDependencies
- **THEN** 不存在 `lodash-es` 与 `@types/lodash-es` 条目

#### Scenario: 构建分包配置

- **WHEN** 查看 `vite.config.ts` 的 `manualChunks.utils`
- **THEN** 不包含 `lodash-es`

### Requirement: useTable 无调试输出

`useTable` Hook SHALL NOT 包含 `console.log` 或其他调试输出语句。错误场景 MAY 使用 `console.error` 记录删除失败等异常。

#### Scenario: 列表加载无 console.log

- **WHEN** 调用 `useTable` 的 `getTableData` 成功返回数据
- **THEN** 控制台不出现 `useTable` 内的 `console.log` 输出

### Requirement: 列表页搜索事件直接绑定

使用 `useTable` 的 CRUD 列表页 SHALL 将 `gi-form` 的 `@search` 直接绑定为 `search` 方法，不得保留仅调用 `search()` 的无参 `handleSearch` 薄包装函数。

含字段重置逻辑的 `@reset` 处理函数（如 `handleReset`）SHALL 保留。

#### Scenario: crud 列表页搜索绑定

- **WHEN** 查看 `views/crud/index.vue` 模板中 `gi-form` 的 `@search` 绑定
- **THEN** 绑定值为 `search` 而非 `handleSearch`
- **AND** script 中不存在仅转发 `search()` 的 `handleSearch` 函数

#### Scenario: user/role 列表页搜索绑定

- **WHEN** 查看 `views/system/user/index.vue` 与 `views/system/role/index.vue`
- **THEN** `@search` 直接绑定 `search`
- **AND** 不存在无参 `handleSearch` 薄包装

### Requirement: animate.css 按需加载

前端 SHALL NOT 在 `main.ts` 全局引入 `animate.css/animate.min.css`。动画样式 MUST 在使用组件内按需引入，或使用 scoped 本地 `@keyframes` 实现等价效果。

#### Scenario: main.ts 无 animate.css 全局 import

- **WHEN** 查看 `src/main.ts`
- **THEN** 不存在 `import 'animate.css/animate.min.css'`

#### Scenario: AppNoticeDrawer 清除动画仍可用

- **WHEN** 用户在通知抽屉执行「全部清除」
- **THEN** 列表项仍播放淡出/滑出动画（通过组件内按需样式或本地 keyframes）
- **AND** 首屏不再加载完整 animate.css 包

