<script setup lang="ts">
import { Icon } from '@iconify/vue'
import Dayjs from 'dayjs'
import { useUserStore } from '@/stores/useUserStore'

defineOptions({ name: 'WelcomeCard' })

const userStore = useUserStore()

const displayName = computed(
  () => userStore.userInfo?.nickname || userStore.userInfo?.username || '管理员',
)

const greeting = computed(() => {
  const hour = Dayjs().hour()
  if (hour < 12)
    return '上午好'
  if (hour < 18)
    return '下午好'
  return '晚上好'
})

interface HeaderStatItem {
  title: string
  value?: number
  displayValue?: string
  icon: string
  color: string
}

const headerStats: HeaderStatItem[] = [
  {
    title: '项目数',
    value: 16,
    icon: 'icon-park-outline:peoples',
    color: '#14c9c9',
  },
  {
    title: '待办',
    value: 8,
    icon: 'icon-park-outline:time',
    color: '#3491fa',
  },
  {
    title: '消息',
    value: 35,
    icon: 'icon-park-outline:message-one',
    color: '#00b42a',
  },
]
</script>

<template>
  <gi-card class="welcome-card" :header-style="{ display: 'none' }">
    <div class="welcome-card__inner">
      <div class="welcome-card__info">
        <el-avatar :size="60" :src="userStore.userInfo?.avatar ?? undefined" class="welcome-card__avatar">
          <Icon icon="icon-park-outline:user" width="36" height="36" />
        </el-avatar>
        <div class="welcome-card__text">
          <div class="welcome-card__title">
            <span>{{ greeting }}！{{ displayName }}，开始您一天的工作吧！</span>
          </div>
          <p class="welcome-card__tip">
            今日阴转大雨，15℃ - 25℃，出门记得带伞哦。
          </p>
        </div>
      </div>
      <div class="welcome-card__stats">
        <div
          v-for="item in headerStats"
          :key="item.title"
          class="welcome-card__stat-item"
        >
          <span
            class="welcome-card__stat-icon"
            :style="{ backgroundColor: `${item.color}20`, color: item.color }"
          >
            <Icon :icon="item.icon" width="18" height="18" />
          </span>
          <el-statistic
            v-if="item.value !== undefined"
            :title="item.title"
            :value="item.value"
          />
          <el-statistic v-else :title="item.title">
            <template #default>
              {{ item.displayValue }}
            </template>
          </el-statistic>
        </div>
      </div>
    </div>
  </gi-card>
</template>

<style lang="scss" scoped>
.welcome-card {
  &__inner {
    padding: 20px 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    align-items: center;
    justify-content: space-between;
  }

  &__info {
    display: flex;
    flex: 1;
    gap: 20px;
    align-items: center;
    min-width: 280px;
  }

  &__avatar {
    flex-shrink: 0;
  }

  &__text {
    flex: 1;
    min-width: 0;
  }

  &__title {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    margin-bottom: 8px;
    font-size: 18px;
    line-height: 1.4;
    color: var(--el-text-color-primary);
  }

  &__tip {
    margin: 0;
    font-size: 14px;
    color: var(--el-text-color-secondary);
  }

  &__stats {
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
    align-items: center;
    justify-content: flex-end;
  }

  &__stat-item {
    display: flex;
    gap: 12px;
    align-items: center;

    :deep(.el-statistic__head) {
      margin-bottom: 4px;
      font-size: 13px;
    }

    :deep(.el-statistic__number) {
      font-size: 22px;
      font-weight: 600;
    }
  }

  &__stat-icon {
    display: inline-flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}

@media (width <= 992px) {
  .welcome-card__stats {
    justify-content: flex-start;
    width: 100%;
  }
}
</style>
