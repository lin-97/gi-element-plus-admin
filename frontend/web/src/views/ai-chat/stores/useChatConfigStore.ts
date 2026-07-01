import { defineStore } from 'pinia'
import { getChatProvider, normalizeModelSlug } from '../providers'

const DEFAULT_SYSTEM_PROMPT = '你是专业、友好的 AI 助手。请使用 Markdown 回答，代码块标注语言，数学公式使用 LaTeX。'

export const useChatConfigStore = defineStore(
  'ai-chat-config',
  () => {
    const providerId = ref('openrouter-free')
    const apiKey = ref('')
    const baseUrl = ref('https://openrouter.ai/api/v1')
    const model = ref('openrouter/free')
    const systemPrompt = ref(DEFAULT_SYSTEM_PROMPT)

    const currentProvider = computed(() => getChatProvider(providerId.value))

    const isConfigured = computed(() => apiKey.value.trim().length > 0)

    function applyProvider(id: string) {
      const provider = getChatProvider(id)
      providerId.value = provider.id
      baseUrl.value = provider.baseUrl
      model.value = provider.model
    }

    function getConfig() {
      return {
        apiKey: apiKey.value.replace(/\s/g, '').trim(),
        baseUrl: baseUrl.value.trim() || currentProvider.value.baseUrl,
        model: normalizeModelSlug(model.value.trim() || currentProvider.value.model),
        systemPrompt: systemPrompt.value.trim() || DEFAULT_SYSTEM_PROMPT,
        providerId: providerId.value,
      }
    }

    return {
      providerId,
      apiKey,
      baseUrl,
      model,
      systemPrompt,
      currentProvider,
      isConfigured,
      applyProvider,
      getConfig,
    }
  },
  {
    persist: {
      key: 'ai-chat-config',
    },
  },
)
