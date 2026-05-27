import { request } from './request'

export type StatusValue = '0' | '1'

export const STATUS_OPTIONS: { label: string, value: StatusValue }[] = [
  { label: '启用', value: '1' },
  { label: '禁用', value: '0' },
]

export interface RoleItem {
  id: number
  code: string
  name: string
  status: StatusValue
  sort?: number
  remark?: string
  isSystem?: boolean
  createTime?: string
}

export interface RoleOption {
  id: number
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

export function getRoleDetailApi(id: number) {
  return request<RoleItem>({ url: `/role/${id}`, method: 'get' })
}

export function getRoleOptionsApi() {
  return request<RoleOption[]>({ url: '/role/options', method: 'get' })
}

export function createRoleApi(data: Partial<RoleItem>) {
  return request<RoleItem>({ url: '/role', method: 'post', data })
}

export function updateRoleApi(id: number, data: Partial<RoleItem>) {
  return request({ url: `/role/${id}`, method: 'put', data })
}

export function updateRoleStatusApi(id: number, status: StatusValue) {
  return updateRoleApi(id, { status })
}

export function deleteRoleApi(ids: string[]) {
  return request({ url: '/role/delete', method: 'post', data: { ids: ids.map(Number) } })
}

export function getRoleMenusApi(roleId: number) {
  return request<{ menuIds: number[] }>({ url: `/role/${roleId}/menus`, method: 'get' })
}

export function updateRoleMenusApi(roleId: number, menuIds: number[]) {
  return request({ url: `/role/${roleId}/menus`, method: 'put', data: { menuIds } })
}
