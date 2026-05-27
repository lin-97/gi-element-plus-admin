---
name: table-page
description: >-
  基于 views/crud 规范，使用 GiPageLayout、GiForm、GiTable、GiDialog、useTable、FormDialog
  生成 GI Element Plus Admin 表格/CRUD 列表页。适用于新建列表页、表格页、CRUD 页面、搜索表单、分页表格或
  frontend/web 中的新增/编辑弹窗。
---

# GI Admin 表格页（CRUD List Page）

参考实现：`frontend/web/src/views/crud/index.vue`、`FormDialog.vue`、`apis/student.ts`、`hooks/useTable.ts`。

## 文件结构

为新业务模块创建：

```
src/views/{module}/
├── index.vue        # 列表页（查询 + 表格 + 工具栏）
└── FormDialog.vue   # 新增/编辑弹窗（可选，有表单时必建）

src/apis/{module}.ts # 类型 + 列表/详情/增删改 API
```

路由组件路径与 `views` 目录一致，例如 `crud/index` → `views/crud/index.vue`。

## 技术栈约定

- Vue 3 `<script setup lang="ts">` + `defineOptions({ name: 'Xxx' })`
- 组件库：`gi-component`（`GiPageLayout`、`GiForm`、`GiTable`、`GiDialog`）
- 列表逻辑：`@/hooks/useTable`
- 请求：`@/apis/request`，分页类型 `PageResult<T>`（`list` + `total`）

## API 层模板

```typescript
import { request } from './request'

export interface XxxItem {
  id: number
  // ...业务字段
}

export interface XxxListQueryParams extends PageParams {
  // ...查询字段（可选）
}

export function getXxxListApi(params: XxxListQueryParams) {
  return request<PageResult<XxxItem>>({ url: '/xxx/list', method: 'get', params })
}

export function createXxxApi(data: Partial<XxxItem>) {
  return request({ url: '/xxx', method: 'post', data })
}

export function updateXxxApi(id: number, data: Partial<XxxItem>) {
  return request({ url: `/xxx/${id}`, method: 'put', data })
}

export function deleteXxxApi(ids: string[]) {
  return request({ url: '/xxx/delete', method: 'post', data: { ids } })
}
```

## 列表页 index.vue

### 核心结构

1. `queryForm`：`reactive` 查询条件
2. `formColumns`：`FormColumnItem[]` 搜索区
3. `tableColumns`：`TableColumnItem[]` 表格列（操作列用 `slotName: 'action'`）
4. `useTable` 绑定列表 API 与 `deleteAPI`
5. `FormDialog` ref，`@success="refresh"`

### 代码骨架

```vue
<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { XxxItem } from '@/apis/xxx'
import { deleteXxxApi, getXxxListApi } from '@/apis/xxx'
import { useTable } from '@/hooks/useTable'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'Xxx' })

const FormDialogRef = useTemplateRef('FormDialogRef')

const queryForm = reactive({
  // 与 XxxListQuery 对齐，空字符串/undefined 表示不过滤
})

const formColumns: FormColumnItem[] = [
  { field: 'name', label: '名称', type: 'input' },
  { field: 'status', label: '状态', type: 'select-v2', props: { options: [], clearable: true } },
]

const tableColumns: TableColumnItem[] = [
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'name', label: '名称' },
  {
    prop: 'action',
    label: '操作',
    width: 120,
    align: 'center',
    slotName: 'action',
  },
]

const {
  tableData,
  loading,
  pagination,
  search,
  refresh,
  onDelete,
} = useTable({
    rowKey: 'id',
    listAPI: p => getXxxListApi({ ...p, ...queryForm }),
    deleteAPI: ids => Promise.all(ids.map(id => deleteXxxApi(Number(id)))),
  },
)

function handleReset() {
  // 重置 queryForm 各字段
  search()
}

function handleAdd() { FormDialogRef.value?.openAdd() }
function handleEdit(row: XxxItem) { FormDialogRef.value?.openEdit(row) }
</script>

<template>
  <GiPageLayout>
    <template #header>
      <GiForm
        :model-value="queryForm"
        :columns="formColumns"
        search
        :grid-item-props="{ span: { xs: 24, sm: 12, md: 12, lg: 8, xl: 6, xxl: 6 } }"
        @update:model-value="Object.assign(queryForm, $event)"
        @search="search"
        @reset="handleReset"
      />
    </template>

    <template #tool>
      <el-button type="primary" @click="handleAdd">新增</el-button>
    </template>

    <GiTable
      v-loading="loading"
      border
      row-key="id"
      :data="tableData"
      :columns="tableColumns"
      :pagination="pagination"
    >
      <template #action="{ row }">
        <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
        <el-button type="danger" link @click="onDelete(row)">删除</el-button>
      </template>
    </GiTable>

    <FormDialog ref="FormDialogRef" @success="refresh" />
  </GiPageLayout>
</template>

<style lang="scss" scoped>
</style>
```

### useTable 要点

| 返回值 | 用途 |
|--------|------|
| `search()` | 查询（重置到第 1 页） |
| `refresh()` | 刷新当前页 |
| `onDelete(row)` | 单条删除（需配置 `deleteAPI`） |
| `onBatchDelete()` | 批量删除（表格需开启多选 + `onSelectionChange`） |
| `pagination` | 直接传给 `GiTable` 的 `:pagination` |

列表 API 必须返回 `PageResult<T>`（`list`、`total`）

### 表格列扩展

```typescript
// 插槽列
{ prop: 'action', label: '操作', slotName: 'action', width: 120, align: 'center' }
```

## 表单弹窗 FormDialog.vue

### 职责

- `openAdd()` / `openEdit(row)` 通过 `defineExpose` 暴露
- `emit('success')` 通知列表刷新
- `GiDialog` + `:on-before-ok`，校验通过后调 create/update API

### 代码骨架

```vue
<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { XxxItem } from '@/apis/xxx'
import { ElMessage } from 'element-plus'
import { createXxxApi, updateXxxApi } from '@/apis/xxx'

defineOptions({ name: 'XxxFormDialog' })

const emit = defineEmits<{
  (e: 'success'): void
}>()

const FormRef = useTemplateRef('FormRef')
const visible = ref(false)
const isEdit = ref(false)
const dialogTitle = computed(() => (isEdit.value ? '编辑' : '新增'))
const currentId = ref('')
const formData = ref(createEmptyForm())

function createEmptyForm() { return { /* 字段默认值 */ } }

const formRules: FormRules = {
  name: [{ required: true, message: '请输入', trigger: 'blur' }],
}

const formColumns: FormColumnItem[] = [
  { field: 'name', label: '名称', type: 'input' },
  { field: 'age', label: '年龄', type: 'input-number', props: { min: 0, max: 150 } },
  { field: 'remark', label: '备注', type: 'textarea', span: 24, props: { rows: 3 } },
]

function openAdd() {
  isEdit.value = false
  currentId.value = undefined
  formData.value = createEmptyForm()
  visible.value = true
}

function openEdit(row: XxxItem) {
  isEdit.value = true
  currentId.value = row.id
  formData.value = row
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await FormRef.value?.formRef?.validate()
    if (isEdit.value && currentId.value) {
      await updateXxxApi(currentId.value, formData.value)
      ElMessage.success('更新成功')
    } else {
      await createXxxApi(formData.value)
      ElMessage.success('添加成功')
    }
    emit('success')
    return true
  } catch {
    return false
  }
}

defineExpose({ openAdd, openEdit })
</script>

<template>
  <GiDialog
    v-model="visible"
    :title="dialogTitle"
    width="600px"
    destroy-on-close
    :on-before-ok="handleBeforeOk"
  >
    <GiForm
      ref="FormRef"
      v-model="formData"
      :columns="formColumns"
      :rules="formRules"
      label-width="80px"
    />
  </GiDialog>
</template>
```

### 表单字段类型（常用）

| type | 场景 |
|------|------|
| `input` | 文本 |
| `input-number` | 数字 |
| `select-v2` | 搜索区下拉（可 `clearable`） |
| `radio-group` | 弹窗内互斥选项 |
| `textarea` | 多行，`span: 24` 占满行 |

可选字段校验用自定义 `validator`，空值跳过（参考 `optionalPatternValidator`）。

## 生成检查清单

- [ ] API：类型、`ListQueryParams`、`PageResult`、增删改查
- [ ] `index.vue`：`useTable` + 查询重置 + 操作列插槽
- [ ] `FormDialog.vue`：`openAdd`/`openEdit`、`handleBeforeOk` 返回 boolean
- [ ] 删除走 `onDelete`，不手写 `ElMessageBox`（除非特殊流程）
- [ ] 组件 `name` 与路由/缓存命名一致
- [ ] 不修改 `src/core` 除非用户明确要求

## 禁止事项

- 列表页不要手写分页 state（优先 `useTable`）
- 不要在 `index.vue` 内联大段表单（拆 `FormDialog.vue`）
- 不要把 API 请求写在模板里

## 参考文件

| 文件 | 说明 |
|------|------|
| `views/crud/index.vue` | 标准列表页 |
| `views/crud/FormDialog.vue` | 标准表单弹窗 |
| `apis/student.ts` | API 与枚举 |
| `hooks/useTable.ts` | 表格 Hook 完整 API |
