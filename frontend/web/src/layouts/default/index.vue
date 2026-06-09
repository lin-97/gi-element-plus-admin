<script setup lang="ts">
import AppHeader from '@/components/AppHeader/index.vue'
import AppSidebar from '@/components/AppSidebar/index.vue'
import AppTabs from '@/components/AppTabs/index.vue'
import PageTransition from '@/components/PageTransition/index.vue'
import { useAppStore } from '@/core/stores'
import { useResponsive } from '@/hooks/useResponsive'

defineOptions({ name: 'DefaultLayout' })

const appStore = useAppStore()
const { isMobile } = useResponsive()
</script>

<template>
  <gi-flex class="default-layout">
    <AppSidebar v-if="!isMobile" />
    <gi-flex flex="1" column>
      <AppHeader />
      <AppTabs v-if="appStore.isShowTabs" />
      <gi-flex flex="1" column>
        <PageTransition />
      </gi-flex>
    </gi-flex>
  </gi-flex>
</template>

<style lang="scss" scoped>
.gi-flex {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
