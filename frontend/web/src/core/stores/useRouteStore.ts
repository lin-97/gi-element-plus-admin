/**
 * @file 路由状态管理模块
 * @description
 * 负责将后端返回的菜单数据转换为 Vue Router 路由配置，并完成动态注册。
 *
 * 典型调用链：
 * 1. 用户登录 / 刷新页面 → `useUserStore.generateRoutes()` 拉取菜单
 * 2. `setRoutes()` 格式化菜单并 `router.addRoute` 注册
 * 3. 退出登录 / 切换账号 → `resetDynamicRoutes()` 移除已注册的动态路由
 */

import type { RouteRecordRaw } from 'vue-router'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { mapTree } from 'xe-utils'
import router from '@/router'
import { DEFAULT_LAYOUT } from '../config'
import { transformPathToName } from '../utils'

/**
 * 后端返回的异步路由（菜单）节点结构
 * @see `getRoutesApi` 接口响应
 */
export interface AsyncRouteItem {
  /** 高亮侧边栏菜单项（用于隐藏子路由在菜单中但仍需激活父级菜单） */
  activeMenu: string
  /** 是否始终显示根菜单（即使只有一个子菜单也不折叠） */
  alwaysShow: boolean
  /** 是否在面包屑中展示 */
  breadcrumb: boolean
  /** 子菜单 */
  children: AsyncRouteItem[]
  /** 组件路径：`Layout` 表示布局容器，否则为 `views` 下的相对路径（如 `crud/index`） */
  component: string
  /** 是否在侧边栏隐藏 */
  hidden: boolean
  /** 菜单图标（Iconify / Element Plus 图标名 / SVG 字符串） */
  icon: string
  /** 菜单 ID */
  id: string
  /** 是否缓存页面（对应 `<keep-alive>`） */
  keepAlive: boolean
  /** 父级菜单 ID */
  parentId: string
  /** 路由路径 */
  path: string
  /** 权限标识 */
  permission: string
  /** 重定向地址 */
  redirect: string
  /** 可访问该菜单的角色列表 */
  roles: string[]
  /** 是否在页签栏中展示 */
  showInTabs: boolean
  /** 排序值，越小越靠前 */
  sort: number
  /** 状态：`1` 启用，`0` 禁用 */
  status: '0' | '1'
  /** 菜单标题 */
  title: string
  /** 菜单类型：`1` 目录，`2` 菜单，`3` 按钮 */
  type: 1 | 2 | 3
  /** 是否固定在页签栏（不可关闭） */
  affix: boolean
}

/** 默认布局组件，对应后端 `component: 'Layout'` */
const Layout = DEFAULT_LAYOUT

/**
 * Vite 构建时收集的视图组件懒加载函数
 * key 形如 `@/views/crud/index.vue`
 */
const modules = import.meta.glob('@/views/**/*.vue')

/**
 * 视图路径 → 懒加载函数的映射表
 * key 为去掉 `views/` 前缀与 `.vue` 后缀的相对路径，如 `crud/index`
 */
const viewPathMap = new Map<string, () => Promise<any>>()

/**
 * 初始化视图路径映射表（仅执行一次）
 * 将 `import.meta.glob` 结果转换为便于后端 `component` 字段查找的 Map
 */
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

/**
 * 根据后端 component 字段加载对应的页面组件
 * @param view - `views` 目录下的相对路径，如 `system/user/index`
 * @returns 懒加载函数，未找到时返回 `undefined`
 */
export function loadView(view: string) {
  return viewPathMap.get(view)
}

/**
 * 将后端 component 字符串解析为 Vue Router 可识别的组件
 * @param component - `Layout` 或 views 相对路径
 */
function transformComponentView(component: string) {
  if (component === 'Layout')
    return Layout as never
  return loadView(component) as never
}

/**
 * 将后端菜单树格式化为 Vue Router 路由配置
 * - 按 `sort` 对同级菜单排序
 * - 路径转路由 `name`（PascalCase，如 `system/user` → `SystemUser`）
 * - 业务字段写入 `meta`，供侧边栏、页签、面包屑等消费
 */
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
        sort: item.sort,
      },
    }
  })
  return routes as RouteRecordRaw[]
}

/**
 * 递归收集路由树中所有 `name`，用于后续动态移除
 */
function collectRouteNames(routes: RouteRecordRaw[], names: string[]) {
  routes.forEach((route) => {
    if (route.name)
      names.push(route.name as string)
    if (route.children?.length)
      collectRouteNames(route.children, names)
  })
}

/**
 * 将动态路由注册到 Vue Router 实例
 * 同时确保 404 兜底路由（CatchAll）存在，避免动态路由注册后无法匹配未知路径
 */
function registerAsyncRoutes(asyncRoutes: RouteRecordRaw[]) {
  asyncRoutes.forEach((route) => {
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
  /** 完整路由表（静态路由 + 动态路由），供菜单等组件读取 */
  const routes = ref<RouteRecordRaw[]>([])

  /** 本次登录周期内注册的动态路由 name 列表，用于 `resetDynamicRoutes` 精确移除 */
  const dynamicRouteNames = ref<string[]>([])

  /**
   * 移除所有已注册的动态路由
   * 在重新拉取菜单（登录、刷新权限、退出登录）前调用，防止路由重复注册
   */
  function resetDynamicRoutes() {
    dynamicRouteNames.value.forEach((name) => {
      if (router.hasRoute(name))
        router.removeRoute(name)
    })
    dynamicRouteNames.value = []
  }

  /**
   * 设置并注册路由
   * - `constantRoutes`：无需权限的静态路由（登录页、404 等）
   * - `asyncData`：后端返回的菜单树，空数组表示仅保留静态路由
   */
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

/** 路由 Store，开启持久化以缓存 `routes`（动态 name 列表每次登录会重新生成） */
export const useRouteStore = defineStore('route', storeSetup, { persist: true })
