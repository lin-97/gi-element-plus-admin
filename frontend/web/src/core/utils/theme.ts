/** 预设主题色 */
export const PRESET_THEME_COLORS = [
  '#165DFF',
  '#722ED1',
  '#F5222D',
  '#FA8C16',
  '#13C2C2',
  '#52C41A',
  '#EB2F96',
] as const

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

/** 混合两种颜色 */
function mixColor(color1: string, color2: string, weight: number) {
  const c1 = hexToRgb(color1)
  const c2 = hexToRgb(color2)
  const w = Math.min(Math.max(weight, 0), 1)
  return rgbToHex(
    c1.r * (1 - w) + c2.r * w,
    c1.g * (1 - w) + c2.g * w,
    c1.b * (1 - w) + c2.b * w,
  )
}

/** 将主题色应用到 Element Plus CSS 变量 */
export function applyThemeColor(color: string) {
  const el = document.documentElement
  el.style.setProperty('--el-color-primary', color)

  for (let i = 1; i <= 9; i++) {
    el.style.setProperty(
      `--el-color-primary-light-${i}`,
      mixColor(color, '#ffffff', i * 0.1),
    )
  }

  el.style.setProperty(
    '--el-color-primary-dark-2',
    mixColor(color, '#000000', 0.2),
  )
}
