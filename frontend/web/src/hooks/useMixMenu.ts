import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { eachTree } from 'xe-utils'
import { useRouteListener } from '@/core/hooks'
import { useRouteStore } from '@/core/stores'
import { deepClone, filterSortTree, isExternal } from '@/utils'

/**
 * 混合布局菜单 Hooks
 * 顶部显示一级菜单，侧边栏显示当前一级菜单下的子菜单
 */
export function useMixMenu() {
  const router = useRouter()
  const routeStore = useRouteStore()
  const { listenerRouteChange } = useRouteListener()

  /** 完整的菜单列表（过滤隐藏项，排序） */
  const fullMenuList = computed(() => {
    const cloneRoutes = deepClone(routeStore.routes)
    return filterSortTree(cloneRoutes, i => i.meta?.hidden === false)
  })

  /** 一级菜单列表（展平只有一个子项的菜单，去掉 children） */
  const topMenuList = computed(() => {
    const cloneRoutes = deepClone(routeStore.routes)
    const showMenuList = filterSortTree(cloneRoutes, i => i.meta?.hidden === false)
    eachTree(showMenuList, (i) => {
      if (i?.children?.length === 1 && i?.meta?.alwaysShow !== true) {
        if (i.meta) {
          i.meta.title = i.meta?.title || i.children?.[0]?.meta?.title
          i.meta.icon = i.meta?.icon || i.children?.[0]?.meta?.icon
        }
        delete i.children
      }
    })
    return showMenuList
  })

  /** 当前激活的一级菜单路径 */
  const activeTopMenu = ref<string>('')

  /** 当前一级菜单下的子菜单（二级及以下） */
  const sideMenuList = computed(() => {
    const topItem = fullMenuList.value.find(item => item.path === activeTopMenu.value)
    if (!topItem?.children?.length)
      return []

    // 对子菜单做展平处理（和 useMenu 一致：只有一个子项时展平）
    const children = deepClone(topItem.children)
    eachTree(children, (i) => {
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
    return filterSortTree(children, () => true)
  })

  /** 侧边栏选中的菜单 */
  const selectedKeys = ref<string[]>([])

  /** 点击一级菜单 */
  function handleTopMenuClick(key: string) {
    if (isExternal(key)) {
      window.open(key)
      return
    }
    activeTopMenu.value = key

    const topItem = fullMenuList.value.find(item => item.path === key)
    if (!topItem?.children?.length) {
      // 没有子菜单，直接跳转
      router.push({ path: key })
    }
    else {
      // 有子菜单，跳转到第一个子菜单
      const firstChild = topItem.children[0]
      if (firstChild) {
        const targetPath
          = firstChild.children?.length === 1 && firstChild.meta?.alwaysShow !== true
            ? firstChild.children[0].path
            : firstChild.path
        router.push({ path: targetPath })
      }
    }
  }

  /** 点击侧边菜单 */
  function handleSideMenuClick(key: string) {
    if (isExternal(key)) {
      window.open(key)
      return
    }
    selectedKeys.value = [key]
    router.push({ path: key })
  }

  /** 根据当前路由自动确定激活的一级菜单 */
  function updateActiveTopMenu(path: string) {
    const matched = fullMenuList.value.find((item) => {
      if (item.path === path)
        return true
      // 检查子菜单中是否包含当前路径
      let found = false
      if (item.children?.length) {
        eachTree(item.children, (child) => {
          if (child.path === path)
            found = true
        })
      }
      return found
    })
    if (matched) {
      activeTopMenu.value = matched.path
    }
  }

  // 监听路由变化，自动更新激活状态
  listenerRouteChange(({ to }) => {
    const activePath = (to?.meta?.activeMenu as string) || to.path
    updateActiveTopMenu(activePath)
    selectedKeys.value = [to.path]
  })

  return {
    topMenuList,
    sideMenuList,
    activeTopMenu,
    selectedKeys,
    handleTopMenuClick,
    handleSideMenuClick,
  }
}
