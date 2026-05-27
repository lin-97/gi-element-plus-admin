import type { AsyncRouteItem } from '@/core/stores/useRouteStore'
import { request } from './request'

export type MenuType = 1 | 2 | 3
export type StatusValue = '0' | '1'

export interface MenuItem {
  id: string
  parentId: string
  type: MenuType
  title: string
  path?: string
  component?: string
  redirect?: string
  icon?: string
  permission?: string
  sort?: number
  status: StatusValue
  hidden?: boolean
  keepAlive?: boolean
  affix?: boolean
  alwaysShow?: boolean
  breadcrumb?: boolean
  showInTabs?: boolean
  activeMenu?: string
  isSystem?: boolean
  children?: MenuItem[]
}

export interface MenuFormData {
  parentId: string
  type: MenuType
  title: string
  path: string
  component: string
  redirect: string
  icon: string
  permission: string
  sort: number
  status: StatusValue
  hidden: boolean
  keepAlive: boolean
  affix: boolean
  alwaysShow: boolean
  breadcrumb: boolean
  showInTabs: boolean
  activeMenu: string
}

/** 获取动态路由菜单 */
export function getRoutesApi() {
  return request<AsyncRouteItem[]>({ url: '/menu/routes', method: 'get' })
}

/** 管理端菜单树 */
export function getMenuTreeApi() {
  return request<MenuItem[]>({ url: '/menu/tree', method: 'get' })
}

export function createMenuApi(data: Partial<MenuFormData>) {
  return request({ url: '/menu', method: 'post', data })
}

export function updateMenuApi(id: string, data: Partial<MenuFormData>) {
  return request({ url: `/menu/${id}`, method: 'put', data })
}

export function deleteMenuApi(ids: string[]) {
  return request({ url: '/menu/delete', method: 'post', data: { ids } })
}
