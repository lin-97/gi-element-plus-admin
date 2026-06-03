<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { StatusValue } from '@/apis/role'
import type { SysUserItem } from '@/apis/user'
import { ElMessage } from 'element-plus'
import { deleteUserApi, getUserListApi, updateUserStatusApi } from '@/apis/user'
import { useDict, useTable } from '@/hooks'
import FormDialog from './FormDialog.vue'
import ResetPasswordDialog from './ResetPasswordDialog.vue'

defineOptions({ name: 'SystemUser' })

const FormDialogRef = useTemplateRef('FormDialogRef')
const ResetPasswordDialogRef = useTemplateRef('ResetPasswordDialogRef')
const { dictData } = useDict(['STATUS'] as const)

const queryForm = reactive({
  username: '',
  phone: '',
  status: undefined as StatusValue | undefined,
})

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'username', label: '用户名', type: 'input' },
  { field: 'phone', label: '手机', type: 'input' },
  {
    field: 'status',
    label: '状态',
    type: 'select-v2',
    props: { options: dictData.value.STATUS, clearable: true },
  },
])

const tableColumns: TableColumnItem[] = [
  { type: 'selection', width: 48, align: 'center', selectable: (row: SysUserItem) => !row.isSuperAdmin },
  { prop: 'avatar', label: '头像', width: 72, slotName: 'avatar' },
  { prop: 'username', label: '用户名', minWidth: 100 },
  { prop: 'nickname', label: '昵称', minWidth: 100 },
  { prop: 'phone', label: '手机', minWidth: 120 },
  { prop: 'email', label: '邮箱', minWidth: 180 },
  { prop: 'roles', label: '角色', minWidth: 140, align: 'center', slotName: 'roles' },
  { prop: 'sort', label: '排序', width: 80, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slotName: 'status' },
  { prop: 'createTime', label: '创建时间', width: 180 },
  { prop: 'remark', label: '备注', minWidth: 200, showOverflowTooltip: true },
  {
    prop: 'action',
    label: '操作',
    width: 180,
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
  listAPI: p => getUserListApi({
    ...p,
    username: queryForm.username || undefined,
    phone: queryForm.phone || undefined,
    status: queryForm.status,
  }),
  deleteAPI: ids => deleteUserApi(ids),
})

function isSuperAdminRow(row: SysUserItem) {
  return !!row.isSuperAdmin
}

function handleSearch() {
  search()
}

function handleReset() {
  queryForm.username = ''
  queryForm.phone = ''
  queryForm.status = undefined
  search()
}

function handleAdd() {
  FormDialogRef.value?.openAdd()
}

function handleEdit(row: SysUserItem) {
  FormDialogRef.value?.openEdit(row)
}

function handleResetPassword(row: SysUserItem) {
  ResetPasswordDialogRef.value?.open(row.id, row.username)
}

async function handleStatusSwitch(row: SysUserItem, val: string | number | boolean) {
  if (!row?.id)
    return
  const status = val as StatusValue
  try {
    await updateUserStatusApi(row.id, status)
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
      <template #avatar="{ row }">
        <el-avatar :size="32" :src="row.avatar">
          {{ row.username?.charAt(0) }}
        </el-avatar>
      </template>
      <template #roles="{ row }">
        <el-space wrap>
          <el-tag v-for="name in (row.roleNames || [])" :key="name" size="small">
            {{ name }}
          </el-tag>
        </el-space>
      </template>
      <template #status="{ row }">
        <el-switch
          v-if="!isSuperAdminRow(row)"
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
        <el-space :size="4" wrap>
          <el-button type="primary" link @click="handleEdit(row)">
            编辑
          </el-button>
          <el-button
            v-if="!isSuperAdminRow(row)"
            type="primary"
            link
            @click="handleResetPassword(row)"
          >
            重置密码
          </el-button>
          <el-button
            v-if="!isSuperAdminRow(row)"
            type="danger"
            link
            @click="onDelete(row)"
          >
            删除
          </el-button>
        </el-space>
      </template>
    </gi-table>

    <FormDialog ref="FormDialogRef" @success="refresh" />
    <ResetPasswordDialog ref="ResetPasswordDialogRef" />
  </gi-page-layout>
</template>
