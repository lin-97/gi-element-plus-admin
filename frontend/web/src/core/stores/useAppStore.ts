import { defineStore } from 'pinia'
import { computed, reactive, toRefs, watch } from 'vue'
import defaultSettings from '../config/setting.json'
import { applyThemeColor } from '../utils/theme'

/**
 * App Store 的核心设置逻辑
 */
function storeSetup() {
  // 初始化 App 配置
  const settingConfig = reactive({ ...defaultSettings }) as App.SettingConfig

  watch(
    () => settingConfig.themeColor,
    color => applyThemeColor(color),
    { immediate: true },
  )

  /**
   * 计算页面切换动画类名
   * 根据配置决定是否启用动画以及使用哪种动画模式
   */
  const transitionName = computed(() =>
    settingConfig.isShowAnimation ? 'fade-slide' : '',
  )

  /**
   * 设置菜单折叠状态
   * @param collapsed - 是否折叠
   */
  const setMenuCollapse = (collapsed: boolean) => {
    settingConfig.isMenuCollapse = collapsed
  }

  /** 恢复默认配置 */
  const resetSetting = () => {
    Object.assign(settingConfig, defaultSettings)
  }

  return {
    ...toRefs(settingConfig),
    transitionName,
    setMenuCollapse,
    resetSetting,
  }
}

// 创建并导出 App Store，启用持久化存储
export const useAppStore = defineStore('app', storeSetup, { persist: true })
