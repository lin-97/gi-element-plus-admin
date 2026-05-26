/**
 * @file 面包屑 Hook
 * @description 基于路由 matched 与标签页标题生成面包屑导航数据
 */

import type { RouteLocationMatched, RouteLocationNormalized } from 'vue-router'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { HOME_PATH } from '../config'
import { useTabsStore } from '../stores/useTabsStore'
import { useRouteListener } from './useRouteListener'

export interface BreadcrumbItem {
  title: string
  path: string
  to?: string
  redirect?: RouteLocationMatched['redirect']
  children: RouteLocationMatched['children']
  meta: RouteLocationMatched['meta']
}

/** 首页路由缓存 */
let homeRoute: RouteLocationMatched | null = null

export function useBreadcrumb() {
  const route = useRoute()
  const router = useRouter()
  const { listenerRouteChange } = useRouteListener()
  const tabsStore = useTabsStore()

  const breadcrumbList = ref<RouteLocationMatched[]>([])

  function getHomeRoute() {
    if (homeRoute)
      return
    const found = router.getRoutes().find(i => i.path === HOME_PATH)
    homeRoute = (found ?? null) as RouteLocationMatched | null
  }

  function getBreadcrumbList(to: RouteLocationNormalized) {
    getHomeRoute()
    const matched = to.matched.filter(
      i => i.meta?.title && i.meta?.breadcrumb !== false,
    )
    if (homeRoute && !matched.some(i => i.path === homeRoute!.path))
      breadcrumbList.value = [homeRoute, ...matched]
    else
      breadcrumbList.value = matched
  }

  function isLastItem(index: number) {
    return index === breadcrumbList.value.length - 1
  }

  function hasRedirect(item: RouteLocationMatched) {
    return !!item.redirect && item.redirect !== 'noRedirect' && item.redirect !== ''
  }

  function handleLink(item: RouteLocationMatched) {
    const { redirect, path, children } = item
    if (redirect === 'noRedirect' && children?.length) {
      const child = children[0]
      router.push((child.meta?.activeMenu as string) || child.path)
      return
    }
    if (redirect) {
      router.push(redirect as string)
      return
    }
    router.push(path)
  }

  listenerRouteChange(({ to }) => {
    if (to.path.startsWith('/redirect/'))
      return
    getBreadcrumbList(to)
  }, true)

  const lastTitle = computed(
    () => (tabsStore.tabList.find(i => i.path === route.path)?.meta?.title as string) || '',
  )

  function getItemTitle(item: RouteLocationMatched, index: number) {
    if (isLastItem(index) && !hasRedirect(item))
      return lastTitle.value || (item.meta?.title as string) || ''
    return (item.meta?.title as string) || ''
  }

  function resolveBreadcrumbTo(item: RouteLocationMatched, index: number): string | undefined {
    if (isLastItem(index) && !hasRedirect(item))
      return undefined
    const { redirect, children, path } = item
    if (redirect === 'noRedirect' && children?.length) {
      const child = children[0]
      return (child.meta?.activeMenu as string) || child.path
    }
    if (redirect)
      return redirect as string
    return path
  }

  const breadcrumbs = computed<BreadcrumbItem[]>(() =>
    breadcrumbList.value.map((item, index) => ({
      title: getItemTitle(item, index),
      path: item.path,
      to: resolveBreadcrumbTo(item, index),
      redirect: item.redirect,
      children: item.children,
      meta: item.meta,
    })),
  )

  return {
    breadcrumbList,
    breadcrumbs,
    lastTitle,
    isLastItem,
    hasRedirect,
    handleLink,
    getItemTitle,
    resolveBreadcrumbTo,
  }
}
