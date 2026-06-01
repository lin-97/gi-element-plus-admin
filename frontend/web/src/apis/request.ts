import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import axios from 'axios'
import qs from 'qs'
import { appConfig } from '@/config'
import router from '@/router'
import { useUserStore } from '@/stores/useUserStore'

/** HTTP 状态码 */
export enum HttpCode {
  SUCCESS = 200,
  UNAUTHORIZED = 401,
  /** 后端业务认证失败码（CustomException code=10401） */
  AUTH_FAILED = 10401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  SERVER_ERROR = 500,
}

function isAuthError(status?: number, code?: number) {
  return status === HttpCode.UNAUTHORIZED
    || code === HttpCode.UNAUTHORIZED
    || code === HttpCode.AUTH_FAILED
}

function shouldSkipAuthRedirect(url?: string) {
  if (!url)
    return false
  return url.includes('/auth/login') || url.includes('/auth/logout')
}

function handleAuthExpired(configUrl?: string) {
  if (shouldSkipAuthRedirect(configUrl))
    return
  const userStore = useUserStore()
  if (!userStore.isLogin)
    return
  userStore.logout()
  router.push(appConfig.loginPath)
}

/** 创建 axios 实例 */
const service: AxiosInstance = axios.create({
  baseURL: appConfig.apiPrefix,
  timeout: 30000,
  paramsSerializer: params => qs.stringify(params, { arrayFormat: 'brackets' }),
})

/** 请求拦截器 */
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.set(appConfig.tokenHeader, `${appConfig.tokenPrefix}${userStore.token}`)
    }
    return config
  },
  error => Promise.reject(error),
)

/** 响应拦截器 */
service.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const res = response.data
    if (res.code === HttpCode.SUCCESS)
      return response

    if (isAuthError(undefined, res.code))
      handleAuthExpired(response.config.url)
    return Promise.reject(new Error(res.message || '请求失败'))
  },
  (error) => {
    const status = error.response?.status as number | undefined
    const res = error.response?.data as ApiResponse | undefined
    if (isAuthError(status, res?.code))
      handleAuthExpired(error.config?.url)

    const detail = error.response?.data?.detail
    const message = res?.message
      || (typeof detail === 'string' ? detail : Array.isArray(detail) ? detail[0]?.msg : undefined)
      || error.message
      || '网络异常'
    return Promise.reject(new Error(message))
  },
)

/** 通用请求方法 */
export function request<T = unknown>(config: AxiosRequestConfig): Promise<T> {
  return service.request<ApiResponse<T>>(config).then(res => res.data.data)
}

export default service
