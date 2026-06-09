import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { eachTree } from 'xe-utils'
import { useRouteListener } from '@/core/hooks'
import { useRouteStore } from '@/core/stores'
import { deepClone, filterSortTree, isExternal } from '@/utils'

/**
 * 菜单管理 Hooks
 * 用于获取和处理应用程序的菜单列表
 */
export function useMenu() {
  const router = useRouter()
  const routeStore = useRouteStore()
  const { listenerRouteChange } = useRouteListener()

  /**
   * 处理后的菜单列表
   * 响应式计算属性，当路由配置变化时自动更新，
   * > hidden:false那么代表这个路由项显示在左侧菜单栏中
   * > 子项children只有一个hidden:false的子元素时, 且alwaysShow为false, 那么这个子项会被展平到父项中
   * 包含以下处理逻辑：
   * 1. 深拷贝原始路由配置避免直接修改
   * 2. 过滤掉设置为隐藏的菜单项
   * 3. 展平只有一个子项的菜单项（提升用户体验）
   */
  const menuList = computed(() => {
    // 深拷贝路由配置，防止修改原始数据
    const cloneRoutes = deepClone(routeStore.routes)

    const sortedMenuList = filterSortTree(cloneRoutes, i => i.meta?.hidden === false)

    // 遍历处理菜单树，展平只有一个子项的菜单项
    eachTree(sortedMenuList, (i) => {
      if (i?.children?.length === 1 && i?.meta?.alwaysShow !== true) {
        if (i.meta) {
          i.meta.title = i.meta?.title || i.children?.[0]?.meta?.title
          i.meta.icon = i.meta?.icon || i.children?.[0]?.meta?.icon
          i.meta.sort = i.meta?.sort ?? i.children?.[0]?.meta?.sort
        }
        i.path = i.children?.[0]?.path
        delete i.children
      }
    })
    return filterSortTree(sortedMenuList, () => true)
  })

  const selectedKeys = ref<string[]>([])

  function handleMenuItemClick(key: string) {
    if (isExternal(key)) {
      window.open(key)
      return
    }
    selectedKeys.value = [key]
    router.push({ path: key })
  }

  listenerRouteChange(({ to }) => {
    if (to?.meta?.activeMenu) {
      selectedKeys.value = [to.meta.activeMenu as string]
      return
    }
    selectedKeys.value = [to.path]
  })

  return {
    menuList,
    selectedKeys,
    handleMenuItemClick,
  }
}
