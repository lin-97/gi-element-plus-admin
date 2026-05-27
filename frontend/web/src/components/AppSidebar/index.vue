<script setup lang="ts">
import AppMenuItem from '@/components/AppMenuItem.vue'
import { useAppStore } from '@/core/stores'
import { useMenu } from '@/hooks/useMenu'

const appStore = useAppStore()

const { menuList, selectedKeys, handleMenuItemClick } = useMenu()
</script>

<template>
  <aside
    class="app-sidebar"
    :class="{ 'app-sidebar--collapsed': appStore.isMenuCollapse }"
  >
    <div class="app-sidebar__logo">
      <span v-if="!appStore.isMenuCollapse" class="app-sidebar__logo-text">GI Admin</span>
      <span v-else class="app-sidebar__logo-text">GI</span>
    </div>
    <el-menu
      :default-active="selectedKeys[0]"
      :collapse="appStore.isMenuCollapse"
      :unique-opened="appStore.isMenuAccordion"
      @select="handleMenuItemClick"
    >
      <AppMenuItem
        v-for="item in menuList"
        :key="item.path"
        :item="item"
      />
    </el-menu>
  </aside>
</template>

<style lang="scss" scoped>
.app-sidebar {
  width: 220px;
  height: 100%;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color);
  transition: width 0.3s;
  overflow: hidden;

  &--collapsed {
    width: 64px;
  }

  :deep(.el-menu) {
    border-right: none;
  }

  &__logo {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
    color: var(--el-color-primary);
    border-bottom: 1px solid var(--el-border-color);

    &-text {
      font-size: 18px;
      font-weight: 600;
      color: var(--el-color-primary);
      white-space: nowrap;
    }
  }
}
</style>
