import type { ApiChatMessage, ChatConfig } from '../types'

const CHAT_COMPLETIONS_PATH = '/chat/completions'

function resolveChatUrl(baseUrl: string) {
  const normalized = baseUrl.replace(/\/$/, '')
  if (normalized.endsWith('/v1'))
    return `${normalized}${CHAT_COMPLETIONS_PATH}`
  return `${normalized}${CHAT_COMPLETIONS_PATH}`
}

function buildRequestHeaders(apiKey: string, baseUrl: string) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
  }

  if (baseUrl.includes('openrouter.ai')) {
    headers['HTTP-Referer'] = window.location.origin
    headers['X-Title'] = 'GI AI Chat'
  }

  return headers
}

function sanitizeApiKey(apiKey: string) {
  return apiKey.replace(/\s/g, '').trim()
}

function extractErrorMessage(payload: unknown, fallback: string) {
  if (!payload || typeof payload !== 'object')
    return fallback

  const data = payload as {
    error?: { message?: string }
    message?: string
  }

  return data.error?.message || data.message || fallback
}

function parseStreamPayload(payload: string) {
  if (payload === '[DONE]')
    return { done: true as const }

  const json = JSON.parse(payload) as {
    error?: { message?: string }
    choices?: Array<{ delta?: { content?: string }, finish_reason?: string | null }>
  }

  if (json.error?.message)
    throw new Error(json.error.message)

  const text = json.choices?.[0]?.delta?.content
  if (text)
    return { done: false as const, text }

  return { done: false as const }
}

export async function chatStreamApi(
  config: ChatConfig,
  messages: ApiChatMessage[],
  onChunk: (text: string) => void,
  signal?: AbortSignal,
) {
  const apiKey = sanitizeApiKey(config.apiKey)
  if (!apiKey)
    throw new Error('API Key 不能为空')

  const res = await fetch(resolveChatUrl(config.baseUrl), {
    method: 'POST',
    headers: buildRequestHeaders(apiKey, config.baseUrl),
    body: JSON.stringify({
      model: config.model,
      messages,
      stream: true,
    }),
    signal,
  })

  if (!res.ok) {
    const errPayload = await res.json().catch(() => null)
    throw new Error(extractErrorMessage(errPayload, `请求失败 (${res.status})`))
  }

  if (!res.body)
    throw new Error('响应体为空')

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  let receivedContent = false

  while (true) {
    const { done, value } = await reader.read()
    if (done)
      break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split(/\r?\n/)
    buffer = lines.pop() || ''

    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed || trimmed.startsWith(':'))
        continue

      if (!trimmed.startsWith('data:'))
        continue

      const payload = trimmed.slice(5).trim()
      if (!payload)
        continue

      try {
        const parsed = parseStreamPayload(payload)
        if (parsed.done)
          return

        if (parsed.text) {
          receivedContent = true
          onChunk(parsed.text)
        }
      }
      catch (error) {
        if (error instanceof SyntaxError)
          continue
        throw error
      }
    }
  }

  if (!receivedContent)
    throw new Error('模型未返回内容，请检查模型名称、账户余额或 API Key 是否有效')
}

export async function testChatConnection(config: ChatConfig) {
  const apiKey = sanitizeApiKey(config.apiKey)
  if (!apiKey)
    throw new Error('API Key 不能为空')

  const res = await fetch(resolveChatUrl(config.baseUrl), {
    method: 'POST',
    headers: buildRequestHeaders(apiKey, config.baseUrl),
    body: JSON.stringify({
      model: config.model,
      messages: [{ role: 'user', content: 'ping' }],
      stream: false,
      max_tokens: 8,
    }),
  })

  const payload = await res.json().catch(() => null)
  if (!res.ok)
    throw new Error(extractErrorMessage(payload, `连接失败 (${res.status})`))
}
