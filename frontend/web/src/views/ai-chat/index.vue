<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useFullscreen, useResizeObserver } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import { appConfig } from '@/config'
import { useTheme } from '@/core/hooks'
import { useResponsive } from '@/hooks/useResponsive'
import ChatInput from './components/ChatInput.vue'
import ChatMessageList from './components/ChatMessageList.vue'
import ChatSettings from './components/ChatSettings.vue'
import ChatSidebar from './components/ChatSidebar.vue'
import { useChatStream } from './hooks/useChatStream'
import { normalizeModelSlug } from './providers'
import { useChatConfigStore } from './stores/useChatConfigStore'
import { useChatStore } from './stores/useChatStore'
import { initChatMarkdownRuntime } from './utils/markdown'
import './styles/index.scss'

defineOptions({ name: 'AiChat' })

const router = useRouter()
const chatStore = useChatStore()
const configStore = useChatConfigStore()
const { isStreaming, send, abort, error } = useChatStream()
const { isDark, toggleDark } = useTheme()
const { isFullscreen, toggle: toggleFullscreen } = useFullscreen()
const { isMobile } = useResponsive()

const settingsVisible = ref(false)
const sidebarDrawerVisible = ref(false)
const streamingMessageId = ref<string | null>(null)
const inputAreaRef = useTemplateRef<HTMLElement>('inputAreaRef')
const inputAreaHeight = ref(0)

const mainStyle = computed(() => ({
  '--ai-chat-input-height': `${inputAreaHeight.value}px`,
}))

useResizeObserver(inputAreaRef, (entries) => {
  const entry = entries[0]
  inputAreaHeight.value = entry ? Math.ceil(entry.contentRect.height) : 0
})

const currentTitle = computed(() => chatStore.currentSession?.title || '新对话')

onBeforeMount(() => {
  void initChatMarkdownRuntime()
})

onMounted(() => {
  const normalized = normalizeModelSlug(configStore.model)

  if (normalized !== configStore.model) {
    configStore.applyProvider('openrouter-free')
    configStore.model = normalized
  }

  if (!chatStore.currentSessionId && !chatStore.sortedSessions.length)
    chatStore.createSession()
  else if (!chatStore.currentSessionId && chatStore.sortedSessions.length)
    chatStore.selectSession(chatStore.sortedSessions[0].id)
})

watch(error, (value) => {
  if (value)
    ElMessage.error(value)
})

function goBack() {
  router.push(appConfig.homePath)
}

function openSettings() {
  settingsVisible.value = true
}

function openSidebarDrawer() {
  sidebarDrawerVisible.value = true
}

function closeSidebarDrawer() {
  sidebarDrawerVisible.value = false
}

async function handleSend(text: string) {
  if (!configStore.isConfigured) {
    ElMessage.warning('请先配置 API Key')
    settingsVisible.value = true
    return
  }

  if (isStreaming.value)
    return

  chatStore.ensureCurrentSession()
  chatStore.addMessage('user', text)
  const assistantMessage = chatStore.addMessage('assistant', '')
  streamingMessageId.value = assistantMessage.id

  const config = configStore.getConfig()
  const messages = chatStore.buildApiMessages(config.systemPrompt)

  try {
    await send(config, messages, (chunk) => {
      chatStore.appendToMessage(assistantMessage.id, chunk)
    })
  }
  catch (e) {
    if ((e as Error).name === 'AbortError')
      return

    const errMsg = (e as Error).message || error.value || '请求失败'
    if (!assistantMessage.content.trim()) {
      chatStore.appendToMessage(assistantMessage.id, `请求失败：${errMsg}`)
    }
  }
  finally {
    streamingMessageId.value = null
  }
}

function handleStop() {
  abort()
  streamingMessageId.value = null
}

function handleSelectPrompt(text: string) {
  handleSend(text)
}
</script>

<template>
  <div class="ai-chat-page">
    <div class="ai-chat">
      <ChatSidebar v-if="!isMobile" class="ai-chat__sidebar" />
      <div class="ai-chat__main" :style="mainStyle">
        <header class="ai-chat__header">
          <div class="ai-chat__header-start">
            <el-tooltip v-if="isMobile" content="对话历史">
              <el-button
                class="g-square-button ai-chat__icon-btn"
                type="primary"
                text
                circle
                @click="openSidebarDrawer"
              >
                <Icon icon="icon-park-outline:expand-left" width="18" height="18" />
              </el-button>
            </el-tooltip>
            <div class="ai-chat__title-wrap">
              <span class="ai-chat__title">AI 对话</span>
              <span class="ai-chat__session-title">{{ currentTitle }}</span>
            </div>
          </div>
          <div class="ai-chat__actions">
            <el-tooltip content="返回后台">
              <el-button
                class="g-square-button ai-chat__icon-btn"
                type="primary"
                text
                circle
                @click="goBack"
              >
                <Icon icon="icon-park-outline:back" width="18" height="18" />
              </el-button>
            </el-tooltip>
            <el-space :size="4">
              <el-tooltip :content="isFullscreen ? '退出全屏' : '全屏'">
                <el-button
                  class="g-square-button ai-chat__icon-btn"
                  type="primary"
                  text
                  circle
                  @click="toggleFullscreen()"
                >
                  <Icon
                    :icon="isFullscreen ? 'custom:off-screen' : 'custom:full-screen'"
                    width="18"
                    height="18"
                  />
                </el-button>
              </el-tooltip>
              <el-tooltip :content="isDark ? '亮色模式' : '暗黑模式'">
                <el-button
                  class="g-square-button ai-chat__icon-btn"
                  type="primary"
                  text
                  circle
                  @click="toggleDark()"
                >
                  <Icon
                    :icon="!isDark ? 'custom:sun-fill' : 'custom:moon-fill'"
                    width="18"
                    height="18"
                  />
                </el-button>
              </el-tooltip>
              <el-tooltip content="AI 对话设置">
                <el-button
                  class="g-square-button ai-chat__icon-btn"
                  type="primary"
                  text
                  circle
                  @click="openSettings"
                >
                  <Icon icon="custom:setting" width="18" height="18" />
                </el-button>
              </el-tooltip>
            </el-space>
          </div>
        </header>

        <ChatMessageList
          class="ai-chat__messages"
          :streaming="isStreaming"
          :streaming-message-id="streamingMessageId"
          @select-prompt="handleSelectPrompt"
          @open-settings="openSettings"
        />
        <div ref="inputAreaRef" class="ai-chat__input">
          <ChatInput
            :disabled="!configStore.isConfigured"
            :loading="isStreaming"
            @send="handleSend"
            @stop="handleStop"
          />
        </div>
      </div>
    </div>

    <ChatSettings v-model="settingsVisible" />

    <gi-drawer
      v-if="isMobile"
      v-model="sidebarDrawerVisible"
      class="ai-chat-sidebar-drawer"
      title="对话历史"
      direction="ltr"
      size="280px"
      :footer="false"
      destroy-on-close
    >
      <ChatSidebar @select="closeSidebarDrawer" @create="closeSidebarDrawer" />
    </gi-drawer>
  </div>
</template>

<style scoped lang="scss">
:deep(.ai-chat__icon-btn.el-button--primary.is-text) {
  --el-button-text-color: var(--el-text-color-primary);
}
</style>
