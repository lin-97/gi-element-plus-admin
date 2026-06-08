import { Delete } from '@element-plus/icons-vue'
import { ElButton } from 'element-plus'
import { Drawer } from 'gi-component'
import { h, ref } from 'vue'
import AppNoticeDrawer from './index.vue'

let drawerInstance: ReturnType<typeof Drawer.open> | null = null

function clearDrawerInstance() {
  drawerInstance = null
}

export function openAppNoticeDrawer() {
  if (drawerInstance)
    return drawerInstance

  const noticeDrawerRef = ref<InstanceType<typeof AppNoticeDrawer> | null>(null)

  function handleClearAll() {
    noticeDrawerRef.value?.clearAll()
  }

  drawerInstance = Drawer.open({
    title: '通知中心',
    direction: 'rtl',
    size: '320px',
    footer: () => h(
      ElButton,
      {
        type: 'primary',
        icon: Delete,
        style: { width: '100%' },
        onClick: handleClearAll,
      },
      '清除所有',
    ),
    content: () => h(AppNoticeDrawer, { ref: noticeDrawerRef, onClosed: clearDrawerInstance }),
    onCancel: clearDrawerInstance,
  })

  return drawerInstance
}
