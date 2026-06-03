<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { RoleItem, StatusValue } from '@/apis/role'
import { ElMessage } from 'element-plus'
import { deleteRoleApi, getRoleListApi, updateRoleStatusApi } from '@/apis/role'
import { SUPER_ADMIN_ROLE } from '@/core/config'
import { useDict } from '@/hooks/useDict'
import { useTable } from '@/hooks/useTable'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'SystemRole' })

const FormDialogRef = useTemplateRef('FormDialogRef')
const { dictData } = useDict(['STATUS'] as const)

const queryForm = reactive({
  code: '',
  name: '',
  status: undefined as StatusValue | undefined,
})

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'code', label: '角色标识', type: 'input' },
  { field: 'name', label: '角色名称', type: 'input' },
  {
    field: 'status',
    label: '状态',
    type: 'select-v2',
    props: { options: dictData.value.STATUS, clearable: true },
  },
])

const tableColumns: TableColumnItem[] = [
  {
    type: 'selection',
    width: 48,
    align: 'center',
    selectable: (row: RoleItem) => !isSystemRole(row),
  },
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'code', label: '角色标识', minWidth: 150 },
  { prop: 'name', label: '角色名称', minWidth: 150 },
  { prop: 'status', label: '状态', width: 100, align: 'center', slotName: 'status' },
  { prop: 'sort', label: '排序', width: 80, align: 'center' },
  { prop: 'createTime', label: '创建时间', width: 180 },
  { prop: 'remark', label: '备注', minWidth: 200, showOverflowTooltip: true },
  {
    prop: 'action',
    label: '操作',
    width: 120,
    align: 'center',
    fixed: 'right',
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
} = useTable({
  rowKey: 'id',
  listAPI: p => getRoleListApi({
    ...p,
    code: queryForm.code || undefined,
    name: queryForm.name || undefined,
    status: queryForm.status,
  }),
  deleteAPI: ids => deleteRoleApi(ids),
})

function isSystemRole(row: RoleItem) {
  return row.code === SUPER_ADMIN_ROLE
}

function handleSearch() {
  search()
}

function handleReset() {
  queryForm.code = ''
  queryForm.name = ''
  queryForm.status = undefined
  search()
}

function handleAdd() {
  FormDialogRef.value?.openAdd()
}

function handleEdit(row: RoleItem) {
  FormDialogRef.value?.openEdit(row)
}

async function handleStatusSwitch(row: RoleItem, val: string | number | boolean) {
  if (!row?.id)
    return
  const status = val as StatusValue
  try {
    await updateRoleStatusApi(row.id, status)
    ElMessage.success(status === '1' ? '已启用' : '已禁用')
  }
  catch {
    refresh()
  }
}
</script>

<template>
  <gi-page-layout class="g-page-layout">
    <template #header>
      <gi-form
        :model-value="queryForm"
        :columns="formColumns"
        search
        :grid-item-props="{ span: { xs: 24, sm: 12, md: 12, lg: 8, xl: 6, xxl: 6 } }"
        @update:model-value="Object.assign(queryForm, $event)"
        @search="handleSearch"
        @reset="handleReset"
      />
    </template>

    <template #tool>
      <el-space>
        <gi-button type="add" @click="handleAdd">
          新增
        </gi-button>
        <el-button type="danger" :disabled="!selectedKeys.length" @click="onBatchDelete">
          批量删除
        </el-button>
      </el-space>
    </template>

    <gi-table
      v-loading="loading"
      border
      :data="tableData"
      :columns="tableColumns"
      row-key="id"
      :pagination="pagination"
      @selection-change="onSelectionChange"
    >
      <template #status="{ row }">
        <el-switch
          v-if="!isSystemRole(row)"
          v-model="row.status"
          active-value="1"
          inactive-value="0"
          inline-prompt
          active-text="启用"
          inactive-text="禁用"
          @change="val => handleStatusSwitch(row, val)"
        />
        <el-tag v-else type="success">
          启用
        </el-tag>
      </template>
      <template #action="{ row }">
        <el-space :size="4">
          <el-button type="primary" link :disabled="isSystemRole(row)" @click="handleEdit(row)">
            编辑
          </el-button>
          <el-button type="danger" link :disabled="isSystemRole(row)" @click="onDelete(row)">
            删除
          </el-button>
        </el-space>
      </template>
    </gi-table>

    <FormDialog ref="FormDialogRef" @success="refresh" />
  </gi-page-layout>
</template>
