<script setup lang="ts">
import {
  Expand,
  Fold,
  FullScreen,
  Moon,
  Setting,
  Sunny,
  SwitchButton,
  User,
} from '@element-plus/icons-vue'
import { useFullscreen } from '@vueuse/core'
import { ElMessageBox, ElSpace } from 'element-plus'
import AppMenuItem from '@/components/AppMenuItem.vue'
import AppSettingDrawer from '@/components/AppSettingDrawer/index.vue'
import { appConfig } from '@/config'
import { useBreadcrumb, useTheme } from '@/core/hooks'
import { useAppStore } from '@/core/stores'
import { useMenu } from '@/hooks/useMenu'
import { useUserStore } from '@/stores/useUserStore'

const { mode = 'default' } = defineProps<{
  mode?: 'default' | 'top'
}>()

const router = useRouter()
const appStore = useAppStore()
const { isDark, toggleDark } = useTheme()
const userStore = useUserStore()
const { toggle: toggleFullscreen } = useFullscreen()
const { breadcrumbs } = useBreadcrumb()
const { menuList, selectedKeys, handleMenuItemClick } = useMenu()

const settingVisible = ref(false)
const isTopMode = computed(() => mode === 'top')

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
  <header class="app-header" :class="{ 'app-header--top': isTopMode }">
    <div class="app-header__left">
      <template v-if="isTopMode">
        <span class="app-header__logo">GI Admin</span>
        <el-menu
          mode="horizontal"
          :default-active="selectedKeys[0]"
          :unique-opened="appStore.isMenuAccordion"
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
        <el-button
          type="primary"
          bg
          text
          circle
          :icon="appStore.isMenuCollapse ? Expand : Fold"
          @click="appStore.setMenuCollapse(!appStore.isMenuCollapse)"
        />
        <el-breadcrumb v-if="breadcrumbs.length" separator="/">
          <el-breadcrumb-item
            v-for="item in breadcrumbs"
            :key="item.path"
            :to="item.to"
          >
            {{ item.title }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </template>
    </div>

    <ElSpace :size="8">
      <el-tooltip content="全屏">
        <el-button type="primary" bg text circle :icon="FullScreen" @click="toggleFullscreen" />
      </el-tooltip>
      <el-tooltip :content="isDark ? '亮色模式' : '暗黑模式'">
        <el-button
          type="primary"
          bg
          text
          circle
          :icon="isDark ? Sunny : Moon"
          @click="toggleDark()"
        />
      </el-tooltip>
      <el-tooltip content="系统设置">
        <el-button
          type="primary"
          bg
          text
          circle
          :icon="Setting"
          @click="settingVisible = true"
        />
      </el-tooltip>
      <el-dropdown trigger="click">
        <span class="app-header__user">
          <el-avatar :size="28" :src="userStore.userInfo?.avatar ?? undefined">
            <el-icon><User /></el-icon>
          </el-avatar>
          <span>{{ userStore.userInfo?.name || '用户' }}</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </ElSpace>

    <AppSettingDrawer v-model="settingVisible" />
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

    :deep(.el-menu-item),
    :deep(.el-sub-menu__title) {
      height: 50px;
      line-height: 50px;
    }
  }

  &__user {
    display: flex;
    gap: 8px;
    align-items: center;
    cursor: pointer;
  }
}

:deep(.el-button) {
  border-radius: 4px;
}
</style>
