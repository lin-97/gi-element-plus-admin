<script setup lang="ts">
// cspell:ignore katex
import MarkdownRender from 'markstream-vue'
import {
  CHAT_CODE_BLOCK_PROPS,
  CHAT_CODE_THEME,
  CHAT_MARKDOWN_LANGS,
  CHAT_PARSE_OPTIONS,
  initChatMarkdownRuntime,
} from '../utils/markdown'
import 'markstream-vue/index.css'
import 'katex/dist/katex.min.css'

defineOptions({ name: 'ChatBubble' })

const props = defineProps<{
  messageId: string
  role: 'user' | 'assistant'
  content: string
  streaming?: boolean
}>()

const markdownReady = ref(false)

onBeforeMount(async () => {
  await initChatMarkdownRuntime()
  markdownReady.value = true
})

const showWaiting = computed(() => {
  return props.role === 'assistant'
    && props.streaming
    && !props.content.trim()
})

/** 有正文后再挂载 Markdown，避免隐藏态初始化导致 Shiki 不生效 */
const showMarkdown = computed(() => {
  return props.role === 'assistant' && props.content.trim().length > 0
})

/** 流式结束切换 key，强制以 final 态重挂载并恢复高亮 */
const markdownRenderKey = computed(() => {
  return props.streaming
    ? `${props.messageId}:streaming`
    : `${props.messageId}:final`
})
</script>

<template>
  <div class="chat-bubble" :class="[`chat-bubble--${props.role}`]">
    <div v-if="props.role === 'user'" class="chat-bubble__user-text">
      {{ props.content }}
    </div>
    <div
      v-else
      class="chat-bubble__assistant"
      :class="{ 'chat-bubble__assistant--waiting': showWaiting }"
    >
      <MarkdownRender
        v-if="showMarkdown && markdownReady"
        :key="markdownRenderKey"
        :index-key="props.messageId"
        class="markstream-vue chat-bubble__markdown"
        mode="chat"
        code-renderer="shiki"
        :code-block-stream="true"
        :render-code-blocks-as-pre="false"
        :is-dark="false"
        :code-block-dark-theme="CHAT_CODE_THEME"
        :code-block-light-theme="CHAT_CODE_THEME"
        :code-block-props="CHAT_CODE_BLOCK_PROPS"
        :langs="CHAT_MARKDOWN_LANGS"
        :parse-options="CHAT_PARSE_OPTIONS"
        :content="props.content"
        :final="!props.streaming"
        :smooth-streaming="false"
        :fade="false"
        :batch-rendering="false"
      />
      <div v-if="showWaiting" class="chat-bubble__waiting" aria-label="AI 正在思考">
        <span class="chat-bubble__dot" />
        <span class="chat-bubble__dot" />
        <span class="chat-bubble__dot" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/markdown';

.chat-bubble {
  display: flex;
  width: 100%;

  &--user {
    justify-content: flex-end;
  }

  &--assistant {
    justify-content: flex-start;
  }

  &__user-text {
    max-width: min(80%, 720px);
    padding: 12px 16px;
    border-radius: 12px 12px 4px 12px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
    color: #fff;
    background: var(--ai-chat-user-bubble);
  }

  &__assistant {
    position: relative;
    max-width: min(92%, 860px);
    padding: 14px 18px;
    border-radius: 12px 12px 12px 4px;
    line-height: 1.6;
    background: var(--ai-chat-assistant-bubble);
    border: 1px solid var(--ai-chat-assistant-border);
    box-shadow: 0 1px 2px rgb(15 23 42 / 4%);

    &--waiting {
      min-height: 48px;
    }
  }

  &__waiting {
    display: flex;
    align-items: center;
    gap: 6px;
    min-height: 24px;
    padding: 2px 0;
  }

  &__dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--ai-chat-accent);
    opacity: 0.35;
    animation: chat-bubble-dot 1.2s ease-in-out infinite;

    &:nth-child(2) {
      animation-delay: 0.15s;
    }

    &:nth-child(3) {
      animation-delay: 0.3s;
    }
  }
}

@keyframes chat-bubble-dot {
  0%,
  80%,
  100% {
    opacity: 0.35;
    transform: translateY(0);
  }

  40% {
    opacity: 1;
    transform: translateY(-4px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .chat-bubble__dot {
    animation: none;
    opacity: 0.7;
  }
}
</style>
