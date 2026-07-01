import type { ApiChatMessage, ChatConfig } from '../types'
import { tryOnScopeDispose, useToggle } from '@vueuse/core'
import { chatStreamApi } from '../apis/chat'

export function useChatStream() {
  const error = ref<string | null>(null)
  const [isStreaming, toggleStreaming] = useToggle(false)
  let abortController: AbortController | null = null

  async function send(
    config: ChatConfig,
    messages: ApiChatMessage[],
    onChunk: (text: string) => void,
  ) {
    error.value = null
    abortController = new AbortController()
    toggleStreaming(true)

    try {
      await chatStreamApi(
        config,
        messages,
        onChunk,
        abortController.signal,
      )
    }
    catch (e) {
      if ((e as Error).name !== 'AbortError')
        error.value = (e as Error).message || '请求失败'
      throw e
    }
    finally {
      toggleStreaming(false)
      abortController = null
    }
  }

  function abort() {
    abortController?.abort()
  }

  tryOnScopeDispose(() => {
    abort()
  })

  return {
    error,
    isStreaming,
    send,
    abort,
  }
}
