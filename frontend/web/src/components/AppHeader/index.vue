<script setup lang="ts">
import {
  Expand,
  Fold,
  FullScreen,
  Moon,
  Sunny,
  SwitchButton,
  User,
} from '@element-plus/icons-vue'
import { useFullscreen } from '@vueuse/core'
import { ElMessageBox, ElSpace } from 'element-plus'
import { appConfig } from '@/config'
import { useBreadcrumb, useTheme } from '@/core/hooks'
import { useAppStore } from '@/core/stores'
import { useUserStore } from '@/stores/modules/user'

interface Props {
  /** 顶栏模式 */
  mode?: 'side' | 'top'
}

withDefaults(defineProps<Props>(), {
  mode: 'side',
})

const router = useRouter()
const appStore = useAppStore()
const { isDark, toggleDark } = useTheme()
const userStore = useUserStore()
const fullscreenTarget = ref(document.documentElement)
const { toggle: toggleFullscreen } = useFullscreen(fullscreenTarget)
const { breadcrumbs } = useBreadcrumb()

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
  <header class="app-header">
    <div class="app-header__left">
      <el-button
        v-if="mode === 'side'"
        type="primary"
        bg
        text
        circle
        :icon="appStore.isMenuAccordion ? Expand : Fold"
        @click="appStore.setMenuCollapse(!appStore.isMenuAccordion)"
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
    </div>
    <div class="app-header__right">
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
        <el-dropdown trigger="click">
          <span class="app-header__user">
            <el-avatar :size="28" :src="userStore.userInfo?.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <span>{{ userStore.userInfo?.nickname || '用户' }}</span>
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
    </div>
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

  &__left,
  &__right {
    display: flex;
    align-items: center;
  }

  &__left {
    gap: 12px;
  }

  &__user {
    display: flex;
    gap: 8px;
    align-items: center;
    cursor: pointer;
  }
}
</style>
