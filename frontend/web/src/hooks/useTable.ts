import type { Ref } from 'vue'
import type { PageResult } from '@/types/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, reactive, ref } from 'vue'
import { appConfig } from '@/config'

export interface UseTablePaginationParams {
  page: number
  pageSize: number
}

export interface UseTableOptions<T> {
  /** 行主键字段，默认 id */
  rowKey?: keyof T
  /** 是否立即加载 */
  immediate?: boolean
  /** 默认每页条数 */
  defaultPageSize?: number
  /** 删除接口，接收主键数组 */
  deleteAPI?: (ids: Array<string | number>) => Promise<unknown>
  onSuccess?: () => void
  onError?: (error: Error) => void
}

export type UseTableApi<T, Q = Record<string, unknown>> = (
  params: UseTablePaginationParams & Q,
) => Promise<PageResult<T>>

export function useTable<T extends object = object, Q = Record<string, unknown>>(
  api: UseTableApi<T, Q>,
  options: UseTableOptions<T> = {},
) {
  const {
    rowKey = 'id' as keyof T,
    immediate = true,
    defaultPageSize = appConfig.pageSize,
    deleteAPI,
    onSuccess,
    onError,
  } = options

  const loading = ref(false)
  const tableData: Ref<T[]> = ref([])
  const selectedKeys = ref<Array<string | number>>([])

  const paginationState = reactive({
    currentPage: 1,
    pageSize: defaultPageSize,
    total: 0,
  })

  async function getTableData() {
    try {
      loading.value = true
      const res = await api({
        page: paginationState.currentPage,
        pageSize: paginationState.pageSize,
      } as UseTablePaginationParams & Q)
      tableData.value = res.items
      paginationState.total = res.total
      onSuccess?.()
    }
    catch (error) {
      onError?.(error as Error)
    }
    finally {
      loading.value = false
    }
  }

  function search() {
    paginationState.currentPage = 1
    getTableData()
  }

  function refresh() {
    getTableData()
  }

  function handlePageChange(page: number) {
    paginationState.currentPage = page
    getTableData()
  }

  function handleSizeChange(pageSize: number) {
    paginationState.pageSize = pageSize
    paginationState.currentPage = 1
    getTableData()
  }

  /** 供 GiTable 使用的分页配置（字段名与 Element Plus 一致） */
  const pagination = computed(() => ({
    currentPage: paginationState.currentPage,
    pageSize: paginationState.pageSize,
    total: paginationState.total,
    pageSizes: appConfig.pageSizes,
    layout: 'total, sizes, prev, pager, next',
    background: true,
    onCurrentChange: handlePageChange,
    onSizeChange: handleSizeChange,
  }))

  const onSelectionChange = (rows: T[]) => {
    selectedKeys.value = rows.map(row => row[rowKey] as string | number)
  }

  interface DeleteOptions {
    title?: string
    content?: string
    successTip?: string
  }

  function handleDelete(
    deleteFn: () => Promise<unknown>,
    deleteOptions?: DeleteOptions,
  ): Promise<boolean | undefined> {
    return new Promise((resolve) => {
      ElMessageBox.confirm(
        deleteOptions?.content ?? '是否确认删除？',
        deleteOptions?.title ?? '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          beforeClose: (action, instance, done) => {
            if (action === 'cancel') {
              done()
              resolve(undefined)
              return
            }
            instance.confirmButtonLoading = true
            deleteFn()
              .then(() => {
                ElMessage.success(deleteOptions?.successTip ?? '删除成功')
                getTableData()
                instance.confirmButtonLoading = false
                done()
                resolve(true)
              })
              .catch((err) => {
                console.error('删除失败', err)
                instance.confirmButtonLoading = false
                done()
                resolve(false)
              })
          },
        },
      ).catch(() => resolve(undefined))
    })
  }

  function onDelete(row: T) {
    if (!deleteAPI) {
      ElMessage.error('deleteAPI 未配置')
      return
    }
    handleDelete(() => deleteAPI([row[rowKey] as string | number]))
  }

  function onBatchDelete() {
    if (!deleteAPI) {
      ElMessage.error('deleteAPI 未配置')
      return
    }
    if (!selectedKeys.value.length) {
      ElMessage.error('请选择要删除的数据')
      return
    }
    handleDelete(
      () => deleteAPI(selectedKeys.value),
      {
        title: '批量删除',
        content: `确定要删除选中的 ${selectedKeys.value.length} 条数据吗？`,
        successTip: '删除成功',
      },
    )
  }

  if (immediate)
    getTableData()

  return {
    tableData,
    loading,
    pagination,
    selectedKeys,
    getTableData,
    search,
    refresh,
    handlePageChange,
    handleSizeChange,
    onSelectionChange,
    handleDelete,
    onDelete,
    onBatchDelete,
  }
}
