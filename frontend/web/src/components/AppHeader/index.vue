<script setup lang="ts">
import AppBreadcrumb from '@/components/AppBreadcrumb/index.vue'
import AppHeaderActions from '@/components/AppHeaderActions/index.vue'
import AppMenuItem from '@/components/AppMenuItem/index.vue'
import AppMenuToggle from '@/components/AppMenuToggle/index.vue'
import { useAppStore } from '@/core/stores'
import { useMenu } from '@/hooks/useMenu'
import { useResponsive } from '@/hooks/useResponsive'

defineOptions({ name: 'AppHeader' })

const { mode = 'default' } = defineProps<{
  mode?: 'default' | 'top'
}>()

const appStore = useAppStore()
const { menuList, selectedKeys, handleMenuItemClick } = useMenu()
const { isXs, isMobile } = useResponsive()

const isTopMode = computed(() => mode === 'top')
</script>

<template>
  <header
    class="app-header"
    :class="{
      'app-header--top': isTopMode,
      'g-area-dark': isTopMode && appStore.isMenuDark,
    }"
    :style="{ height: `${appStore.headerHeight}px` }"
  >
    <div class="app-header__left">
      <template v-if="isTopMode">
        <span v-if="!isMobile" class="app-header__logo app__logo">GI Admin</span>
        <AppMenuToggle v-if="isMobile" />
        <el-menu
          mode="horizontal"
          :default-active="selectedKeys[0]"
          :unique-opened="appStore.isMenuAccordion"
          :popper-class="appStore.isMenuDark ? 'g-area-dark' : ''"
          class="app-header__menu"
          @select="handleMenuItemClick"
        >
          <AppMenuItem
            v-for="item in menuList"
            :key="item.path"
            :item="item"
          />
        </el-menu>
      </template>
      <template v-else>
        <AppMenuToggle />
        <AppBreadcrumb v-if="!isXs" />
      </template>
    </div>

    <AppHeaderActions />
  </header>
</template>

<style lang="scss" scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color);
  transition: height 0.3s;
  box-sizing: border-box;

  :deep(.el-menu--horizontal) {
    --el-menu-horizontal-height: 100%;
    --el-menu-item-height: 100%;
  }

  &--top {
    height: auto;
    flex-wrap: wrap;
  }

  &__left {
    height: 100%;
    display: flex;
    flex: 1;
    gap: 12px;
    align-items: center;
    min-width: 0;
    overflow: hidden;
  }

  &__logo {
    flex-shrink: 0;
    font-size: 18px;
    font-weight: 600;
    color: var(--el-color-primary);
    white-space: nowrap;
  }

  &__menu {
    flex: 1;
    min-width: 0;
    border-bottom: none;
  }
}
</style>
