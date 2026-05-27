import type { StatusValue } from './dict'
import { request } from './request'

export type { StatusValue } from './dict'

export interface RoleItem {
  id: string
  code: string
  name: string
  status: StatusValue
  sort?: number
  remark?: string
  isSystem?: boolean
  createTime?: string
}

export interface RoleOption {
  id: string
  code: string
  name: string
}

export interface RoleListQuery extends PageParams {
  code?: string
  name?: string
  status?: StatusValue
}

export function getRoleListApi(params: RoleListQuery) {
  return request<PageResult<RoleItem>>({ url: '/role/list', method: 'get', params })
}

export function getRoleDetailApi(id: string) {
  return request<RoleItem>({ url: `/role/${id}`, method: 'get' })
}

export function getRoleOptionsApi() {
  return request<RoleOption[]>({ url: '/role/options', method: 'get' })
}

export function createRoleApi(data: Partial<RoleItem>) {
  return request<RoleItem>({ url: '/role', method: 'post', data })
}

export function updateRoleApi(id: string, data: Partial<RoleItem>) {
  return request({ url: `/role/${id}`, method: 'put', data })
}

export function updateRoleStatusApi(id: string, status: StatusValue) {
  return updateRoleApi(id, { status })
}

export function deleteRoleApi(ids: string[]) {
  return request({ url: '/role/delete', method: 'post', data: { ids } })
}

export function getRoleMenusApi(roleId: string) {
  return request<{ menuIds: string[] }>({ url: `/role/${roleId}/menus`, method: 'get' })
}

export function updateRoleMenusApi(roleId: string, menuIds: string[]) {
  return request({ url: `/role/${roleId}/menus`, method: 'put', data: { menuIds } })
}
