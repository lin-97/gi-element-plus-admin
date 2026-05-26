import type { RouteRecordRaw } from 'vue-router'
import type { AsyncRouteItem } from '@/core/stores/useRouteStore'
import { defineStore } from 'pinia'
import { getRoutesApi } from '@/apis/menu'
import { transformPathToName } from '@/core/utils'
import { resolveGlobModule } from '@/utils/modules'

const layoutModules = import.meta.glob('@/layouts/**/index.vue')
const viewModules = import.meta.glob('@/views/**/*.vue')

function resolveComponent(component: string) {
  if (!component)
    return undefined
  if (component === 'Layout' || component.startsWith('Layout')) {
    const layoutName = component === 'Layout' ? 'default' : component.replace('Layout', '').toLowerCase()
    return resolveGlobModule(layoutModules, path => path.includes(`/layouts/${layoutName}/index.vue`))
  }
  return resolveGlobModule(viewModules, path => path.endsWith(`/views/${component}.vue`))
    ?? resolveGlobModule(viewModules, path => path.endsWith(`/views/${component}/index.vue`))
}

function transformAsyncRoutes(menus: AsyncRouteItem[]): RouteRecordRaw[] {
  if (!menus.length)
    return []

  const sorted = [...menus].sort((a, b) => (a.sort ?? 0) - (b.sort ?? 0))

  return sorted.map((item) => {
    const children = item.children?.length
      ? transformAsyncRoutes([...item.children].sort((a, b) => (a.sort ?? 0) - (b.sort ?? 0)))
      : undefined

    const route: RouteRecordRaw = {
      path: item.path,
      name: transformPathToName(item.path),
      redirect: item.redirect || undefined,
      meta: {
        title: item.title,
        icon: item.icon,
        hidden: item.hidden,
        keepAlive: item.keepAlive,
        affix: item.affix,
        breadcrumb: item.breadcrumb,
        showInTabs: item.showInTabs,
        activeMenu: item.activeMenu,
        alwaysShow: item.alwaysShow,
        permission: item.permission || undefined,
      },
      children,
    }

    if (item.component) {
      const resolved = resolveComponent(item.component) as RouteRecordRaw['component']
      if (!resolved)
        console.error(`[permission] 未找到路由组件: ${item.component}`)
      route.component = resolved
    }

    return route
  })
}

export const usePermissionStore = defineStore('permission', () => {
  const staticRoutes: RouteRecordRaw[] = [
    {
      path: '/',
      component: () => import('@/layouts/default/index.vue'),
      meta: { title: '首页', icon: 'home' },
      children: [
        {
          path: 'dashboard',
          component: () => import('@/views/dashboard/index.vue'),
          meta: { title: '工作台', icon: 'house', affix: true },
        },
      ],
    },
  ]

  const routes = ref<RouteRecordRaw[]>([...staticRoutes])
  const isRoutesLoaded = ref(false)

  async function generateRoutes() {
    try {
      const data = await getRoutesApi()
      console.log('[permission] API routes data:', data)
      const dynamicRoutes = transformAsyncRoutes(data)
      console.log('[permission] transformed routes:', dynamicRoutes)
      const allRoutes = [...staticRoutes, ...dynamicRoutes]
      console.log('[permission] all routes:', allRoutes)
      routes.value = allRoutes
      isRoutesLoaded.value = true
      return allRoutes
    }
    catch (e) {
      console.error('[permission] generateRoutes error:', e)
      isRoutesLoaded.value = true
      return routes.value
    }
  }

  function reset() {
    routes.value = [...staticRoutes]
    isRoutesLoaded.value = false
  }

  return { routes, isRoutesLoaded, generateRoutes, reset }
})
