export type ChatRole = 'user' | 'assistant' | 'system'

export interface ChatMessage {
  id: string
  role: ChatRole
  content: string
  createdAt: number
}

export interface ChatSession {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: number
  updatedAt: number
}

export interface ChatConfig {
  apiKey: string
  baseUrl: string
  model: string
  systemPrompt: string
  providerId?: string
}

export interface ApiChatMessage {
  role: ChatRole
  content: string
}
