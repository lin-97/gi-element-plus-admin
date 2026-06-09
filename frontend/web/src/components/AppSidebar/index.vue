<script setup lang="ts">
import AppMenuItem from '@/components/AppMenuItem/index.vue'
import { useAppStore } from '@/core/stores'
import { useMenu } from '@/hooks/useMenu'

defineOptions({ name: 'AppSidebar' })

const { drawer = false } = defineProps<{
  drawer?: boolean
}>()

const appStore = useAppStore()

const isCollapsed = computed(() => !drawer && appStore.isMenuCollapse)

const { menuList, selectedKeys, handleMenuItemClick } = useMenu()
</script>

<template>
  <aside
    class="app-sidebar"
    :class="{
      'app-sidebar--collapsed': isCollapsed,
      'app-sidebar--drawer': drawer,
      'g-area-dark': appStore.isMenuDark,
    }"
    :style="{ width: isCollapsed ? '64px' : drawer ? '100%' : `${appStore.menuWidth}px` }"
  >
    <div class="app-sidebar__logo app__logo" :style="{ height: `${appStore.headerHeight}px` }">
      <span v-if="!isCollapsed" class="app-sidebar__logo-text">GI Admin</span>
      <span v-else class="app-sidebar__logo-text">GI</span>
    </div>
    <el-scrollbar class="app-sidebar__scroll" :wrap-style="{ overflowX: 'hidden' }">
      <el-menu
        :default-active="selectedKeys[0]"
        :collapse="isCollapsed"
        :unique-opened="appStore.isMenuAccordion"
        :popper-class="appStore.isMenuDark ? 'g-area-dark' : ''"
        @select="handleMenuItemClick"
      >
        <AppMenuItem
          v-for="item in menuList"
          :key="item.path"
          :item="item"
        />
      </el-menu>
    </el-scrollbar>
  </aside>
</template>

<style lang="scss" scoped>
.app-sidebar {
  display: flex;
  flex-direction: column;
  width: 220px;
  height: 100%;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color);
  transition: width 0.3s;
  overflow: hidden;

  &--collapsed {
    width: 64px;
  }

  &--drawer {
    width: 100%;
    border-right: none;
  }

  &__scroll {
    flex: 1;
    min-height: 0;
    overflow: hidden;

    :deep(.el-menu) {
      border-right: none;
    }
  }

  &--collapsed &__scroll :deep(.el-menu--collapse) {
    width: 100%;
  }

  &__logo {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 600;
    color: var(--el-color-primary);
    border-bottom: 1px solid var(--el-border-color);
    transition: height 0.3s;

    &-text {
      font-size: 18px;
      font-weight: 600;
      white-space: nowrap;
    }
  }
}
</style>
