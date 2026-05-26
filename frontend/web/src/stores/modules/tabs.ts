import type { RouteLocationNormalized } from 'vue-router'
import { defineStore } from 'pinia'

export interface TabItem {
  path: string
  title: string
  name?: string | symbol | null
  affix?: boolean
  keepAlive?: boolean
}

export const useTabsStore = defineStore('tabs', () => {
  const tabs = ref<TabItem[]>([])
  const activeTab = ref('')

  /** 添加标签页 */
  function addTab(route: RouteLocationNormalized) {
    const title = (route.meta?.title as string) || '未命名'
    if (route.meta?.hidden)
      return

    const exist = tabs.value.find(t => t.path === route.path)
    if (!exist) {
      tabs.value.push({
        path: route.path,
        title,
        name: route.name,
        affix: route.meta?.affix as boolean,
        keepAlive: route.meta?.keepAlive as boolean,
      })
    }
    activeTab.value = route.path
  }

  /** 关闭标签页 */
  function closeTab(path: string) {
    const index = tabs.value.findIndex(t => t.path === path)
    if (index === -1)
      return
    const tab = tabs.value[index]
    if (tab.affix)
      return
    tabs.value.splice(index, 1)
    return tabs.value[index] || tabs.value[index - 1]
  }

  /** 关闭左侧 */
  function closeLeft(path: string) {
    const index = tabs.value.findIndex(t => t.path === path)
    if (index === -1)
      return
    tabs.value = tabs.value.filter((t, i) => t.affix || i >= index)
  }

  /** 关闭右侧 */
  function closeRight(path: string) {
    const index = tabs.value.findIndex(t => t.path === path)
    if (index === -1)
      return
    tabs.value = tabs.value.filter((t, i) => t.affix || i <= index)
  }

  /** 关闭其他 */
  function closeOther(path: string) {
    tabs.value = tabs.value.filter(t => t.affix || t.path === path)
  }

  /** 关闭全部（保留固定） */
  function closeAll() {
    tabs.value = tabs.value.filter(t => t.affix)
  }

  /** 重置 */
  function reset() {
    tabs.value = []
    activeTab.value = ''
  }

  return { tabs, activeTab, addTab, closeTab, closeLeft, closeRight, closeOther, closeAll, reset }
})
