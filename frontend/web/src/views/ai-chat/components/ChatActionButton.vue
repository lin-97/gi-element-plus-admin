<script setup lang="ts">
import { Icon } from '@iconify/vue'

defineOptions({ name: 'ChatActionButton' })

const props = defineProps<{
  variant: 'send' | 'stop'
  disabled?: boolean
}>()

const emit = defineEmits<{
  click: []
}>()

const label = computed(() => (props.variant === 'send' ? '发送' : '停止'))

const icon = computed(() => (
  props.variant === 'send' ? 'icon-park-outline:send' : 'icon-park-outline:pause-one'
))

function handleClick() {
  if (props.disabled)
    return
  emit('click')
}
</script>

<template>
  <button
    type="button"
    class="chat-action-btn"
    :class="[
      `chat-action-btn--${props.variant}`,
      { 'is-disabled': props.disabled },
    ]"
    :disabled="props.disabled"
    :aria-label="label"
    @click="handleClick"
  >
    <span v-if="props.variant === 'stop'" class="chat-action-btn__ripple" aria-hidden="true" />
    <span v-if="props.variant === 'stop'" class="chat-action-btn__glow" aria-hidden="true" />
    <Icon :icon="icon" width="16" height="16" class="chat-action-btn__icon" />
    <span class="chat-action-btn__label">{{ label }}</span>
  </button>
</template>

<style scoped lang="scss">
.chat-action-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-width: 88px;
  height: 36px;
  padding: 0 16px;
  border: none;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1;
  color: #fff;
  cursor: pointer;
  overflow: visible;
  transition:
    box-shadow 0.2s ease,
    filter 0.2s ease,
    opacity 0.2s ease;

  &__icon {
    flex-shrink: 0;
  }

  &__label {
    position: relative;
    z-index: 1;
  }

  &--send {
    background: linear-gradient(135deg, #5856d6 0%, #7c3aed 100%);
    box-shadow: 0 4px 14px rgb(88 86 214 / 35%);

    &:hover:not(.is-disabled) {
      box-shadow: 0 6px 20px rgb(88 86 214 / 45%);
      filter: brightness(1.05);
    }

    &:active:not(.is-disabled) {
      box-shadow: 0 2px 8px rgb(88 86 214 / 30%);
      filter: brightness(0.98);
    }
  }

  &--stop {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    box-shadow: 0 4px 14px rgb(239 68 68 / 35%);
    animation: chat-action-stop-enter 0.35s ease;

    &:hover {
      box-shadow: 0 6px 20px rgb(239 68 68 / 45%);
      filter: brightness(1.05);
    }

    &:active {
      box-shadow: 0 2px 8px rgb(239 68 68 / 30%);
      filter: brightness(0.98);
    }
  }

  &__ripple {
    position: absolute;
    inset: -3px;
    border-radius: inherit;
    border: 2px solid rgb(239 68 68 / 55%);
    animation: chat-action-ripple 1.6s ease-out infinite;
    pointer-events: none;
  }

  &__glow {
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: rgb(239 68 68 / 25%);
    animation: chat-action-glow 1.6s ease-in-out infinite;
    pointer-events: none;
  }

  &.is-disabled {
    opacity: 0.45;
    cursor: not-allowed;
    box-shadow: none;
    filter: none;
  }
}

@keyframes chat-action-stop-enter {
  from {
    opacity: 0;
    transform: scale(0.92);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes chat-action-ripple {
  0% {
    transform: scale(1);
    opacity: 0.7;
  }

  100% {
    transform: scale(1.18);
    opacity: 0;
  }
}

@keyframes chat-action-glow {
  0%,
  100% {
    opacity: 0.3;
  }

  50% {
    opacity: 0.55;
  }
}

@media (prefers-reduced-motion: reduce) {
  .chat-action-btn--stop {
    animation: none;
  }

  .chat-action-btn__ripple,
  .chat-action-btn__glow {
    animation: none !important;
  }
}
</style>
