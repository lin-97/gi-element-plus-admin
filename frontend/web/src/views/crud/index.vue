<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { GenderValue, StudentItem } from '@/apis/student'
import { deleteStudentApi, getStudentListApi } from '@/apis/student'
import { useDict } from '@/hooks/useDict'
import { useTable } from '@/hooks/useTable'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'Crud' })

const FormDialogRef = useTemplateRef('FormDialogRef')
const { options: genderOptions, getLabel: getGenderLabel } = useDict('GENDER')

const queryForm = reactive({
  name: '',
  student_no: '',
  gender: undefined as GenderValue | undefined,
  age: '',
})

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'name', label: '姓名', type: 'input' },
  { field: 'student_no', label: '学号', type: 'input' },
  {
    field: 'gender',
    label: '性别',
    type: 'select-v2',
    props: { options: genderOptions.value, clearable: true },
  },
  { field: 'age', label: '年龄', type: 'input' },
])

const tableColumns: TableColumnItem[] = [
  { type: 'selection', width: 48, align: 'center' },
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'name', label: '姓名' },
  { prop: 'student_no', label: '学号' },
  { prop: 'gender', label: '性别', render: ({ row }) => getGenderLabel(row.gender) },
  { prop: 'age', label: '年龄' },
  { prop: 'phone', label: '电话' },
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
  selectedKeys,
  search,
  refresh,
  onDelete,
  onBatchDelete,
  onSelectionChange,
} = useTable(
  {
    rowKey: 'id',
    listAPI: p => getStudentListApi({
      ...p,
      name: queryForm.name || undefined,
      student_no: queryForm.student_no || undefined,
      gender: queryForm.gender,
      age: queryForm.age ? Number(queryForm.age) : undefined,
    }),
    deleteAPI: ids => deleteStudentApi(ids),
  },
)

function handleSearch() {
  search()
}

function handleReset() {
  queryForm.name = ''
  queryForm.student_no = ''
  queryForm.gender = undefined
  queryForm.age = ''
  search()
}

function handleAdd() {
  FormDialogRef.value?.openAdd()
}

function handleEdit(row: StudentItem) {
  FormDialogRef.value?.openEdit(row)
}
</script>

<template>
  <GiPageLayout class="g-page-layout">
    <template #header>
      <GiForm
        :model-value="queryForm" :columns="formColumns" search :grid-item-props="{
          span: { xs: 24, sm: 12, md: 12, lg: 8, xl: 6, xxl: 6 },
        }" @update:model-value="Object.assign(queryForm, $event)" @search="handleSearch" @reset="handleReset"
      />
    </template>

    <template #tool>
      <el-space>
        <gi-button v-hasPerm="['crud:add']" type="add" @click="handleAdd">
          新增
        </gi-button>
        <el-button
          v-hasPerm="['crud:delete']"
          type="danger"
          :disabled="!selectedKeys.length"
          @click="onBatchDelete"
        >
          批量删除
        </el-button>
      </el-space>
    </template>

    <GiTable
      v-loading="loading"
      border
      :data="tableData"
      :columns="tableColumns"
      row-key="id"
      :pagination="pagination"
      @selection-change="onSelectionChange"
    >
      <template #action="{ row }">
        <el-button v-hasPerm="['crud:edit']" type="primary" link @click="handleEdit(row)">
          编辑
        </el-button>
        <el-button v-hasPerm="['crud:delete']" type="danger" link @click="onDelete(row)">
          删除
        </el-button>
      </template>
    </GiTable>

    <FormDialog ref="FormDialogRef" @success="refresh" />
  </GiPageLayout>
</template>

<style lang="scss" scoped>
</style>
