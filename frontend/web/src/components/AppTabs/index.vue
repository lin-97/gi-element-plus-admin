<script setup lang="ts">
import type { DropdownInstance } from 'element-plus'
import type { NavTabItem } from 'gi-component'
import type { RouteLocationNormalized } from 'vue-router'
import {
  ArrowLeft,
  ArrowRight,
  Close,
  Minus,
} from '@element-plus/icons-vue'
import { Icon } from '@iconify/vue'
import { HOME_PATH } from '@/core/config'
import { useRouteListener } from '@/core/hooks'
import { useTabsStore } from '@/core/stores/useTabsStore'

defineOptions({ name: 'AppTabs' })

const isHomeTab = (path: string) => path === '/' || path === HOME_PATH

const router = useRouter()
const route = useRoute()
const tabsStore = useTabsStore()
const { listenerRouteChange } = useRouteListener()

listenerRouteChange(({ to }) => {
  tabsStore.addTabItem(to)
}, true)

const activeValue = computed({
  get: () => route.path,
  set: (val) => {
    if (val && val !== route.path)
      router.push(String(val))
  },
})

type TabItem = RouteLocationNormalized & NavTabItem & { value: string }

const tabList = computed<TabItem[]>(() =>
  tabsStore.tabList
    .map(tab => ({
      label: (tab.meta?.title as string) || '未命名',
      value: tab.path,
      disabled: false,
      ...tab,
    }))
    .sort((a, b) => Number(isHomeTab(String(b.value))) - Number(isHomeTab(String(a.value)))),
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
</script>

<template>
  <div class="app-tabs">
    <gi-nav-tabs v-model="activeValue" :data="tabList" custom>
      <template #default="{ item, active }">
        <gi-tag
          v-if="item.meta?.affix || ['/', '/dashboard'].includes(item.value)"
          :type="active ? 'dark' : 'light-outline'"
          :color="active ? 'primary' : 'info'"
          size="large"
          :closable="false"
          style="height: 26px;"
          @close="tabsStore.close('current', item.value)"
        >
          {{ item.label }}
        </gi-tag>

        <el-dropdown
          v-else
          :ref="(el) => setDropdownRef(item.value, el)"
          trigger="contextmenu"
          @visible-change="(visible) => handleContextMenuVisible(visible, item.value)"
        >
          <gi-tag
            :type="active ? 'dark' : 'light-outline'"
            :color="active ? 'primary' : 'info'"
            size="large"
            :closable="true"
            @close="tabsStore.close('current', item.value)"
          >
            {{ item.label }}
          </gi-tag>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item :icon="ArrowLeft" @click="tabsStore.close('left', item.value)">
                关闭左侧
              </el-dropdown-item>
              <el-dropdown-item :icon="ArrowRight" @click="tabsStore.close('right', item.value)">
                关闭右侧
              </el-dropdown-item>
              <el-dropdown-item :icon="Minus" @click="tabsStore.close('other', item.value)">
                关闭其他
              </el-dropdown-item>
              <el-dropdown-item :icon="Close" @click="tabsStore.close('all')">
                关闭所有
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template #right-extra>
        <el-button text circle class="g-square-button app-tabs__reload" @click="tabsStore.reloadPage()">
          <Icon icon="custom:reload" width="17" height="17" />
        </el-button>
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

.app-tabs__reload {
  color: var(--el-text-color-primary);
}
</style>
