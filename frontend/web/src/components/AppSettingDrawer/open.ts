import { ElButton } from 'element-plus'
import { Drawer } from 'gi-component'
import { h } from 'vue'
import { useTheme } from '@/core/hooks'
import { useAppStore } from '@/core/stores'
import AppSettingDrawer from './index.vue'

let drawerInstance: ReturnType<typeof Drawer.open> | null = null

function clearDrawerInstance() {
  drawerInstance = null
}

/** 打开系统设置抽屉（挂载在 body，切换布局时不会关闭） */
export function openAppSettingDrawer() {
  if (drawerInstance)
    return drawerInstance

  const appStore = useAppStore()
  const { isDark } = useTheme()

  function handleReset() {
    appStore.resetSetting()
    isDark.value = false
  }

  drawerInstance = Drawer.open({
    title: '系统设置',
    direction: 'rtl',
    size: '320px',
    footer: () => h(
      ElButton,
      {
        type: 'primary',
        style: { width: '100%' },
        onClick: handleReset,
      },
      () => '恢复默认配置',
    ),
    content: () => h(AppSettingDrawer, { onClosed: clearDrawerInstance }),
    onCancel: clearDrawerInstance,
  })

  return drawerInstance
}
