/**
 * @file 路由状态管理模块
 * @description 处理动态路由的加载、格式化和状态管理
 */

import type { RouteRecordRaw } from 'vue-router'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { mapTree } from 'xe-utils'
import router from '@/router'
import { DEFAULT_LAYOUT } from '../config'
import { transformPathToName } from '../utils'

/** 后端返回的异步路由配置 */
export interface AsyncRouteItem {
  activeMenu: string
  alwaysShow: boolean
  breadcrumb: boolean
  children: AsyncRouteItem[]
  component: string
  hidden: boolean
  icon: string
  id: string
  keepAlive: boolean
  parentId: string
  path: string
  permission: string
  redirect: string
  roles: string[]
  showInTabs: boolean
  sort: number
  status: '0' | '1'
  title: string
  type: 1 | 2 | 3
  affix: boolean
}

const Layout = DEFAULT_LAYOUT

const modules = import.meta.glob('@/views/**/*.vue')
const viewPathMap = new Map<string, () => Promise<any>>()

function initViewPathMap() {
  if (viewPathMap.size > 0)
    return
  for (const path in modules) {
    const dir = path.split('views/')[1]?.split('.vue')[0]
    if (dir)
      viewPathMap.set(dir, () => modules[path]())
  }
}

initViewPathMap()

export function loadView(view: string) {
  return viewPathMap.get(view)
}

function transformComponentView(component: string) {
  if (component === 'Layout')
    return Layout as never
  return loadView(component) as never
}

function formatAsyncRoutes(menus: AsyncRouteItem[]) {
  if (!menus.length)
    return []

  menus.sort((a, b) => (a?.sort ?? 0) - (b?.sort ?? 0))

  const routes = mapTree(menus, (item) => {
    if (item.children && item.children.length)
      item.children.sort((a, b) => (a?.sort ?? 0) - (b?.sort ?? 0))

    return {
      path: item.path,
      name: transformPathToName(item.path),
      component: item.component ? transformComponentView(item.component) : undefined,
      redirect: item.redirect,
      meta: {
        hidden: item.hidden,
        keepAlive: item.keepAlive,
        title: item.title,
        icon: item.icon,
        affix: item.affix,
        breadcrumb: item.breadcrumb,
        showInTabs: item.showInTabs,
        activeMenu: item.activeMenu,
        alwaysShow: item.alwaysShow,
      },
    }
  })
  return routes as RouteRecordRaw[]
}

function collectRouteNames(routes: RouteRecordRaw[], names: string[]) {
  routes.forEach((route) => {
    if (route.name)
      names.push(route.name as string)
    if (route.children?.length)
      collectRouteNames(route.children, names)
  })
}

function registerAsyncRoutes(asyncRoutes: RouteRecordRaw[]) {
  asyncRoutes.forEach((route) => {
    if (route.name)
      router.addRoute(route)
    else
      router.addRoute(route)
  })

  if (!router.hasRoute('CatchAll')) {
    router.addRoute({
      path: '/:pathMatch(.*)*',
      name: 'CatchAll',
      redirect: '/404',
      meta: { hidden: true },
    })
  }
}

function storeSetup() {
  const routes = ref<RouteRecordRaw[]>([])
  const dynamicRouteNames = ref<string[]>([])

  function resetDynamicRoutes() {
    dynamicRouteNames.value.forEach((name) => {
      if (router.hasRoute(name))
        router.removeRoute(name)
    })
    dynamicRouteNames.value = []
  }

  const setRoutes = (params: { constantRoutes: RouteRecordRaw[], asyncData: AsyncRouteItem[] }) => {
    const { constantRoutes, asyncData } = params
    const asyncRoutes = formatAsyncRoutes(asyncData)
    routes.value = constantRoutes.concat(asyncRoutes)
    const names: string[] = []
    collectRouteNames(asyncRoutes, names)
    dynamicRouteNames.value = names
    registerAsyncRoutes(asyncRoutes)
  }

  return {
    routes,
    dynamicRouteNames,
    resetDynamicRoutes,
    setRoutes,
  }
}

export const useRouteStore = defineStore('route', storeSetup, { persist: true })
