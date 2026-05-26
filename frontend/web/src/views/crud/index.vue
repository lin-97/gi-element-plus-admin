<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { StudentInfo } from '@/apis/student'
import { GiForm, GiPageLayout, GiTable } from 'gi-component'
import { deleteStudentApi, getStudentListApi } from '@/apis/student'
import { useTable } from '@/hooks/useTable'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'Crud' })

const formDialogRef = ref<InstanceType<typeof FormDialog>>()

const queryForm = reactive({
  name: '',
})

const formColumns: FormColumnItem[] = [
  { field: 'name', label: '姓名', type: 'input' },
]

const tableColumns: TableColumnItem[] = [
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'name', label: '姓名' },
  { prop: 'student_no', label: '学号' },
  { prop: 'gender', label: '性别' },
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
  search,
  refresh,
  onDelete,
} = useTable<StudentInfo>(
  params => getStudentListApi({
    page: params.page,
    pageSize: params.pageSize,
    page_size: params.pageSize,
    name: queryForm.name || undefined,
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
      <GiForm v-model="queryForm" :columns="formColumns" search @search="handleSearch" @reset="handleReset" />
    </template>

    <template #tool>
      <el-button type="primary" @click="handleAdd">
        新增
      </el-button>
    </template>

    <GiTable
      border
      :data="tableData"
      :columns="tableColumns"
      :loading="loading"
      row-key="id"
      :pagination="pagination"
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
