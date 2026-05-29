import qs from 'qs'
import { request } from './request'

/** GET /auth/userinfo */
export interface UserInfo {
  id: string
  username: string
  nickname?: string
  phone?: string
  email?: string
  avatar?: string | null
  remark?: string
  status: string
  sort?: number
  createTime?: string
  deptId?: string | null
  roleIds?: string[]
  roleNames?: string[]
  roles: string[]
  permissions: string[]
}

/** POST /auth/login 响应中的 user（UserOutSchema） */
export interface LoginUser {
  id: number
  username: string
  name: string
  mobile?: string | null
  email?: string | null
  gender?: string | null
  avatar?: string | null
  isSuperuser: boolean
  status: string
  deptId?: number | null
  createTime?: string
}

export interface LoginResult {
  token: string
  accessToken: string
  refreshToken: string
  expiresIn: number
  tokenType?: string
  user: LoginUser
}
/** 登录（OAuth2 表单，需 application/x-www-form-urlencoded） */
export function loginApi(data: { username: string, password: string }) {
  return request<LoginResult>({
    url: '/auth/login',
    method: 'post',
    data: qs.stringify({
      username: data.username,
      password: data.password,
      grant_type: 'password',
    }),
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
}

/** 获取用户信息 */
export function getUserInfoApi() {
  return request<UserInfo>({ url: '/auth/userinfo', method: 'get' })
}

/** 退出登录（需 JSON body，否则后端 422） */
export function logoutApi(token?: string) {
  return request({
    url: '/auth/logout',
    method: 'post',
    data: token ? { token } : {},
  })
}
