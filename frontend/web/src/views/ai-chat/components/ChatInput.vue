<script setup lang="ts">
import ChatActionButton from './ChatActionButton.vue'

defineOptions({ name: 'ChatInput' })

const props = defineProps<{
  disabled?: boolean
  loading?: boolean
}>()

const emit = defineEmits<{
  send: [text: string]
  stop: []
}>()

const input = ref('')
const isFocused = ref(false)

const canSend = computed(() => {
  return !props.disabled && !props.loading && input.value.trim().length > 0
})

function handleSend() {
  const text = input.value.trim()
  if (!canSend.value)
    return
  emit('send', text)
  input.value = ''
}

function handleKeydown(event: Event | KeyboardEvent) {
  if (!(event instanceof KeyboardEvent))
    return

  if (event.key === 'Enter' && (event.ctrlKey || event.metaKey))
    return

  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}

function handleStop() {
  emit('stop')
}

function handleFocusIn() {
  isFocused.value = true
}

function handleFocusOut() {
  isFocused.value = false
}
</script>

<template>
  <div class="chat-input">
    <div
      class="chat-input__frame"
      :class="{ 'is-focused': isFocused }"
      @focusin="handleFocusIn"
      @focusout="handleFocusOut"
    >
      <div class="chat-input__inner">
        <el-input
          v-model="input"
          type="textarea"
          :rows="3"
          resize="none"
          :disabled="props.disabled || props.loading"
          placeholder="输入消息，Enter 发送，Ctrl + Enter 换行"
          @keydown="handleKeydown"
        />
        <div class="chat-input__actions">
          <span class="chat-input__hint">Enter 发送 · Ctrl + Enter 换行</span>
          <Transition name="chat-action-switch" mode="out-in">
            <ChatActionButton
              v-if="props.loading"
              key="stop"
              variant="stop"
              @click="handleStop"
            />
            <ChatActionButton
              v-else
              key="send"
              variant="send"
              :disabled="!canSend"
              @click="handleSend"
            />
          </Transition>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-input {
  padding: 0;

  &__frame {
    position: relative;
    max-width: 960px;
    margin: 0 auto;
    border-radius: 16px;

    &::before {
      content: '';
      position: absolute;
      inset: 0;
      border-radius: inherit;
      padding: 2px;
      background: linear-gradient(135deg, #5856d6, #22c55e, #f59e0b, #ef4444, #ec4899, #8b5cf6, #5856d6);
      mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
      mask-composite: exclude;
      -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      opacity: 0;
      pointer-events: none;
      z-index: 0;
      transition: opacity 0.2s ease;
    }

    &.is-focused::before {
      opacity: 1;
    }
  }

  &__inner {
    position: relative;
    z-index: 1;
    padding: 12px 16px;
    border-radius: 16px;
    border: 1px solid var(--ai-chat-glass-border);
    background: var(--ai-chat-panel-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: var(--ai-chat-glass-shadow);
    transition:
      box-shadow 0.2s ease,
      transform 0.2s ease,
      border-color 0.2s ease;
  }

  &__frame.is-focused &__inner {
    border-color: transparent;
    box-shadow: var(--ai-chat-glass-shadow-hover);
    transform: translateY(-2px);
  }

  &__actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 12px;
    gap: 12px;
  }

  &__hint {
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }

  :deep(.el-textarea__inner) {
    border: none;
    box-shadow: none;
    background: transparent;
    padding: 0;
    resize: none;
  }
}

.chat-action-switch-enter-active,
.chat-action-switch-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.chat-action-switch-enter-from {
  opacity: 0;
  transform: translateY(4px) scale(0.96);
}

.chat-action-switch-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.96);
}

@media (prefers-reduced-motion: reduce) {
  .chat-action-switch-enter-active,
  .chat-action-switch-leave-active {
    transition: none;
  }
}
</style>
