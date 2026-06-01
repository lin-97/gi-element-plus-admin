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

// Element Plus 暗色模式背景色，用于生成 primary-light 色阶
const EP_DARK_BG_COLOR = '#141414'

const THEME_STYLE_ID = 'app-theme-vars'

function hexToRgb(hex: string) {
  const normalized = hex.replace('#', '')
  const value = normalized.length === 3
    ? normalized.split('').map(c => c + c).join('')
    : normalized

  const num = Number.parseInt(value, 16)
  return {
    r: (num >> 16) & 255,
    g: (num >> 8) & 255,
    b: num & 255,
  }
}

function rgbToHex(r: number, g: number, b: number) {
  const toHex = (n: number) => Math.round(n).toString(16).padStart(2, '0')
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`
}

/** 与 Sass color.mix 一致：mix(base, mixIn, weight)，weight 为 mixIn 占比 */
function mixColor(base: string, mixIn: string, weight: number) {
  const c1 = hexToRgb(base)
  const c2 = hexToRgb(mixIn)
  const w = Math.min(Math.max(weight, 0), 1)
  return rgbToHex(
    c1.r * (1 - w) + c2.r * w,
    c1.g * (1 - w) + c2.g * w,
    c1.b * (1 - w) + c2.b * w,
  )
}

interface PrimaryPalette {
  primary: string
  light: Record<number, string>
  dark2: string
}

/** 按 Element Plus 规则生成 primary 色阶 */
function generatePrimaryPalette(color: string, mode: 'light' | 'dark'): PrimaryPalette {
  const lightMixBase = mode === 'light' ? '#ffffff' : EP_DARK_BG_COLOR
  const darkMixBase = mode === 'light' ? '#000000' : '#ffffff'

  const light: Record<number, string> = {}
  for (let i = 1; i <= 9; i++) {
    light[i] = mixColor(color, lightMixBase, i * 0.1)
  }

  return {
    primary: color,
    light,
    dark2: mixColor(color, darkMixBase, 0.2),
  }
}

function paletteToCssBlock(palette: PrimaryPalette): string {
  const lines = [
    `--el-color-primary: ${palette.primary};`,
    ...Array.from({ length: 9 }, (_, i) =>
      `--el-color-primary-light-${i + 1}: ${palette.light[i + 1]};`),
    `--el-color-primary-dark-2: ${palette.dark2};`,
  ]
  return lines.join('\n  ')
}

function buildThemeStyle(color: string): string {
  const lightPalette = generatePrimaryPalette(color, 'light')
  const darkPalette = generatePrimaryPalette(color, 'dark')

  return `:root {
  ${paletteToCssBlock(lightPalette)}
}
html.dark {
  ${paletteToCssBlock(darkPalette)}
}`
}

function clearLegacyInlineThemeVars() {
  const el = document.documentElement
  el.style.removeProperty('--el-color-primary')
  for (let i = 1; i <= 9; i++) {
    el.style.removeProperty(`--el-color-primary-light-${i}`)
  }
  el.style.removeProperty('--el-color-primary-dark-2')
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
