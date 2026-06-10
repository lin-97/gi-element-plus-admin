## 1. useTable 清理

- [x] 1.1 移除 `hooks/useTable.ts` 中 `getTableData` 内的 `console.log(res, 'res')`

## 2. useFormDialog composable

- [x] 2.1 新增 `hooks/useFormDialog.ts`：封装 visible、isEdit、currentId、formData、dialogTitle、openAdd、openEdit、handleBeforeOk
- [x] 2.2 在 `hooks/index.ts` 导出 `useFormDialog`
- [x] 2.3 迁移 `views/crud/FormDialog.vue` 使用 `useFormDialog`
- [x] 2.4 迁移 `views/system/dict/DictTypeFormDialog.vue` 使用 `useFormDialog`
- [x] 2.5 迁移 `views/system/dict/DictDataFormDialog.vue` 使用 `useFormDialog`（submit 注入 typeId）

## 3. 字典缓存失效

- [x] 3.1 `DictTypeFormDialog` 提交成功后调用 `clearDictCache(code)`（编辑时用原/新 code）
- [x] 3.2 `DictDataFormDialog` 提交成功后根据当前字典类型 code 调用 `clearDictCache`
- [x] 3.3 `DictTypePane` 删除类型成功后调用 `clearDictCache(deletedCode)`

## 4. 列表页搜索绑定简化

- [x] 4.1 `views/crud/index.vue`：`@search="search"`，删除无参 `handleSearch`
- [x] 4.2 `views/system/user/index.vue`：同上
- [x] 4.3 `views/system/role/index.vue`：同上

## 5. animate.css 按需加载

- [x] 5.1 移除 `main.ts` 中 `import 'animate.css/animate.min.css'`
- [x] 5.2 在 `AppNoticeDrawer/index.vue` 用 scoped 本地 `@keyframes` 实现 fadeOutRight 动画
- [x] 5.3 从 `package.json` 移除 `animate.css` 依赖并更新 lockfile

## 6. 验证

- [x] 6.1 运行 `pnpm typecheck` 与 `pnpm lint` 通过
- [x] 6.2 手动验证：字典增删改后其他页 useDict 选项更新；通知抽屉清除动画正常；CRUD/字典弹窗新增编辑正常
