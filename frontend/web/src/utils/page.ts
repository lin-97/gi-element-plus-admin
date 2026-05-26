import type { PageResult } from '@/types/api'

/** 兼容旧分页字段，统一为 list / size */
export function normalizePageResult<T>(data: unknown): PageResult<T> {
  const raw = (data ?? {}) as Record<string, unknown>
  const list = (raw.list ?? raw.items ?? []) as T[]
  return {
    list,
    total: Number(raw.total ?? 0),
    page: Number(raw.page ?? 1),
    size: Number(raw.size ?? raw.page_size ?? 10),
  }
}
