<script setup lang="ts">
import AppMenuItem from '@/components/AppMenuItem/index.vue'
import { useAppStore } from '@/core/stores'
import { useMenu } from '@/hooks/useMenu'

defineOptions({ name: 'AppSidebar' })

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
    <el-scrollbar class="app-sidebar__scroll">
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

  &__scroll {
    flex: 1;
    min-height: 0;

    :deep(.el-menu) {
      border-right: none;
    }
  }

  &__logo {
    flex-shrink: 0;
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
