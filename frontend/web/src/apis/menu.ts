import type { AsyncRouteItem } from '@/core/stores/useRouteStore'
import { request } from './request'

/** 获取动态路由菜单 */
export function getRoutesApi() {
  return request<AsyncRouteItem[]>({ url: '/menu/routes', method: 'get' })
}
