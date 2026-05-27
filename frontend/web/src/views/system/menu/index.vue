<script setup lang="ts">
import type { MenuItem } from '@/apis/menu'
import { ElMessage } from 'element-plus'
import { deleteMenuApi, getMenuTreeApi } from '@/apis/menu'
import { useUserStore } from '@/stores/useUserStore'
import FormDialog from './FormDialog.vue'

defineOptions({ name: 'SystemMenu' })

const userStore = useUserStore()
const FormDialogRef = useTemplateRef('FormDialogRef')

const loading = ref(false)
const tableData = ref<MenuItem[]>([])
const expandAll = ref(true)

const typeLabel: Record<number, string> = { 1: '目录', 2: '菜单', 3: '按钮' }

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
  <GiPageLayout>
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

    <el-table
      v-loading="loading"
      :data="tableData"
      row-key="id"
      border
      :default-expand-all="expandAll"
      :tree-props="{ children: 'children' }"
    >
      <el-table-column prop="title" label="标题" min-width="160" />
      <el-table-column label="类型" width="80" align="center">
        <template #default="{ row }">
          {{ typeLabel[row.type] ?? row.type }}
        </template>
      </el-table-column>
      <el-table-column prop="path" label="路径" min-width="160" show-overflow-tooltip />
      <el-table-column prop="permission" label="权限标识" min-width="140" show-overflow-tooltip />
      <el-table-column prop="component" label="组件" min-width="140" show-overflow-tooltip />
      <el-table-column prop="sort" label="排序" width="72" align="center" />
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="row.status === '1' ? 'success' : 'info'">
            {{ row.status === '1' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" align="center" fixed="right">
        <template #default="{ row }">
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
      </el-table-column>
    </el-table>

    <FormDialog ref="FormDialogRef" @success="onFormSuccess" />
  </GiPageLayout>
</template>
