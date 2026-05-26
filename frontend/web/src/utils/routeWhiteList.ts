import { appConfig } from '@/config'

/** 是否属于页签白名单路由（不展示在系统页签中） */
export function isTabWhiteList(path: string) {
  if (appConfig.tabWhiteList.includes(path))
    return true
  return appConfig.tabWhitePrefixList.some(prefix => path.startsWith(prefix))
}
