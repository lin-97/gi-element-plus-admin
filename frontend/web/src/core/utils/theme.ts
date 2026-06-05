/** 预设主题色 */
export const PRESET_THEME_COLORS = [
  '#165DFF',
  '#722ED1',
  '#F5222D',
  '#FA8C16',
  '#13C2C2',
  '#52C41A',
  '#EB2F96',
  '#18A058',
  '#2d8cf0',
  '#007AFF',
  '#5ac8fa',
  '#5856D6',
  '#536dfe',
  '#9c27b0',
  '#AF52DE',
  '#0096c7',
  '#00C1D4',
  '#43a047',
  '#e53935',
  '#f4511e',
  '#6d4c41',
] as const

const THEME_STYLE_ID = 'app-theme-vars'

const THEME_VAR_KEYS = [
  '--el-color-primary',
  '--el-color-primary-light-3',
  '--el-color-primary-light-5',
  '--el-color-primary-light-7',
  '--el-color-primary-light-8',
  '--el-color-primary-light-9',
  '--el-color-primary-dark-2',
] as const

/** 获取暗色主题色 */
function getDarkColor(hex: string, rate = 0.8) {
  let r = Number.parseInt(hex.slice(1, 3), 16) as number
  let g = Number.parseInt(hex.slice(3, 5), 16) as number
  let b = Number.parseInt(hex.slice(5, 7), 16) as number
  // 公式：new = src*rate + 255*(1-rate)
  r = Math.round(r * rate + 255 * (1 - rate))
  g = Math.round(g * rate + 255 * (1 - rate))
  b = Math.round(b * rate + 255 * (1 - rate))
  const toHex = (n: number) => n.toString(16).padStart(2, '0')
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`
}

function buildPaletteCss(color: string, dark: boolean) {
  const themeColor = dark ? getDarkColor(color) : color
  const b_color = dark ? '#000' : '#fff'
  const percentages = dark ? [100, 80, 70, 60, 50, 30] as const : [100, 70, 50, 30, 20, 10] as const
  const lines = [
    `--el-color-primary: color-mix(in srgb, ${themeColor} ${percentages[0]}%, ${b_color});`,
    `--el-color-primary-light-3: color-mix(in srgb, ${themeColor} ${percentages[1]}%, ${b_color});`,
    `--el-color-primary-light-5: color-mix(in srgb, ${themeColor} ${percentages[2]}%, ${b_color});`,
    `--el-color-primary-light-7: color-mix(in srgb, ${themeColor} ${percentages[3]}%, ${b_color});`,
    `--el-color-primary-light-8: color-mix(in srgb, ${themeColor} ${percentages[4]}%, ${b_color});`,
    `--el-color-primary-light-9: color-mix(in srgb, ${themeColor} ${percentages[5]}%, ${b_color});`,
    `--el-color-primary-dark-2: color-mix(in srgb, ${themeColor} 80%, ${dark ? '#fff' : '#000'});`,
  ]
  return lines.join('\n  ')
}

function buildThemeStyle(color: string) {
  return `:root {
  ${buildPaletteCss(color, false)}
}
html.dark {
  ${buildPaletteCss(color, true)}
}`
}

function clearLegacyInlineThemeVars() {
  const el = document.documentElement
  for (const key of THEME_VAR_KEYS)
    el.style.removeProperty(key)
}

/** 将主题色应用到 Element Plus CSS 变量（亮色 / 暗色双 palette） */
export function applyThemeColor(color: string) {
  let styleEl = document.getElementById(THEME_STYLE_ID) as HTMLStyleElement | null
  if (!styleEl) {
    styleEl = document.createElement('style')
    styleEl.id = THEME_STYLE_ID
    document.head.appendChild(styleEl)
  }

  styleEl.textContent = buildThemeStyle(color)
  clearLegacyInlineThemeVars()
}
