<script setup lang="ts">
import type { TableColumnItem } from 'gi-component'
import type { MenuItem } from '@/apis/menu'
import { ElMessage, ElMessageBox } from 'element-plus'
import { deleteMenuApi, getMenuTreeApi } from '@/apis/menu'
import { transformPathToName } from '@/core/utils'
import { useUserStore } from '@/stores/useUserStore'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'SystemMenu' })

const userStore = useUserStore()
const FormDialogRef = useTemplateRef('FormDialogRef')

const loading = ref(false)
const tableData = ref<MenuItem[]>([])
const expandAll = ref(true)

const typeLabel: Record<number, string> = { 1: '目录', 2: '菜单', 3: '按钮' }

const typeTagType: Record<number, 'primary' | 'success' | 'info'> = {
  1: 'primary',
  2: 'success',
  3: 'info',
}

const tableColumns: TableColumnItem[] = [
  { prop: 'title', label: '标题', minWidth: 160 },
  { prop: 'type', label: '类型', width: 88, align: 'center', slotName: 'type' },
  { prop: 'path', label: '路径', minWidth: 160, showOverflowTooltip: true },
  { label: '组件名', minWidth: 160, showOverflowTooltip: true, slotName: 'componentName' },
  { prop: 'component', label: '组件', minWidth: 140, showOverflowTooltip: true },
  { prop: 'icon', label: '图标', width: 72, align: 'center', slotName: 'icon' },
  { prop: 'permission', label: '权限标识', minWidth: 140, showOverflowTooltip: true },
  { prop: 'sort', label: '排序', width: 72, align: 'center' },
  { prop: 'status', label: '状态', width: 80, align: 'center', slotName: 'status' },
  {
    prop: 'action',
    label: '操作',
    width: 180,
    align: 'center',
    fixed: 'right',
    slotName: 'action',
  },
]

async function loadTree() {
  loading.value = true
  try {
    tableData.value = await getMenuTreeApi()
  }
  finally {
    loading.value = false
  }
}

async function handleRefreshRoutes() {
  await userStore.refreshRoutes()
  ElMessage.success('路由已刷新')
}

function handleAddRoot() {
  FormDialogRef.value?.openAdd()
}

function handleAddChild(row: MenuItem) {
  FormDialogRef.value?.openAdd(row)
}

function handleEdit(row: MenuItem) {
  FormDialogRef.value?.openEdit(row)
}

async function handleDelete(row: MenuItem) {
  if (row.isSystem) {
    ElMessage.warning('系统菜单不可删除')
    return
  }
  if (row.children?.length) {
    ElMessage.warning('请先删除子节点')
    return
  }
  try {
    await ElMessageBox.confirm(
      `确定删除「${row.title}」吗？`,
      '提示',
      { type: 'warning', confirmButtonText: '确定', cancelButtonText: '取消' },
    )
    await deleteMenuApi([row.id])
    ElMessage.success('删除成功')
    await loadTree()
    await userStore.refreshRoutes()
  }
  catch {
    /* handled by request */
  }
}

async function onFormSuccess() {
  await loadTree()
  await userStore.refreshRoutes()
}

onMounted(() => {
  loadTree()
})
</script>

<template>
  <gi-page-layout class="g-page-layout">
    <template #tool>
      <el-space>
        <gi-button type="add" @click="handleAddRoot">
          新增根目录
        </gi-button>
        <el-button @click="handleRefreshRoutes">
          刷新路由
        </el-button>
      </el-space>
    </template>

    <gi-table
      v-loading="loading"
      border
      :data="tableData"
      :columns="tableColumns"
      row-key="id"
      :default-expand-all="expandAll"
      :tree-props="{ children: 'children' }"
      :pagination="false"
    >
      <template #type="{ row }">
        <el-tag
          size="small"
          :type="typeTagType[row.type] ?? 'info'"
          effect="light"
        >
          {{ typeLabel[row.type] ?? row.type }}
        </el-tag>
      </template>
      <template #componentName="{ row }">
        <span>{{ row.path ? transformPathToName(row.path) : '-' }}</span>
      </template>
      <template #icon="{ row }">
        <AppMenuIcon v-if="row.icon" :icon="row.icon" :size="18" />
        <span v-else>-</span>
      </template>
      <template #status="{ row }">
        <el-tag :type="row.status === '1' ? 'success' : 'info'">
          {{ row.status === '1' ? '启用' : '禁用' }}
        </el-tag>
      </template>
      <template #action="{ row }">
        <el-space :size="4">
          <el-button
            v-if="row.type !== 3"
            type="primary"
            link
            @click="handleAddChild(row)"
          >
            新增子级
          </el-button>
          <el-button type="primary" link @click="handleEdit(row)">
            编辑
          </el-button>
          <el-button
            type="danger"
            link
            :disabled="row.isSystem"
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </el-space>
      </template>
    </gi-table>

    <FormDialog ref="FormDialogRef" @success="onFormSuccess" />
  </gi-page-layout>
</template>
