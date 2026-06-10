## ADDED Requirements

### Requirement: 字典变更后前端缓存失效

当超级管理员在字典管理页成功创建、更新或删除字典类型或字典数据后，前端 SHALL 调用 `clearDictCache(code)` 使对应字典 code 的 `useDict` 内存缓存失效。删除字典类型时 MUST 清除该类型 `code` 的缓存；若无法确定 code，SHALL 调用无参 `clearDictCache()` 清空全部缓存。

#### Scenario: 编辑字典类型后缓存失效

- **WHEN** 超级管理员在 `DictTypeFormDialog` 成功更新字典类型且该类型 `code` 为 `ORDER_STATUS`
- **THEN** 前端调用 `clearDictCache('ORDER_STATUS')`
- **AND** 其他页面下次 `useDict(['ORDER_STATUS'])` 时重新请求 API

#### Scenario: 增删字典数据后缓存失效

- **WHEN** 超级管理员在 `DictDataFormDialog` 成功新增或更新字典数据
- **THEN** 前端根据当前选中字典类型的 `code` 调用 `clearDictCache(code)`

#### Scenario: 删除字典类型后缓存失效

- **WHEN** 超级管理员成功删除字典类型
- **THEN** 前端清除该类型 `code` 对应缓存（或清空全部字典缓存）

#### Scenario: 其他页面字典选项更新

- **WHEN** 字典管理页完成上述变更后，用户导航至使用 `useDict` 的业务页（如用户列表的状态筛选）
- **THEN** 下拉选项反映最新字典数据，无需整页刷新
