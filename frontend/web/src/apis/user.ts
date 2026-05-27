import type { UserInfo } from '@/apis/auth'
import { request } from './request'

/** 用户分页列表 */
export function getUserListApi(params: PageParams) {
  return request<PageResult<UserInfo>>({ url: '/user/list', method: 'get', params })
}

/** 新增用户 */
export function createUserApi(data: Partial<UserInfo>) {
  return request({ url: '/user', method: 'post', data })
}

/** 更新用户 */
export function updateUserApi(id: string | number, data: Partial<UserInfo>) {
  return request({ url: `/user/${id}`, method: 'put', data })
}

/** 删除用户 */
export function deleteUserApi(id: string | number) {
  return request({ url: `/user/${id}`, method: 'delete' })
}
