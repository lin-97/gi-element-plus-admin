import type { Router } from 'vue-router'
import NProgress from 'nprogress'
import { appConfig } from '@/config'
import { usePermissionStore } from '@/stores/modules/permission'
import { useTabsStore } from '@/stores/modules/tabs'
import { useUserStore } from '@/stores/modules/user'
import 'nprogress/nprogress.css'

NProgress.configure({ showSpinner: false })

const whiteList = [appConfig.loginPath, appConfig.notFoundPath]

/** 注册路由守卫 */
export function setupRouterGuard(router: Router) {
  router.beforeEach(async (to, _from, next) => {
    NProgress.start()
    const userStore = useUserStore()
    const permissionStore = usePermissionStore()

    if (userStore.isLogin) {
      if (to.path === appConfig.loginPath) {
        next({ path: appConfig.homePath })
        return
      }

      if (!permissionStore.isRoutesLoaded) {
        const mergedRoutes = await permissionStore.generateRoutes()
        mergedRoutes.forEach((route: import('vue-router').RouteRecordRaw) => {
          router.addRoute(route)
        })
        next({ ...to, replace: true })
        return
      }

      next()
    }
    else {
      if (permissionStore.isRoutesLoaded) {
        permissionStore.reset()
        useTabsStore().reset()
      }
      if (whiteList.includes(to.path)) {
        next()
      }
      else {
        next(`${appConfig.loginPath}?redirect=${to.fullPath}`)
      }
    }
  })

  router.afterEach((to) => {
    const tabsStore = useTabsStore()
    tabsStore.addTab(to)
    NProgress.done()
  })
}
