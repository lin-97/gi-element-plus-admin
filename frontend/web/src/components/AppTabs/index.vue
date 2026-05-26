<script setup lang="ts">
import type { DropdownInstance } from 'element-plus'
import type { NavTabItem } from 'gi-component'
import {
  ArrowLeft,
  ArrowRight,
  Close,
  Minus,
  Refresh,
} from '@element-plus/icons-vue'
import { GiTag } from 'gi-component'
import { appConfig } from '@/config'
import { useTabsStore } from '@/stores/modules/tabs'

const router = useRouter()
const route = useRoute()
const tabsStore = useTabsStore()

const activeValue = computed({
  get: () => tabsStore.activeTab,
  set: (val) => {
    if (val && val !== route.path)
      router.push(String(val))
  },
})

const tabList = computed<NavTabItem[]>(() =>
  tabsStore.tabs.map(tab => ({
    label: tab.title,
    value: tab.path,
  })),
)

const dropdownRefMap = new Map<string | number, DropdownInstance>()

function setDropdownRef(value: string | number, el: unknown) {
  if (el)
    dropdownRefMap.set(value, el as DropdownInstance)
  else
    dropdownRefMap.delete(value)
}

/** 新开页签右键菜单时，关闭其它页签已打开的菜单 */
function handleContextMenuVisible(visible: boolean, value: string | number) {
  if (!visible)
    return
  dropdownRefMap.forEach((inst, key) => {
    if (key !== value)
      inst.handleClose()
  })
}

function isAffix(path: string | number) {
  return !!tabsStore.tabs.find(t => t.path === path)?.affix
}

function ensureActiveRoute() {
  if (!tabsStore.tabs.some(t => t.path === route.path)) {
    const target = tabsStore.tabs.at(-1)
    if (target)
      router.push(target.path)
    else
      router.push(appConfig.homePath)
  }
}

function handleClose(path: string | number, e?: Event) {
  e?.stopPropagation()
  const pathStr = String(path)
  const next = tabsStore.closeTab(pathStr)
  if (pathStr === route.path && next)
    router.push(next.path)
}

function handleCloseLeft(path: string | number) {
  tabsStore.closeLeft(String(path))
  ensureActiveRoute()
}

function handleCloseRight(path: string | number) {
  tabsStore.closeRight(String(path))
  ensureActiveRoute()
}

function handleCloseOther(path: string | number) {
  const pathStr = String(path)
  tabsStore.closeOther(pathStr)
  if (route.path !== pathStr)
    router.push(pathStr)
}

function handleCloseAll() {
  tabsStore.closeAll()
  ensureActiveRoute()
}

function handleRefresh() {
  router.replace({ path: `/redirect${route.fullPath}` })
}
</script>

<template>
  <div class="app-tabs">
    <gi-nav-tabs v-model="activeValue" :data="tabList" custom>
      <template #default="{ item, active, disabled }">
        <el-dropdown
          :ref="(el) => setDropdownRef(item.value, el)"
          trigger="contextmenu"
          :disabled="disabled"
          @visible-change="(visible) => handleContextMenuVisible(visible, item.value)"
        >
          <GiTag
            :type="active ? 'dark' : 'light'"
            :color="active ? 'primary' : 'info'"
            size="large"
            :closable="!disabled"
            style="height: 26px;"
            @close="handleClose(item.value, $event)"
          >
            {{ item.label }}
          </GiTag>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item :icon="ArrowLeft" @click="handleCloseLeft(item.value)">
                关闭左侧
              </el-dropdown-item>
              <el-dropdown-item :icon="ArrowRight" @click="handleCloseRight(item.value)">
                关闭右侧
              </el-dropdown-item>
              <el-dropdown-item :icon="Minus" @click="handleCloseOther(item.value)">
                关闭其他
              </el-dropdown-item>
              <el-dropdown-item :icon="Close" @click="handleCloseAll()">
                关闭所有
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template #right-extra>
        <el-button text circle bg :icon="Refresh" @click="handleRefresh" />
      </template>
    </gi-nav-tabs>
  </div>
</template>

<style lang="scss" scoped>
.app-tabs {
  width: 100%;
  padding: 0 10px;
  box-sizing: border-box;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);

  :deep(.gi-tag) {
    cursor: pointer;
  }
}
</style>
