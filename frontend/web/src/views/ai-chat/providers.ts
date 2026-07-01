export interface ChatProvider {
  id: string
  name: string
  description: string
  baseUrl: string
  model: string
  keyHint: string
  keyPlaceholder: string
  registerUrl: string
  models: Array<{ label: string, value: string }>
}

/** AI 对话服务商预设（OpenAI 兼容） */
export const CHAT_PROVIDERS: ChatProvider[] = [
  {
    id: 'openrouter-free',
    name: 'OpenRouter 免费（推荐）',
    description: 'OpenRouter 免费模型会变动，推荐使用「自动免费路由」openrouter/free；DeepSeek 的 :free 后缀模型可能随时下线。',
    baseUrl: 'https://openrouter.ai/api/v1',
    model: 'openrouter/free',
    keyHint: '在 openrouter.ai 注册 → Settings → API Keys 创建 Key',
    keyPlaceholder: 'sk-or-v1-...',
    registerUrl: 'https://openrouter.ai/settings/keys',
    models: [
      { label: '自动免费模型（推荐）', value: 'openrouter/free' },
      { label: 'DeepSeek R1 免费', value: 'deepseek/deepseek-r1:free' },
      { label: 'DeepSeek Chat 免费（旧）', value: 'deepseek/deepseek-chat:free' },
      { label: 'Qwen3 Coder 免费', value: 'qwen/qwen3-coder:free' },
      { label: 'Llama 3.2 3B 免费', value: 'meta-llama/llama-3.2-3b-instruct:free' },
    ],
  },
  {
    id: 'openrouter-deepseek-paid',
    name: 'OpenRouter DeepSeek（付费）',
    description: '需在 OpenRouter 充值少量余额；deepseek-chat-v3-0324:free 已下线，请用此付费 slug。',
    baseUrl: 'https://openrouter.ai/api/v1',
    model: 'deepseek/deepseek-chat-v3-0324',
    keyHint: 'OpenRouter Key + 账户有余额（Credits）',
    keyPlaceholder: 'sk-or-v1-...',
    registerUrl: 'https://openrouter.ai/settings/credits',
    models: [
      { label: 'DeepSeek Chat V3', value: 'deepseek/deepseek-chat-v3-0324' },
      { label: 'DeepSeek R1', value: 'deepseek/deepseek-r1' },
    ],
  },
  {
    id: 'siliconflow',
    name: '硅基流动（新用户送额度）',
    description: '新用户注册通常赠送免费 Token 额度，可调用 DeepSeek-V3 等模型（额度用完后需充值）。',
    baseUrl: 'https://api.siliconflow.cn/v1',
    model: 'deepseek-ai/DeepSeek-V3',
    keyHint: '在 cloud.siliconflow.cn 注册并在「API 密钥」页创建 Key',
    keyPlaceholder: 'sk-...',
    registerUrl: 'https://cloud.siliconflow.cn/account/ak',
    models: [
      { label: 'DeepSeek-V3', value: 'deepseek-ai/DeepSeek-V3' },
      { label: 'DeepSeek-R1', value: 'deepseek-ai/DeepSeek-R1' },
      { label: 'DeepSeek-V3.2', value: 'deepseek-ai/DeepSeek-V3.2' },
    ],
  },
  {
    id: 'siliconflow-free',
    name: '硅基流动 完全免费模型',
    description: '平台标注免费的轻量模型（非 DeepSeek 品牌，但可正常对话，长期免费）。',
    baseUrl: 'https://api.siliconflow.cn/v1',
    model: 'Qwen/Qwen2.5-7B-Instruct',
    keyHint: '同上，使用硅基流动 API Key',
    keyPlaceholder: 'sk-...',
    registerUrl: 'https://cloud.siliconflow.cn/account/ak',
    models: [
      { label: 'Qwen2.5-7B（免费）', value: 'Qwen/Qwen2.5-7B-Instruct' },
      { label: 'GLM-4-9B（免费）', value: 'THUDM/glm-4-9b-chat' },
    ],
  },
  {
    id: 'deepseek-official',
    name: 'DeepSeek 官方 API',
    description: '需在 platform.deepseek.com 充值；Insufficient Balance 表示余额不足。',
    baseUrl: 'https://api.deepseek.com',
    model: 'deepseek-chat',
    keyHint: '在 platform.deepseek.com 创建 API Key 并充值',
    keyPlaceholder: 'sk-...',
    registerUrl: 'https://platform.deepseek.com/api_keys',
    models: [
      { label: 'deepseek-chat', value: 'deepseek-chat' },
      { label: 'deepseek-reasoner', value: 'deepseek-reasoner' },
      { label: 'deepseek-v4-flash', value: 'deepseek-v4-flash' },
      { label: 'deepseek-v4-pro', value: 'deepseek-v4-pro' },
    ],
  },
]

export function getChatProvider(id: string) {
  return CHAT_PROVIDERS.find(item => item.id === id) ?? CHAT_PROVIDERS[0]
}

/** 将旧配置中的已下线免费模型迁移到新默认值 */
export function normalizeModelSlug(model: string) {
  const deprecatedFreeSlugs = [
    'deepseek/deepseek-chat-v3-0324:free',
  ]
  if (deprecatedFreeSlugs.includes(model))
    return 'openrouter/free'
  return model
}
