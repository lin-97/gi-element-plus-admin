<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { breakpointsTailwind, useBreakpoints, useFullscreen } from '@vueuse/core'
import { ElMessageBox } from 'element-plus'
import AppBreadcrumb from '@/components/AppBreadcrumb/index.vue'
import AppMenuItem from '@/components/AppMenuItem/index.vue'
import AppMenuToggle from '@/components/AppMenuToggle/index.vue'
import { openAppSettingDrawer } from '@/components/AppSettingDrawer/open'
import { appConfig } from '@/config'
import { useTheme } from '@/core/hooks'
import { useAppStore } from '@/core/stores'
import { useMenu } from '@/hooks/useMenu'
import { useUserStore } from '@/stores/useUserStore'

defineOptions({ name: 'AppHeader' })

const { mode = 'default' } = defineProps<{
  mode?: 'default' | 'top'
}>()

const router = useRouter()
const appStore = useAppStore()
const { isDark, toggleDark } = useTheme()
const userStore = useUserStore()
const { isFullscreen, toggle: toggleFullscreen } = useFullscreen()
const { menuList, selectedKeys, handleMenuItemClick } = useMenu()

const isTopMode = computed(() => mode === 'top')

const breakpoints = useBreakpoints(breakpointsTailwind)
const isXsScreen = breakpoints.smaller('sm')
const isMdScreen = breakpoints.smaller('md')

async function handleLogout() {
  await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
  await userStore.logout()
  router.push(appConfig.loginPath)
}
</script>

<template>
  <header
    class="app-header"
    :class="{
      'app-header--top': isTopMode,
      'g-area-dark': isTopMode && appStore.isMenuDark,
    }"
  >
    <div class="app-header__left">
      <template v-if="isTopMode">
        <span v-if="!isMdScreen" class="app-header__logo app__logo">GI Admin</span>
        <AppMenuToggle v-if="isMdScreen" />
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
        <AppBreadcrumb v-if="!isXsScreen" />
      </template>
    </div>

    <el-space :size="8">
      <el-space :size="4">
        <el-tooltip v-if="!isXsScreen" :content="isFullscreen ? '退出全屏' : '全屏'">
          <el-button class="g-square-button" type="primary" text circle @click="toggleFullscreen">
            <Icon
              :icon="isFullscreen ? 'custom:off-screen' : 'custom:full-screen'"
              width="18"
              height="18"
            />
          </el-button>
        </el-tooltip>
        <el-tooltip :content="isDark ? '亮色模式' : '暗黑模式'">
          <el-button
            class="g-square-button"
            type="primary"
            text
            circle
            @click="toggleDark()"
          >
            <Icon
              :icon="!isDark ? 'custom:sun-fill' : 'custom:moon-fill'"
              width="18"
              height="18"
            />
          </el-button>
        </el-tooltip>
        <el-tooltip content="系统设置">
          <el-button
            class="g-square-button"
            type="primary"
            text
            circle
            @click="openAppSettingDrawer()"
          >
            <Icon icon="custom:setting" width="18" height="18" />
          </el-button>
        </el-tooltip>
      </el-space>
      <el-dropdown trigger="click">
        <span class="app-header__user">
          <el-avatar :size="28" :src="userStore.userInfo?.avatar ?? undefined">
            <Icon icon="icon-park-outline:user" width="18" height="18" />
          </el-avatar>
          <span class="app-header__user-name">{{ userStore.userInfo?.nickname || '用户' }}</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <template #icon>
                <Icon icon="icon-park-outline:avatar" width="16" height="16" />
              </template>
              个人中心
            </el-dropdown-item>
            <el-dropdown-item @click="handleLogout">
              <template #icon>
                <Icon icon="icon-park-outline:power" width="16" height="16" />
              </template>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-space>
  </header>
</template>

<style lang="scss" scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 50px;
  padding: 0 16px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color);

  &--top {
    height: auto;
    min-height: 50px;
    flex-wrap: wrap;
  }

  &__left {
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

  &__user {
    display: flex;
    gap: 8px;
    align-items: center;
    cursor: pointer;

    &-name {
      font-weight: 500;
    }
  }
}
.el-button--primary.is-text {
  --el-button-text-color: var(--el-text-color-primary);
}
</style>
