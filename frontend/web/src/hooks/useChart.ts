import type { EChartsOption } from 'echarts'
import { computed } from 'vue'
import { useTheme } from '@/core/hooks'

interface Options {
  (isDark?: boolean): EChartsOption
}

/**
 * 用于集中管理 ECharts 配置，提供完整类型提示
 * @param sourceOption - ECharts 配置项（isDark 为 true 时 theme 为内置 dark）
 * @returns { option, theme, isDark }
 */
export function useChart(sourceOption: Options) {
  const { isDark } = useTheme()

  const option = computed<EChartsOption>(() => ({
    backgroundColor: 'transparent',
    ...sourceOption(isDark.value),
  }))

  /** ECharts 内置暗黑主题名 */
  const theme = computed(() => isDark.value ? 'dark' : undefined)

  return {
    option,
    theme,
    isDark,
  }
}
