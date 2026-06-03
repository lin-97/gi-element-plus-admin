<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useUserStore } from '@/stores/useUserStore'

defineOptions({ name: 'MessageCard' })

const userStore = useUserStore()

const displayName = computed(
  () => userStore.userInfo?.nickname || userStore.userInfo?.username || '管理员',
)

const messages = [
  {
    type: '活动',
    tagType: 'warning' as const,
    content: '内容最新优惠活动',
    time: '5分钟前',
  },
  {
    type: '消息',
    tagType: 'success' as const,
    content: '新增内容尚未通过审核，详情请点击查看。',
    time: '半小时前',
  },
  {
    type: '通知',
    tagType: 'primary' as const,
    content: '当前产品试用期即将结束，如需续费请点击查看。',
    time: '1小时前',
  },
  {
    type: '通知',
    tagType: 'primary' as const,
    content: '1月新系统升级计划通知',
    time: '1天前',
  },
  {
    type: '消息',
    tagType: 'success' as const,
    content: '完成系统升级计划通知',
    time: '2天前',
  },
]
</script>

<template>
  <gi-card class="message-card">
    <template #title>
      <span>消息</span>
    </template>
    <template #extra>
      <el-link type="primary" :underline="false">
        更多
      </el-link>
    </template>
    <div class="message-card__list">
      <div
        v-for="(item, index) in messages"
        :key="index"
        class="message-card__item"
      >
        <el-avatar :size="40" :src="userStore.userInfo?.avatar ?? undefined">
          <Icon icon="icon-park-outline:user" width="20" height="20" />
        </el-avatar>
        <div class="message-card__body">
          <div class="message-card__user">
            {{ displayName }}
          </div>
          <div class="message-card__content">
            <el-tag :type="item.tagType" size="small" effect="plain">
              {{ item.type }}
            </el-tag>
            <span>{{ item.content }}</span>
          </div>
        </div>
        <span class="message-card__time">{{ item.time }}</span>
      </div>
    </div>
  </gi-card>
</template>

<style lang="scss" scoped>
.message-card {
  &__list {
    display: flex;
    flex-direction: column;
  }

  &__item {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 14px 0;
    border-bottom: 1px solid var(--el-border-color-lighter);

    &:last-child {
      border-bottom: none;
    }
  }

  &__body {
    flex: 1;
    min-width: 0;
  }

  &__user {
    margin-bottom: 6px;
    font-size: 14px;
    font-weight: 500;
    color: var(--el-text-color-primary);
  }

  &__content {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    font-size: 13px;
    line-height: 1.5;
    color: var(--el-text-color-regular);

    span:last-child {
      flex: 1;
      min-width: 0;
    }
  }

  &__time {
    flex-shrink: 0;
    font-size: 12px;
    color: var(--el-text-color-placeholder);
    white-space: nowrap;
  }
}
</style>
