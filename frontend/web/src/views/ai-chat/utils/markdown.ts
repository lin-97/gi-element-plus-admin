import { enableKatex, preloadCodeBlockRuntime } from 'markstream-vue'
import { registerHighlight } from 'stream-markdown'

/** 代码块固定使用暗色主题 */
export const CHAT_CODE_THEME = 'github-dark'

export const CHAT_MARKDOWN_LANGS = [
  'javascript',
  'typescript',
  'python',
  'java',
  'json',
  'bash',
  'shell',
  'vue',
  'html',
  'css',
  'scss',
  'markdown',
] as const

export const CHAT_CODE_BLOCK_PROPS = {
  theme: CHAT_CODE_THEME,
  showHeader: true,
  showCopyButton: true,
  stream: true,
} as const

export const CHAT_PARSE_OPTIONS = {
  streamParse: true,
} as const

let initialized = false
let runtimeReady: Promise<boolean> | null = null

/** 对话页 Markdown 渲染初始化（KaTeX + Shiki 预加载，仅执行一次） */
export function initChatMarkdownRuntime() {
  if (initialized)
    return runtimeReady ?? Promise.resolve(true)
  initialized = true
  enableKatex()
  // preloadCodeBlockRuntime 仅预热 Monaco；Shiki 流式高亮需单独 registerHighlight
  runtimeReady = Promise.all([
    preloadCodeBlockRuntime(),
    registerHighlight({
      themes: [CHAT_CODE_THEME],
      langs: [...CHAT_MARKDOWN_LANGS],
    }),
  ]).then(() => true)
  void runtimeReady
  return runtimeReady
}
