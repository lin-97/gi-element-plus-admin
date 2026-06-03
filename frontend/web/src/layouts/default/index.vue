<script setup lang="ts">
import AppHeader from '@/components/AppHeader/index.vue'
import AppSidebar from '@/components/AppSidebar/index.vue'
import AppTabs from '@/components/AppTabs/index.vue'
import PageTransition from '@/components/PageTransition/index.vue'
import { useAppStore } from '@/core/stores'

defineOptions({ name: 'DefaultLayout' })

const appStore = useAppStore()
</script>

<template>
  <div class="layout">
    <AppSidebar />
    <div class="layout__main">
      <AppHeader />
      <AppTabs v-if="appStore.isShowTabs" />
      <div class="layout__content">
        <PageTransition />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.layout {
  display: flex;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--el-fill-color-light);
}

.layout__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

.layout__content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
