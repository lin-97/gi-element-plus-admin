<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { UserInfo } from '@/types/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { GiForm, GiPageLayout, GiTable } from 'gi-component'
import { deleteUserApi, getUserListApi } from '@/apis/user'
import { appConfig } from '@/config'
import { formatDate } from '@/utils/date'

defineOptions({ name: 'SystemUser' })

/** 查询表单 */
const queryForm = reactive({
  username: '',
  nickname: '',
})

/** 查询表单列配置 */
const formColumns: FormColumnItem[] = [
  { field: 'username', label: '用户名', type: 'input' },
  { field: 'nickname', label: '昵称', type: 'input' },
]

/** 表格列配置 */
const tableColumns: TableColumnItem[] = [
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'username', label: '用户名', minWidth: 120 },
  { prop: 'nickname', label: '昵称', minWidth: 120 },
  { prop: 'email', label: '邮箱', minWidth: 180 },
  { prop: 'phone', label: '手机', minWidth: 140 },
  {
    prop: 'createTime',
    label: '创建时间',
    minWidth: 180,
    formatter: (row: UserInfo & { createTime?: string }) => formatDate(row.createTime),
  },
]

const loading = ref(false)
const tableData = shallowRef<UserInfo[]>([])
const total = ref(0)
const pagination = reactive({ page: 1, size: appConfig.pageSize })

/** 加载列表 */
async function fetchList() {
  loading.value = true
  try {
    const res = await getUserListApi({ ...queryForm, ...pagination })
    tableData.value = res.list
    total.value = res.total
  }
  finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  fetchList()
}

function handleReset() {
  queryForm.username = ''
  queryForm.nickname = ''
  handleSearch()
}

async function handleDelete(row: UserInfo) {
  await ElMessageBox.confirm(`确定删除用户「${row.nickname}」？`, '提示', { type: 'warning' })
  await deleteUserApi(row.id)
  ElMessage.success('删除成功')
  fetchList()
}

onMounted(() => fetchList())
</script>

<template>
  <GiPageLayout class="page-container">
    <template #header>
      <GiForm
        v-model="queryForm"
        :columns="formColumns"
        search
        @search="handleSearch"
        @reset="handleReset"
      />
    </template>

    <GiTable
      :data="tableData"
      :columns="tableColumns"
      :loading="loading"
      row-key="id"
    >
      <template #toolbar>
        <el-button type="primary">
          新增用户
        </el-button>
      </template>
      <template #action="{ row }">
        <el-button type="primary" link>
          编辑
        </el-button>
        <el-button type="danger" link @click="handleDelete(row)">
          删除
        </el-button>
      </template>
    </GiTable>

    <div class="user-page__pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :total="total"
        :page-sizes="appConfig.pageSizes"
        layout="total, sizes, prev, pager, next"
        background
        @change="fetchList"
      />
    </div>
  </GiPageLayout>
</template>

<style lang="scss" scoped>
.page-container {
  height: 100%;
}

.user-page__pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
