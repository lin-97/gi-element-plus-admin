<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useScroll } from '@vueuse/core'
import { useChatConfigStore } from '../stores/useChatConfigStore'
import { useChatStore } from '../stores/useChatStore'
import ChatBubble from './ChatBubble.vue'

defineOptions({ name: 'ChatMessageList' })

const props = defineProps<{
  streaming?: boolean
  streamingMessageId?: string | null
}>()

const emit = defineEmits<{
  selectPrompt: [text: string]
  openSettings: []
}>()

const chatStore = useChatStore()
const configStore = useChatConfigStore()

const scrollRef = useTemplateRef<HTMLElement>('scrollRef')
const { y } = useScroll(scrollRef, { behavior: 'smooth' })

const examplePrompts = [
  '解释 Vue 3 响应式原理',
  '写一个 JavaScript 快排算法',
  '二次方程求根公式 $x=\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}$ 是什么？',
]

const messages = computed(() => chatStore.currentSession?.messages ?? [])

watch(
  () => [messages.value.length, messages.value.at(-1)?.content, props.streaming],
  async () => {
    await nextTick()
    if (scrollRef.value)
      y.value = scrollRef.value.scrollHeight
  },
)

function handlePrompt(text: string) {
  emit('selectPrompt', text)
}
</script>

<template>
  <div ref="scrollRef" class="chat-message-list">
    <div v-if="!configStore.isConfigured" class="chat-message-list__guide">
      <Icon icon="icon-park-outline:key" width="48" class="chat-message-list__guide-icon" />
      <h3>请先配置 API Key</h3>
      <p>在设置中填写 DeepSeek API Key 后即可开始对话。</p>
      <el-button type="primary" @click="emit('openSettings')">
        打开设置
      </el-button>
    </div>

    <div v-else-if="!messages.length" class="chat-message-list__welcome">
      <h3>开始新的对话</h3>
      <p>你可以尝试以下问题：</p>
      <div class="chat-message-list__prompts">
        <button
          v-for="item in examplePrompts"
          :key="item"
          type="button"
          class="chat-message-list__prompt"
          @click="handlePrompt(item)"
        >
          {{ item }}
        </button>
      </div>
    </div>

    <div v-else class="chat-message-list__content">
      <div
        v-for="message in messages"
        :key="message.id"
        class="chat-message-list__item"
      >
        <ChatBubble
          :message-id="message.id"
          :role="message.role === 'user' ? 'user' : 'assistant'"
          :content="message.content"
          :streaming="props.streaming && message.id === props.streamingMessageId"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-message-list {
  height: 100%;
  overflow-y: auto;
  padding: 72px 20px
    calc(var(--ai-chat-input-bottom, 20px) + var(--ai-chat-input-height, 168px) + var(--ai-chat-input-gap, 24px));

  &__guide,
  &__welcome {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100%;
    text-align: center;
    gap: 12px;
    color: var(--el-text-color-regular);

    h3 {
      margin: 0;
      font-size: 20px;
      color: var(--el-text-color-primary);
    }

    p {
      margin: 0;
      max-width: 420px;
      line-height: 1.6;
    }
  }

  &__guide-icon {
    color: var(--ai-chat-accent);
  }

  &__prompts {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-top: 8px;
    max-width: 720px;
  }

  &__prompt {
    padding: 10px 14px;
    border: 1px solid var(--el-border-color);
    border-radius: 999px;
    background: var(--el-bg-color);
    color: var(--el-text-color-primary);
    cursor: pointer;
    transition:
      border-color 0.2s ease,
      background-color 0.2s ease,
      color 0.2s ease;

    &:hover {
      border-color: var(--ai-chat-accent);
      color: var(--ai-chat-accent);
      background: color-mix(in srgb, var(--ai-chat-accent) 8%, transparent);
    }
  }

  &__content {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 960px;
    margin: 0 auto;
  }

  &__item {
    width: 100%;
  }
}
</style>
