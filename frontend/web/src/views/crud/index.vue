<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { GenderValue, StudentInfo } from '@/apis/student'
import { deleteStudentApi, formatGender, GENDER_OPTIONS, getStudentListApi } from '@/apis/student'
import { useTable } from '@/hooks/useTable'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'Crud' })

const formDialogRef = ref<InstanceType<typeof FormDialog>>()

const queryForm = reactive({
  name: '',
  student_no: '',
  gender: undefined as GenderValue | undefined,
  age: '',
})

const formColumns: FormColumnItem[] = [
  { field: 'name', label: '姓名', type: 'input' },
  { field: 'student_no', label: '学号', type: 'input' },
  {
    field: 'gender',
    label: '性别',
    type: 'select-v2',
    props: { options: GENDER_OPTIONS, clearable: true },
  },
  { field: 'age', label: '年龄', type: 'input' },
]

const tableColumns: TableColumnItem[] = [
  { type: 'selection', width: 48, align: 'center' },
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'name', label: '姓名' },
  { prop: 'student_no', label: '学号' },
  { prop: 'gender', label: '性别', render: ({ row }) => formatGender(row.gender) },
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
} = useTable<StudentInfo>(
  params => getStudentListApi({
    page: params.page,
    size: params.size,
    name: queryForm.name || undefined,
    student_no: queryForm.student_no || undefined,
    gender: queryForm.gender,
    age: queryForm.age ? Number(queryForm.age) : undefined,
  }),
  {
    rowKey: 'id',
    deleteAPI: ids => Promise.all(ids.map(id => deleteStudentApi(Number(id)))),
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
  formDialogRef.value?.openAdd()
}

function handleEdit(row: StudentInfo) {
  formDialogRef.value?.openEdit(row)
}
</script>

<template>
  <GiPageLayout class="page-container">
    <template #header>
      <GiForm
        :model-value="queryForm" :columns="formColumns" search :grid-item-props="{
          span: { xs: 24, sm: 12, md: 12, lg: 8, xl: 6, xxl: 6 },
        }" @update:model-value="Object.assign(queryForm, $event)" @search="handleSearch" @reset="handleReset"
      />
    </template>

    <template #tool>
      <el-space>
        <el-button type="primary" @click="handleAdd">
          新增
        </el-button>
        <el-button
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
        <el-button type="primary" link @click="handleEdit(row)">
          编辑
        </el-button>
        <el-button type="danger" link @click="onDelete(row)">
          删除
        </el-button>
      </template>
    </GiTable>

    <FormDialog ref="formDialogRef" @success="refresh" />
  </GiPageLayout>
</template>

<style lang="scss" scoped>
.page-container {
  height: 100%;
}
</style>
