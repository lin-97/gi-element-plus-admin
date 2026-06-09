<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { Drawer } from 'gi-component'
import { h, onBeforeUnmount } from 'vue'
import AppSidebar from '@/components/AppSidebar/index.vue'
import { useAppStore } from '@/core/stores'
import { useResponsive } from '@/hooks/useResponsive'

defineOptions({ name: 'AppMenuToggle' })

const appStore = useAppStore()
const route = useRoute()
const { isMobile } = useResponsive()

const menuIcon = computed(() => {
  if (isMobile.value)
    return 'custom:menu-unfold'
  return appStore.isMenuCollapse ? 'custom:menu-unfold' : 'custom:menu-fold'
})

let drawerInstance: ReturnType<typeof Drawer.open> | null = null
let stopRouteWatch: (() => void) | null = null

function closeMobileMenu() {
  drawerInstance?.close()
  drawerInstance = null
  stopRouteWatch?.()
  stopRouteWatch = null
}

function openMobileMenu() {
  closeMobileMenu()

  drawerInstance = Drawer.open({
    withHeader: false,
    footer: false,
    direction: 'ltr',
    size: '220px',
    bodyClass: 'app-menu-toggle__drawer-body',
    content: () => h(AppSidebar, { drawer: true }),
  })

  stopRouteWatch = watch(() => route.path, () => {
    closeMobileMenu()
  })
}

function handleClick() {
  if (isMobile.value) {
    openMobileMenu()
    return
  }
  appStore.setMenuCollapse(!appStore.isMenuCollapse)
}

onBeforeUnmount(() => {
  closeMobileMenu()
})
</script>

<template>
  <el-button class="g-square-button app-menu-toggle__button" type="primary" bg text circle @click="handleClick">
    <Icon :icon="menuIcon" width="18" height="18" />
  </el-button>
</template>

<style lang="scss">
.app-menu-toggle__button.el-button--primary.is-text {
  --el-button-text-color: var(--el-text-color-primary);
}

.app-menu-toggle__drawer-body {
  padding: 0 !important;
  height: 100%;
}
</style>
