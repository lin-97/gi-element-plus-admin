import { request } from './request'

export type StatusValue = '0' | '1'

export interface DictOption {
  label: string
  value: string
}

export interface DictTypeItem {
  id: string
  name: string
  code: string
  status: StatusValue
  sort?: number
  remark?: string
  isSystem?: boolean
  createTime?: string
  updateTime?: string
}

export interface DictDataItem {
  id: string
  typeId: string
  label: string
  value: string
  status: StatusValue
  sort?: number
  remark?: string
  createTime?: string
}

export interface DictTypeListQuery {
  name?: string
  status?: StatusValue
}

export interface DictDataListQuery extends PageParams {
  typeId: string
  label?: string
  status?: StatusValue
}

export function getDictTypeListApi(params?: DictTypeListQuery) {
  return request<DictTypeItem[]>({ url: '/dict/type/list', method: 'get', params })
}

export function createDictTypeApi(data: Partial<DictTypeItem>) {
  return request<DictTypeItem>({ url: '/dict/type', method: 'post', data })
}

export function updateDictTypeApi(id: string, data: Partial<DictTypeItem>) {
  return request<DictTypeItem>({ url: `/dict/type/${id}`, method: 'put', data })
}

export function deleteDictTypeApi(ids: string[]) {
  return request({ url: '/dict/type/delete', method: 'post', data: { ids } })
}

export function getDictDataListApi(params: DictDataListQuery) {
  return request<PageResult<DictDataItem>>({ url: '/dict/data/list', method: 'get', params })
}

export function createDictDataApi(data: Partial<DictDataItem>) {
  return request<DictDataItem>({ url: '/dict/data', method: 'post', data })
}

export function updateDictDataApi(id: string, data: Partial<DictDataItem>) {
  return request<DictDataItem>({ url: `/dict/data/${id}`, method: 'put', data })
}

export function updateDictDataStatusApi(id: string, status: StatusValue) {
  return request<DictDataItem>({ url: `/dict/data/${id}/status`, method: 'put', data: { status } })
}

export function deleteDictDataApi(ids: string[]) {
  return request({ url: '/dict/data/delete', method: 'post', data: { ids } })
}

export function getDictByCodeApi(code: string) {
  return request<DictOption[]>({ url: `/dict/data/by-code/${code}`, method: 'get' })
}
