import type { StatusValue } from './role'
import { request } from './request'

export interface UserInfo {
  id: number
  username: string
  nickname: string
  phone?: string
  email?: string
  avatar?: string
  remark?: string
  status?: StatusValue
  createTime?: string
  roles: string[]
  permissions: string[]
}

export interface LoginResult {
  token: string
  user: UserInfo
}

/** 登录 */
export function loginApi(data: { username: string, password: string }) {
  return request<LoginResult>({ url: '/auth/login', method: 'post', data })
}

/** 获取用户信息 */
export function getUserInfoApi() {
  return request<UserInfo>({ url: '/auth/userinfo', method: 'get' })
}

/** 退出登录 */
export function logoutApi() {
  return request({ url: '/auth/logout', method: 'post' })
}
