import type { ApiChatMessage, ChatMessage, ChatRole, ChatSession } from '../types'
import { defineStore } from 'pinia'

function createId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

function createMessage(role: ChatRole, content: string): ChatMessage {
  return {
    id: createId(),
    role,
    content,
    createdAt: Date.now(),
  }
}

function deriveTitle(messages: ChatMessage[]) {
  const firstUser = messages.find(item => item.role === 'user')
  if (!firstUser?.content.trim())
    return '新对话'
  return firstUser.content.trim().slice(0, 20)
}

export const useChatStore = defineStore(
  'ai-chat',
  () => {
    const sessions = ref<ChatSession[]>([])
    const currentSessionId = ref<string | null>(null)

    const currentSession = computed(() => {
      if (!currentSessionId.value)
        return null
      return sessions.value.find(item => item.id === currentSessionId.value) ?? null
    })

    const sortedSessions = computed(() => {
      return [...sessions.value].sort((a, b) => b.updatedAt - a.updatedAt)
    })

    function touchSession(session: ChatSession) {
      session.updatedAt = Date.now()
      session.title = deriveTitle(session.messages)
    }

    function createSession() {
      const session: ChatSession = {
        id: createId(),
        title: '新对话',
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now(),
      }
      sessions.value.unshift(session)
      currentSessionId.value = session.id
      return session
    }

    function selectSession(id: string) {
      if (sessions.value.some(item => item.id === id))
        currentSessionId.value = id
    }

    function deleteSession(id: string) {
      const index = sessions.value.findIndex(item => item.id === id)
      if (index === -1)
        return

      sessions.value.splice(index, 1)
      if (currentSessionId.value === id) {
        currentSessionId.value = sessions.value[0]?.id ?? null
      }
    }

    function ensureCurrentSession() {
      if (currentSession.value)
        return currentSession.value
      return createSession()
    }

    function addMessage(role: ChatRole, content: string) {
      const session = ensureCurrentSession()
      const message = createMessage(role, content)
      session.messages.push(message)
      touchSession(session)
      return message
    }

    function appendToMessage(messageId: string, chunk: string) {
      const session = currentSession.value
      if (!session)
        return

      const message = session.messages.find(item => item.id === messageId)
      if (!message)
        return

      message.content += chunk
      touchSession(session)
      sessions.value = [...sessions.value]
    }

    function buildApiMessages(systemPrompt: string): ApiChatMessage[] {
      const session = currentSession.value
      if (!session)
        return [{ role: 'system', content: systemPrompt }]

      return [
        { role: 'system', content: systemPrompt },
        ...session.messages
          .filter(item => (item.role === 'user' || item.role === 'assistant') && item.content.trim())
          .map(item => ({ role: item.role, content: item.content })),
      ]
    }

    return {
      sessions,
      currentSessionId,
      currentSession,
      sortedSessions,
      createSession,
      selectSession,
      deleteSession,
      ensureCurrentSession,
      addMessage,
      appendToMessage,
      buildApiMessages,
    }
  },
  {
    persist: {
      key: 'ai-chat-sessions',
    },
  },
)
