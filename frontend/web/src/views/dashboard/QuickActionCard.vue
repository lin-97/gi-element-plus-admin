<script setup lang="ts">
import { Icon } from '@iconify/vue'

defineOptions({ name: 'QuickActionCard' })

const router = useRouter()

const quickActions = [
  { label: '主控台', icon: 'icon-park-outline:dashboard-one', color: '#3491fa', path: '/dashboard' },
  { label: '列表', icon: 'icon-park-outline:list', color: '#3491fa', path: '/crud/index' },
  { label: '表单', icon: 'icon-park-outline:form-one', color: '#3491fa', path: '/crud/index' },
  { label: '权限管理', icon: 'icon-park-outline:permissions', color: '#3491fa', path: '/system/role' },
  { label: '系统管理', icon: 'icon-park-outline:setting-two', color: '#3491fa', path: '/system/user' },
  { label: '消息', icon: 'icon-park-outline:remind', color: '#3491fa', path: '/dashboard' },
]

function handleQuickAction(path: string) {
  router.push(path)
}
</script>

<template>
  <GiCard title="快捷操作" class="quick-action-card">
    <el-row :gutter="12" style="gap: 12px 0;">
      <el-col
        v-for="item in quickActions"
        :key="item.label"
        :span="8"
      >
        <div
          class="quick-action-card__item"
          role="button"
          tabindex="0"
          @click="handleQuickAction(item.path)"
          @keydown.enter="handleQuickAction(item.path)"
        >
          <span
            class="quick-action-card__icon"
            :style="{ backgroundColor: `${item.color}18`, color: item.color }"
          >
            <Icon :icon="item.icon" width="24" height="24" />
          </span>
          <span class="quick-action-card__label">{{ item.label }}</span>
        </div>
      </el-col>
    </el-row>
  </GiCard>
</template>

<style lang="scss" scoped>
.quick-action-card {
  &__item {
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 8px;
    transition: background-color 0.2s;
  }

  &__icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
  }

  &__label {
    font-size: 13px;
    color: var(--el-text-color-primary);
  }
}
</style>
