import type { Router } from 'vue-router'
import NProgress from 'nprogress'
import { appConfig } from '@/config'
import { setRouteEmitter } from '@/core/hooks'
import { useUserStore } from '@/stores/useUserStore'
import { isRoutesLoadedState, markRoutesLoaded } from './route-load-state'
import 'nprogress/nprogress.css'

NProgress.configure({ showSpinner: false })

const whiteList = [appConfig.loginPath, appConfig.notFoundPath]

export { resetRoutesLoadedFlag } from './route-load-state'

/** 注册路由守卫 */
export function setupRouterGuard(router: Router) {
  router.beforeEach(async (to, _from, next) => {
    NProgress.start()
    const userStore = useUserStore()

    if (userStore.isLogin) {
      if (to.path === appConfig.loginPath) {
        next({ path: appConfig.homePath })
        return
      }

      if (!isRoutesLoadedState()) {
        await userStore.generateRoutes()
        markRoutesLoaded()
        next({ ...to, replace: true })
        return
      }

      next()
    }
    else {
      if (whiteList.includes(to.path)) {
        next()
      }
      else {
        next(`${appConfig.loginPath}?redirect=${to.fullPath}`)
      }
    }
  })

  router.afterEach((to, from) => {
    setRouteEmitter(to, from)
    NProgress.done()
  })
}
