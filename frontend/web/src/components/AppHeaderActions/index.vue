<script setup lang="ts">
/**
 * 顶部右侧工具栏
 * 包含：全屏、暗黑模式、通知、设置、用户下拉
 */
import { Icon } from '@iconify/vue'
import { useFullscreen } from '@vueuse/core'
import { ElMessageBox } from 'element-plus'
import { openAppNoticeDrawer } from '@/components/AppNoticeDrawer/open'
import { openAppSettingDrawer } from '@/components/AppSettingDrawer/open'
import { appConfig } from '@/config'
import { useTheme } from '@/core/hooks'
import { useResponsive } from '@/hooks/useResponsive'
import { useUserStore } from '@/stores/useUserStore'

defineOptions({ name: 'AppHeaderActions' })

const router = useRouter()
const { isDark, toggleDark } = useTheme()
const userStore = useUserStore()
const { isFullscreen, toggle: toggleFullscreen } = useFullscreen()
const { isXs } = useResponsive()

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
  <el-space :size="8">
    <el-space :size="4">
      <el-tooltip v-if="!isXs" :content="isFullscreen ? '退出全屏' : '全屏'">
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
      <el-tooltip content="通知中心">
        <el-badge :value="8" type="success" is-dot :offset="[-4, 8]">
          <el-button
            class="g-square-button"
            type="primary"
            text
            circle
            @click="openAppNoticeDrawer"
          >
            <Icon icon="custom:notice" width="18" height="18" />
          </el-button>
        </el-badge>
      </el-tooltip>
      <el-tooltip content="系统设置">
        <el-button
          class="g-square-button"
          type="primary"
          text
          circle
          @click="openAppSettingDrawer"
        >
          <Icon icon="custom:setting" width="18" height="18" />
        </el-button>
      </el-tooltip>
    </el-space>
    <el-dropdown trigger="click">
      <span class="app-header-actions__user">
        <el-avatar :size="28" :src="userStore.userInfo?.avatar ?? undefined">
          <Icon icon="icon-park-outline:user" width="18" height="18" />
        </el-avatar>
        <span class="app-header-actions__user-name">{{ userStore.userInfo?.nickname || '用户' }}</span>
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
</template>

<style lang="scss" scoped>
  :deep(.el-button--primary.is-text) {
  --el-button-text-color: var(--el-text-color-primary);
}
.app-header-actions__user {
  display: flex;
  gap: 8px;
  align-items: center;
  cursor: pointer;

  &-name {
    font-weight: 500;
  }
}
</style>
