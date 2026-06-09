<script setup lang="ts">
/**
 * 混合布局模式
 * 顶部显示 Logo + 一级菜单，侧边栏显示当前一级菜单下的二级及以下菜单
 */
import { Icon } from '@iconify/vue'
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'
import AppHeaderActions from '@/components/AppHeaderActions/index.vue'
import AppMenuIcon from '@/components/AppMenuIcon/index.vue'
import AppMenuItem from '@/components/AppMenuItem/index.vue'
import AppMenuToggle from '@/components/AppMenuToggle/index.vue'
import AppTabs from '@/components/AppTabs/index.vue'
import PageTransition from '@/components/PageTransition/index.vue'
import { useAppStore } from '@/core/stores'
import { useMixMenu } from '@/hooks/useMixMenu'

defineOptions({ name: 'MixLayout' })

const appStore = useAppStore()
const breakpoints = useBreakpoints(breakpointsTailwind)
const isMobile = breakpoints.smaller('md')

const {
  topMenuList,
  sideMenuList,
  activeTopMenu,
  selectedKeys,
  handleTopMenuClick,
  handleSideMenuClick,
} = useMixMenu()

const collapseIcon = computed(() =>
  appStore.isMenuCollapse ? 'custom:menu-unfold' : 'custom:menu-fold',
)

function toggleCollapse() {
  appStore.setMenuCollapse(!appStore.isMenuCollapse)
}
</script>

<template>
  <div class="layout">
    <!-- 顶部区域：Logo + 一级菜单 + 工具栏 -->
    <header
      class="mix-header"
      :class="{ 'g-area-dark': appStore.isMenuDark }"
      :style="{ height: `${appStore.headerHeight}px` }"
    >
      <div class="mix-header__left">
        <div v-if="!isMobile" class="mix-header__logo app__logo" :style="{ width: appStore.isMenuCollapse ? '64px' : `${appStore.menuWidth}px` }">
          <span v-if="!appStore.isMenuCollapse">GI Admin</span>
          <span v-else>GI</span>
        </div>
        <el-menu
          v-if="!isMobile"
          mode="horizontal"
          :default-active="activeTopMenu"
          class="mix-header__menu"
          @select="handleTopMenuClick"
        >
          <el-menu-item
            v-for="item in topMenuList"
            :key="item.path"
            :index="item.path"
          >
            <AppMenuIcon :icon="(item.meta?.icon as string)" />
            <template #title>
              {{ item.meta?.title }}
            </template>
          </el-menu-item>
        </el-menu>
        <AppMenuToggle v-else style="margin-left: 16px" />
      </div>
      <div class="mix-header__right">
        <AppHeaderActions />
      </div>
    </header>

    <!-- 下方区域 -->
    <div class="layout__body">
      <!-- 侧边栏：当前一级菜单的子菜单 -->
      <aside
        v-if="sideMenuList.length && !isMobile"
        class="mix-sidebar"
        :class="{
          'mix-sidebar--collapsed': appStore.isMenuCollapse,
          'g-area-dark': appStore.isMenuDark,
        }"
        :style="{ width: appStore.isMenuCollapse ? '64px' : `${appStore.menuWidth}px` }"
      >
        <el-scrollbar
          class="mix-sidebar__scroll"
          :wrap-style="{ overflowX: 'hidden' }"
        >
          <el-menu
            :default-active="selectedKeys[0]"
            :collapse="appStore.isMenuCollapse"
            :unique-opened="appStore.isMenuAccordion"
            :collapse-transition="false"
            :popper-class="appStore.isMenuDark ? 'g-area-dark' : ''"
            @select="handleSideMenuClick"
          >
            <AppMenuItem
              v-for="item in sideMenuList"
              :key="item.path"
              :item="item"
            />
          </el-menu>
        </el-scrollbar>
        <div class="mix-sidebar__toggle" @click="toggleCollapse">
          <Icon :icon="collapseIcon" width="18" height="18" />
        </div>
      </aside>

      <!-- 主内容区 -->
      <div class="layout__main">
        <AppTabs v-if="appStore.isShowTabs" />
        <div class="layout__content">
          <PageTransition />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--el-fill-color-light);
}

.mix-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 16px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color);
  transition: height 0.3s;
  box-sizing: border-box;

  :deep(.el-menu--horizontal) {
    --el-menu-horizontal-height: 100%;
    --el-menu-item-height: 100%;
  }

  &__left {
    height: 100%;
    display: flex;
    flex: 1;
    align-items: center;
    min-width: 0;
    overflow: hidden;
  }

  &__logo {
    width: 220px;
    flex-shrink: 0;
    font-size: 18px;
    font-weight: 600;
    color: var(--el-color-primary);
    white-space: nowrap;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  &__menu {
    flex: 1;
    min-width: 0;
    border-bottom: none;
  }

  &__right {
    display: flex;
    align-items: center;
  }
}

.layout__body {
  display: flex;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.mix-sidebar {
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
    width: 100%;
    overflow: hidden;

    :deep(.el-scrollbar__wrap) {
      overflow-x: hidden !important;
    }

    :deep(.el-scrollbar__view) {
      width: 100% !important;
    }

    :deep(.el-scrollbar__bar.is-horizontal) {
      display: none !important;
    }

    :deep(.el-menu) {
      border-right: none;
    }
  }

  &--collapsed &__scroll {
    :deep(.el-menu--collapse) {
      --el-menu-base-level-padding: 0px;
      width: 100% !important;

      .el-menu-item,
      .el-sub-menu__title {
        justify-content: center;
        padding-inline: 0 !important;
      }

      .el-menu-tooltip__trigger {
        justify-content: center;
        padding-inline: 0 !important;
      }
    }
  }

  &__toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 40px;
    cursor: pointer;
    border-top: 1px solid var(--el-border-color);
    color: var(--el-text-color-primary);
    transition: color 0.2s;

    &:hover {
      color: var(--el-color-primary);
    }
  }
}

.layout__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

.layout__content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
