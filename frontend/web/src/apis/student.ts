import { request } from './request'

/** 性别：1-男 2-女（与后端存储一致） */
export type GenderValue = '1' | '2'

export const GENDER_OPTIONS: { label: string, value: GenderValue }[] = [
  { label: '男', value: '1' },
  { label: '女', value: '2' },
]
export interface StudentItem {
  id: number
  name: string
  student_no?: string
  gender?: GenderValue
  age?: number
  phone?: string
  email?: string
  address?: string
  created_at?: string
  updated_at?: string
}

export interface StudentListQuery extends PageParams {
  name?: string
  student_no?: string
  gender?: GenderValue
  age?: number
}

export function getStudentListApi(params: StudentListQuery) {
  return request<StudentItem[]>({ url: '/student/list', method: 'get', params })
}

export function getStudentDetailApi(id: number) {
  return request<StudentItem>({ url: `/student/${id}`, method: 'get' })
}

export function createStudentApi(data: Partial<StudentItem>) {
  return request({ url: '/student', method: 'post', data })
}

export function updateStudentApi(id: number, data: Partial<StudentItem>) {
  return request({ url: `/student/${id}`, method: 'put', data })
}

/** 批量删除学生（支持单条：传 [id]） */
export function deleteStudentApi(ids: string[]) {
  return request({ url: '/student/delete', method: 'post', data: { ids } })
}
