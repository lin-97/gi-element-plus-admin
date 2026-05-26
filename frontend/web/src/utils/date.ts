import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.locale('zh-cn')
dayjs.extend(relativeTime)

/** 日期格式化（统一使用 dayjs） */
export function formatDate(date?: string | number | Date, format = 'YYYY-MM-DD HH:mm:ss'): string {
  if (!date)
    return '-'
  return dayjs(date).format(format)
}

/** 相对时间 */
export function fromNow(date?: string | number | Date): string {
  if (!date)
    return '-'
  return dayjs(date).fromNow()
}

export { dayjs }
