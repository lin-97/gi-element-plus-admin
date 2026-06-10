<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { GenderValue, StudentItem } from '@/apis/student'
import { deleteStudentApi, getStudentListApi } from '@/apis/student'
import { getDictLabel, useDict } from '@/hooks/useDict'
import { useTable } from '@/hooks/useTable'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'Crud' })

const FormDialogRef = useTemplateRef('FormDialogRef')
const { dictData } = useDict(['GENDER'] as const)

const queryForm = reactive({
  name: '',
  studentNo: '',
  gender: undefined as GenderValue | undefined,
  age: '',
})

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'name', label: '姓名', type: 'input' },
  { field: 'studentNo', label: '学号', type: 'input' },
  {
    field: 'gender',
    label: '性别',
    type: 'select-v2',
    props: { options: dictData.value.GENDER, clearable: true },
  },
  { field: 'age', label: '年龄', type: 'input' },
])

const tableColumns: TableColumnItem[] = [
  { type: 'selection', width: 48, align: 'center', fixed: 'left' },
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'name', label: '姓名' },
  { prop: 'studentNo', label: '学号' },
  { prop: 'gender', label: '性别', render: ({ row }) => getDictLabel(dictData.value.GENDER, row.gender) },
  { prop: 'age', label: '年龄' },
  { prop: 'phone', label: '电话' },
  {
    prop: 'action',
    label: '操作',
    width: 120,
    align: 'center',
    slotName: 'action',
    fixed: 'right',
  },
]

/** 与 GTableSetting 内 getColumnKey 规则一致：不允许在列设置中隐藏 */
const disabledColumnKeys = ['id', 'name', 'action']

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
      studentNo: queryForm.studentNo || undefined,
      gender: queryForm.gender,
      age: queryForm.age ? Number(queryForm.age) : undefined,
    }),
    deleteAPI: ids => deleteStudentApi(ids),
  },
)

function handleReset() {
  queryForm.name = ''
  queryForm.studentNo = ''
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
  <gi-page-layout class="g-page-layout">
    <template #header>
      <gi-form
        :model-value="queryForm" :columns="formColumns" search :grid-item-props="{
          span: { xs: 24, sm: 12, md: 12, lg: 8, xl: 6, xxl: 6 },
        }" @update:model-value="Object.assign(queryForm, $event)" @search="search" @reset="handleReset"
      />
    </template>

    <g-table-setting
      :columns="tableColumns"
      :disabled-column-keys="disabledColumnKeys"
      @refresh="refresh"
    >
      <template #toolbar-left>
        <el-space wrap>
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
      <template #default="{ settingColumns, tableProps }">
        <gi-table
          v-loading="loading"
          v-bind="tableProps"
          :data="tableData"
          :columns="settingColumns"
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
        </gi-table>
      </template>
    </g-table-setting>

    <FormDialog ref="FormDialogRef" @success="refresh" />
  </gi-page-layout>
</template>

<style lang="scss" scoped>
</style>
