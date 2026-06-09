<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ref } from 'vue'

defineOptions({ name: 'AppNoticeDrawer' })

const emit = defineEmits<{
  (e: 'closed'): void
}>()

interface NoticeItem {
  id: number
  title: string
  message: string
  type: 'success' | 'warning' | 'error' | 'info'
  time: string
}

const EXIT_ANIMATION_MS = 500
const CLEAR_STAGGER_MS = 80

const notices = ref<NoticeItem[]>([
  {
    id: 1,
    title: '系统更新',
    message: '系统已完成更新，新增多项功能',
    type: 'success',
    time: '2026-01-15 10:30',
  },
  {
    id: 2,
    title: '订单提醒',
    message: '您有新的订单待处理',
    type: 'warning',
    time: '2026-01-15 09:20',
  },
  {
    id: 3,
    title: '安全警告',
    message: '检测到异常登录尝试，请检查账户安全',
    type: 'error',
    time: '2026-01-15 08:45',
  },
  {
    id: 4,
    title: '消息通知',
    message: '您收到一条新消息',
    type: 'info',
    time: '2026-01-14 16:30',
  },
  {
    id: 5,
    title: '维护通知',
    message: '系统将于今晚22:00进行维护升级',
    type: 'warning',
    time: '2026-01-14 14:00',
  },
  {
    id: 6,
    title: '数据备份',
    message: '数据库备份已完成',
    type: 'success',
    time: '2026-01-14 10:00',
  },
  {
    id: 7,
    title: '存储告警',
    message: '服务器存储空间已使用80%，请及时清理',
    type: 'warning',
    time: '2026-01-13 15:30',
  },
  {
    id: 8,
    title: '登录通知',
    message: '您的账户在新设备上登录',
    type: 'info',
    time: '2026-01-13 09:15',
  },
  {
    id: 9,
    title: '权限变更',
    message: '您的账户权限已更新',
    type: 'success',
    time: '2026-01-12 14:20',
  },
  {
    id: 10,
    title: '证书即将过期',
    message: 'SSL证书将在7天后过期，请及时更新',
    type: 'error',
    time: '2026-01-12 11:00',
  },
])

const isClearingAll = ref(false)

function removeNotice(id: number) {
  if (isClearingAll.value)
    return
  notices.value = notices.value.filter(n => n.id !== id)
}

function clearAll() {
  const list = notices.value
  if (!list.length || isClearingAll.value)
    return

  isClearingAll.value = true
  setTimeout(() => {
    notices.value = []
    isClearingAll.value = false
  }, (list.length - 1) * CLEAR_STAGGER_MS + EXIT_ANIMATION_MS)
}

onUnmounted(() => {
  emit('closed')
})

defineExpose({ clearAll })
</script>

<template>
  <div class="app-notice-drawer">
    <div
      v-for="(notice, index) in notices"
      :key="notice.id"
      class="app-notice-drawer__item"
      :class="{
        'app-notice-drawer__item--removing animate__animated animate__fadeOutRight animate__faster': isClearingAll,
      }"
      :style="isClearingAll ? { '--remove-delay': `${index * CLEAR_STAGGER_MS}ms` } : undefined"
    >
      <el-alert
        :title="notice.title"
        :type="notice.type"
        :closable="true"
        show-icon
        @close="removeNotice(notice.id)"
      >
        <template #default>
          <div>{{ notice.message }}</div>
          <div class="app-notice-drawer__time">
            {{ notice.time }}
          </div>
        </template>
        <template #close>
          <Icon icon="icon-park-outline:close" width="16" height="16" />
        </template>
      </el-alert>
    </div>

    <el-empty v-if="notices.length === 0" description="暂无通知" :image-size="80" />
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-alert) {
  --el-alert-icon-large-size: 18px;
}

:deep(.el-alert__title.with-description) {
  font-size: 14px;
  font-weight: 600;
}

.app-notice-drawer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
}

.app-notice-drawer__item {
  &--removing {
    animation-delay: var(--remove-delay, 0ms);
    pointer-events: none;
  }
}

.app-notice-drawer__time {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 6px;
}
</style>
