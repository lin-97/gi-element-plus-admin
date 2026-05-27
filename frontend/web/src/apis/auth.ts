import { request } from './request'

export interface LoginResult {
  token: string
  user: {
    id: number
    username: string
    nickname: string
    role: string
  }
}

export type UserInfo = LoginResult['user']

/** 登录 */
export function loginApi(data: { username: string, password: string }) {
  return request<LoginResult>({ url: '/auth/login', method: 'post', data })
}

/** 获取用户信息 */
export function getUserInfoApi() {
  return request<LoginResult['user']>({ url: '/auth/userinfo', method: 'get' })
}

/** 退出登录 */
export function logoutApi() {
  return request({ url: '/auth/logout', method: 'post' })
}
