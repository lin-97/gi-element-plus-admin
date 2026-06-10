## ADDED Requirements

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
