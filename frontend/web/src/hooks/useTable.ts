import type { AxiosResponse } from 'axios'
import type { Ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { reactive, ref } from 'vue'

/** 删除操作的配置选项 */
export interface DeleteOptions {
  /** 确认框标题 */
  title?: string
  /** 确认框内容 */
  content?: string
  /** 成功提示信息 */
  successTip?: string
}

interface Options<T> {
  onSuccess?: () => void
  onError?: (_error: Error) => void
  immediate?: boolean
  /** 行数据的唯一键（如表格 row-key） */
  rowKey?: keyof T
  listAPI: (_p: PageParams) => Promise<PageResult<T>> | Promise<T[]>
  deleteAPI?: (_pks: string[]) => Promise<any>
  exportAPI?: () => Promise<any>
}

export function useTable<F>(options: Options<F>) {
  const { onSuccess, onError, immediate = true } = options

  const loading = ref(false)
  const tableData: Ref<F[]> = ref([])

  const pagination = reactive({
    currentPage: 1,
    pageSize: 10,
    total: 0,
    onCurrentChange: (size: number) => {
      pagination.currentPage = size
      getTableData()
    },
    onSizeChange: (size: number) => {
      pagination.pageSize = size
      getTableData()
    },
  })

  function setTotal(total: number) {
    pagination.total = total
  }

  async function getTableData() {
    try {
      loading.value = true
      const res = await options.listAPI({ page: pagination.currentPage, size: pagination.pageSize })
      console.log(res, 'res')
      // 处理返回的数据结构可能是分页或数组的情况
      const data = !Array.isArray(res) ? res.list : res
      tableData.value = data as F[]
      // 设置总数据量
      const total = !Array.isArray(res) ? res.total : data.length
      setTotal(total)
      onSuccess?.()
    }
    catch (error) {
      onError?.(error as Error)
    }
    finally {
      loading.value = false
    }
  }

  // 是否立即触发请求
  immediate && getTableData()

  function search() {
    pagination.currentPage = 1
    getTableData()
  }

  function refresh() {
    getTableData()
  }

  /**
   * 处理删除操作
   * @description 弹出确认框，点击确定后确认框内显示 loading 并执行删除，成功后关闭并刷新表格
   * @param deleteApi - 删除操作的 API 函数（如 () => CmBearingService.delete(id)）
   * @param options - 删除操作的配置选项
   * @returns Promise<boolean | undefined> 用户取消为 undefined，执行结果为 true/false
   */
  function handleDelete(
    deleteApi: () => Promise<AxiosResponse<unknown>>,
    options?: DeleteOptions,
  ): Promise<boolean | undefined> {
    return new Promise((resolve) => {
      ElMessageBox.confirm(options?.content ?? '是否确认删除？', options?.title ?? '提示', {
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
          deleteApi()
            .then(() => {
              ElMessage.success(options?.successTip ?? '删除成功')
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
      }).catch(() => resolve(undefined))
    })
  }

  const selectedKeys = ref<string[]>([])
  const onSelectionChange = (rows: F[]) => {
    selectedKeys.value = rows.map(row => row[options.rowKey as keyof F] as unknown as string)
  }

  // 删除单个数据
  const onDelete = (row: F) => {
    if (!options.deleteAPI) {
      ElMessage.error('deleteAPI没有配置')
      return
    }
    const deleteAPI = options.deleteAPI
    handleDelete(() => deleteAPI([row[options.rowKey as keyof F] as unknown as string]))
  }

  // 批量删除数据
  const onBatchDelete = () => {
    if (!options.deleteAPI) {
      ElMessage.error('deleteAPI没有配置')
      return
    }
    if (!selectedKeys.value.length) {
      ElMessage.error('请选择要删除的数据')
      return
    }
    const deleteAPI = options.deleteAPI
    handleDelete(() => deleteAPI(selectedKeys.value.map(key => key as unknown as string)), {
      title: '批量删除',
      content: `确定要删除选中的 ${selectedKeys.value.length} 条数据吗？`,
      successTip: '删除成功',
    })
  }

  return {
    /** 表格数据 */
    tableData,
    /** 获取表格数据 */
    getTableData,
    /** 分页数据 */
    pagination,
    /** 加载状态 */
    loading,
    /** 搜索 */
    search,
    /** 刷新 */
    refresh,
    /** 处理删除（确认框、确定后 loading、成功提示与刷新） */
    handleDelete,
    /** 选择项变化时触发 */
    onSelectionChange,
    /** 选择项 */
    selectedKeys,
    /** 删除单个数据 */
    onDelete,
    /** 批量删除数据 */
    onBatchDelete,
  }
}
