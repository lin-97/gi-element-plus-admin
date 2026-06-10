# use-form-dialog Specification

## Purpose
TBD - created by archiving change frontend-hooks-formdialog-optimize. Update Purpose after archive.
## Requirements
### Requirement: useFormDialog 表单弹窗状态机

前端 SHALL 在 `@/hooks/useFormDialog` 提供 composable，封装表单弹窗的通用状态：`visible`、`isEdit`、`currentId`、`formData`、`dialogTitle`，以及 `openAdd`、`openEdit`、`handleBeforeOk` 方法。

调用方 MUST 传入：
- `createEmptyForm: () => TForm` — 空表单工厂
- `toFormData: (row: TRow) => TForm` — 行数据转表单（编辑时用）
- `submit: (ctx: { isEdit: boolean, id: string, data: TForm }) => Promise<void>` — 提交逻辑

`handleBeforeOk` SHALL 依次：校验表单（通过 `formRef`）、调用 `submit`、触发 `onSuccess` 回调、返回 `true`；校验或提交失败时返回 `false` 且不关闭弹窗。

#### Scenario: 打开新增弹窗

- **WHEN** 调用方执行 `openAdd()`
- **THEN** `visible` 为 `true`、`isEdit` 为 `false`、`currentId` 为空、`formData` 为 `createEmptyForm()` 返回值

#### Scenario: 打开编辑弹窗

- **WHEN** 调用方执行 `openEdit(row)`
- **THEN** `visible` 为 `true`、`isEdit` 为 `true`、`currentId` 为行 id、`formData` 为 `toFormData(row)` 返回值

#### Scenario: 提交成功

- **WHEN** 用户在弹窗点击确定且表单校验通过、`submit`  resolve
- **THEN** `handleBeforeOk` 返回 `true` 并调用 `onSuccess` 回调

#### Scenario: 提交失败不关闭

- **WHEN** 表单校验失败或 `submit` reject
- **THEN** `handleBeforeOk` 返回 `false` 且弹窗保持打开

### Requirement: FormDialog 组件复用 useFormDialog

标准 CRUD FormDialog（含 `gi-dialog` + `gi-form` + validate + create/update API）SHALL 使用 `useFormDialog` 管理状态，不得在组件内重复实现相同的 visible/isEdit/openAdd/openEdit 样板代码。

复杂弹窗（含额外异步数据加载、动态 formRules、非标准 open 参数如 menu 父节点）MAY 仅部分复用或暂不迁移，但新增的标准 FormDialog MUST 使用 `useFormDialog`。

#### Scenario: crud FormDialog 使用 composable

- **WHEN** 查看 `views/crud/FormDialog.vue`
- **THEN** 通过 `useFormDialog` 管理弹窗状态与提交
- **AND** 仍通过 `defineExpose({ openAdd, openEdit })` 对外暴露接口

#### Scenario: 字典 FormDialog 使用 composable

- **WHEN** 查看 `DictTypeFormDialog.vue` 与 `DictDataFormDialog.vue`
- **THEN** 两者均使用 `useFormDialog` 管理弹窗状态与提交

