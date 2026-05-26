import { storeToRefs } from 'pinia'
import { useAppStore } from '@/stores/modules/app'

/** 主题相关状态（暗黑模式） */
export function useTheme() {
  const appStore = useAppStore()
  const { isDark } = storeToRefs(appStore)

  return { isDark }
}
