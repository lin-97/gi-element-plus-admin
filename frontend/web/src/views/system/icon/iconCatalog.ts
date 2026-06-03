import { icons as iconParkRaw } from '@iconify-json/icon-park-outline'
import { customIcons } from '@/icons/custom'

export const ICON_PARK_PREFIX = 'icon-park-outline'
export const CUSTOM_PREFIX = 'custom'

/** Icon Park Outline 全量图标名（约 2600+） */
export const iconParkList: string[] = Object.keys(iconParkRaw.icons).map(
  name => `${ICON_PARK_PREFIX}:${name}`,
)

/** 项目自定义 Iconify 图标名 */
export const customIconList: string[] = Object.keys(customIcons.icons).map(
  name => `${CUSTOM_PREFIX}:${name}`,
)

/** 按图标名（含前缀）过滤，大小写不敏感；无关键词时返回全量 */
export function filterIcons(list: string[], keyword: string): string[] {
  const q = keyword.trim().toLowerCase()
  if (!q)
    return list
  return list.filter(name => name.toLowerCase().includes(q))
}

/** 分页切片 */
export function paginateIcons<T>(list: T[], page: number, pageSize: number): T[] {
  const start = (page - 1) * pageSize
  return list.slice(start, start + pageSize)
}
