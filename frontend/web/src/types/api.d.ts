/** 统一 API 响应结构 */
interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

/** 分页请求参数 */
interface PageParams {
  page: number
  size: number
}

/** 分页响应数据 */
interface PageResult<T> {
  list: T[]
  total: number
  page: number
  size: number
}
