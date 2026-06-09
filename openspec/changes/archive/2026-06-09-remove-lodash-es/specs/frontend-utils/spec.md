## ADDED Requirements

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
