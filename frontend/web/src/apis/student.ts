import type { PageParams, PageResult } from '@/types/api'
import { normalizePageResult } from '@/utils/page'
import { request } from './request'

/** 性别：1-男 2-女（与后端存储一致） */
export type GenderValue = '1' | '2'

export const GENDER_OPTIONS: { label: string, value: GenderValue }[] = [
  { label: '男', value: '1' },
  { label: '女', value: '2' },
]

export function normalizeGender(gender?: string | number | null): GenderValue | undefined {
  const value = String(gender ?? '')
  return value === '1' || value === '2' ? value : undefined
}

const GENDER_LABEL_MAP: Record<GenderValue, string> = {
  1: '男',
  2: '女',
}

export function formatGender(gender?: number | string | null): string {
  if (gender === '男')
    return '男'
  if (gender === '女')
    return '女'
  const value = Number(gender)
  if (value === 1)
    return GENDER_LABEL_MAP[1]
  if (value === 2)
    return GENDER_LABEL_MAP[2]
  return ''
}

export interface StudentInfo {
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
  return request<PageResult<StudentInfo>>({ url: '/student/list', method: 'get', params })
    .then(res => normalizePageResult<StudentInfo>(res))
}

export function getStudentDetailApi(id: number) {
  return request<StudentInfo>({ url: `/student/${id}`, method: 'get' })
}

export function createStudentApi(data: Partial<StudentInfo>) {
  return request({ url: '/student', method: 'post', data })
}

export function updateStudentApi(id: number, data: Partial<StudentInfo>) {
  return request({ url: `/student/${id}`, method: 'put', data })
}

export function deleteStudentApi(id: number) {
  return request({ url: `/student/${id}`, method: 'delete' })
}
