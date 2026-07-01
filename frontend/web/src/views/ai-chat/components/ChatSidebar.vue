<script setup lang="ts">
import { Icon } from '@iconify/vue'
import Dayjs from 'dayjs'
import { Dialog } from 'gi-component'
import { useChatStore } from '../stores/useChatStore'

defineOptions({ name: 'ChatSidebar' })

const emit = defineEmits<{
  create: []
}>()

const chatStore = useChatStore()

function formatTime(timestamp: number) {
  return Dayjs(timestamp).format('MM-DD HH:mm')
}

function handleSelect(id: string) {
  chatStore.selectSession(id)
}

function handleCreate() {
  chatStore.createSession()
  emit('create')
}

function handleDelete(id: string, event: Event) {
  event.stopPropagation()
  Dialog.warning({
    title: '提示',
    content: '确定删除该对话吗？',
    okText: '删除',
    onBeforeOk: async () => {
      chatStore.deleteSession(id)
      return true
    },
  })
}
</script>

<template>
  <aside class="chat-sidebar">
    <div class="chat-sidebar__header">
      <el-button type="primary" class="ai-chat-accent-btn chat-sidebar__create" @click="handleCreate">
        <Icon icon="icon-park-outline:plus" width="18" />
        新建对话
      </el-button>
    </div>

    <el-scrollbar class="chat-sidebar__list">
      <div
        v-for="session in chatStore.sortedSessions"
        :key="session.id"
        class="chat-sidebar__item"
        :class="{ 'is-active': session.id === chatStore.currentSessionId }"
        @click="handleSelect(session.id)"
      >
        <div class="chat-sidebar__item-main">
          <div class="chat-sidebar__item-title">
            {{ session.title }}
          </div>
          <div class="chat-sidebar__item-time">
            {{ formatTime(session.updatedAt) }}
          </div>
        </div>
        <button
          type="button"
          class="chat-sidebar__delete"
          aria-label="删除对话"
          @click="handleDelete(session.id, $event)"
        >
          <Icon icon="icon-park-outline:delete" width="16" />
        </button>
      </div>

      <div v-if="!chatStore.sortedSessions.length" class="chat-sidebar__empty">
        暂无对话，点击上方新建
      </div>
    </el-scrollbar>
  </aside>
</template>

<style scoped lang="scss">
.chat-sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;

  &__header {
    padding: 16px;
    border-bottom: 1px solid var(--el-border-color-lighter);
  }

  &__create {
    width: 100%;
  }

  &__list {
    flex: 1;
    min-height: 0;
  }

  &__item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    cursor: pointer;
    border-left: 3px solid transparent;
    transition:
      background-color 0.2s ease,
      border-color 0.2s ease;

    &:hover {
      background: var(--el-fill-color-light);
    }

    &.is-active {
      background: var(--el-fill-color);
      border-left-color: var(--ai-chat-accent);
    }
  }

  &__item-main {
    flex: 1;
    min-width: 0;
  }

  &__item-title {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 14px;
  }

  &__item-time {
    margin-top: 4px;
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }

  &__delete {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    padding: 0;
    border: none;
    border-radius: 6px;
    color: var(--el-text-color-secondary);
    background: transparent;
    cursor: pointer;
    opacity: 0;
    transition:
      opacity 0.2s ease,
      background-color 0.2s ease,
      color 0.2s ease;

    &:hover {
      color: var(--el-color-danger);
      background: var(--el-color-danger-light-9);
    }
  }

  &__item:hover &__delete,
  &__item.is-active &__delete {
    opacity: 1;
  }

  &__empty {
    padding: 24px 16px;
    font-size: 13px;
    color: var(--el-text-color-secondary);
    text-align: center;
  }
}
</style>
