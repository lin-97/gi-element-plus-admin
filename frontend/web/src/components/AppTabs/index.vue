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
import { useTabsStore } from '@/core/stores/useTabsStore'
import { isTabWhiteList } from '@/utils/routeWhiteList'

const router = useRouter()
const route = useRoute()
const tabsStore = useTabsStore()

const activeValue = computed({
  get: () => route.path,
  set: (val) => {
    if (val && val !== route.path)
      router.push(String(val))
  },
})

const tabList = computed<NavTabItem[]>(() =>
  tabsStore.tabList
    .filter(tab => !isTabWhiteList(tab.path))
    .map(tab => ({
      label: (tab.meta?.title as string) || '未命名',
      value: tab.path,
      disabled: tab?.meta?.affix,
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

function ensureActiveRoute() {
  if (!tabsStore.tabList.some(t => t.path === route.path)) {
    const target = tabsStore.tabList.at(-1)
    if (target)
      router.push(target.fullPath || target.path)
    else
      router.push(appConfig.homePath)
  }
}

function handleClose(path: string | number, e?: Event) {
  e?.stopPropagation()
  tabsStore.close('current', String(path))
}

function handleCloseLeft(path: string | number) {
  tabsStore.close('left', String(path))
  ensureActiveRoute()
}

function handleCloseRight(path: string | number) {
  tabsStore.close('right', String(path))
  ensureActiveRoute()
}

function handleCloseOther(path: string | number) {
  tabsStore.close('other', String(path))
  ensureActiveRoute()
}

function handleCloseAll() {
  tabsStore.close('all')
}

function handleRefresh() {
  tabsStore.reloadPage()
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
            :type="active ? 'dark' : 'light-outline'"
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
