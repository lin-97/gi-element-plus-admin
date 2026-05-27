/** 应用全局配置 */
export const appConfig = {
  /** 应用标题 */
  title: import.meta.env.VITE_APP_TITLE,
  /** API 前缀 */
  apiPrefix: import.meta.env.VITE_API_BASE_URL,
  /** Token 请求头字段 */
  tokenHeader: 'Authorization',
  /** Token 前缀 */
  tokenPrefix: 'Bearer ',
  /** 登录页路径 */
  loginPath: '/login',
  /** 首页路径 */
  homePath: '/dashboard',
  /** 404 路径 */
  notFoundPath: '/404',
  /** 页签白名单（不加入系统页签） */
  tabWhiteList: ['/login', '/404'],
  /** 页签白名单路径前缀 */
  tabWhitePrefixList: ['/redirect'],
}

/** 是否属于页签白名单路由（不展示在系统页签中） */
export function isTabWhiteList(path: string) {
  if (appConfig.tabWhiteList.includes(path))
    return true
  return appConfig.tabWhitePrefixList.some(prefix => path.startsWith(prefix))
}
