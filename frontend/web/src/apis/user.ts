import type { RoleOption } from './role'
import type { StatusValue } from './role'
import { request } from './request'

/** 头像 URL 最大长度（与后端 users.avatar VARCHAR(500) 一致） */
export const AVATAR_MAX_LENGTH = 500

export interface SysUserItem {
  id: string
  username: string
  nickname?: string
  phone?: string
  email?: string
  avatar?: string
  remark?: string
  status: StatusValue
  sort?: number
  createTime?: string
  isSuperAdmin?: boolean
  deptId?: string | null
  roleIds?: string[]
  roleNames?: string[]
  roles?: string[]
}

export interface SysUserListQuery extends PageParams {
  username?: string
  phone?: string
  status?: StatusValue
}

export interface SysUserFormData {
  username: string
  password?: string
  nickname?: string
  phone?: string
  email?: string
  avatar?: string
  remark?: string
  status: StatusValue
  sort?: number
  roleIds: string[]
}

export function getUserListApi(params: SysUserListQuery) {
  return request<PageResult<SysUserItem>>({ url: '/user/list', method: 'get', params })
}

export function getUserDetailApi(id: string) {
  return request<SysUserItem>({ url: `/user/${id}`, method: 'get' })
}

export function createUserApi(data: Partial<SysUserFormData> & { password: string }) {
  const { roleIds, ...rest } = data
  return request({ url: '/user', method: 'post', data: { ...rest, role_ids: roleIds ?? [] } })
}

export function updateUserApi(id: string, data: Partial<SysUserFormData>) {
  const { roleIds, ...rest } = data
  return request({ url: `/user/${id}`, method: 'put', data: { ...rest, role_ids: roleIds } })
}

export function deleteUserApi(ids: string[]) {
  return request({ url: '/user/delete', method: 'post', data: { ids } })
}

export function resetUserPasswordApi(id: string, password: string) {
  return request({ url: `/user/${id}/password`, method: 'put', data: { password } })
}

export function updateUserStatusApi(id: string, status: StatusValue) {
  return request({ url: `/user/${id}/status`, method: 'put', data: { status } })
}

export type { RoleOption }
