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
  <div class="default-layout">
    <AppSidebar v-if="!isMobile" />
    <div class="default-layout__main">
      <AppHeader />
      <AppTabs v-if="appStore.isShowTabs" />
      <div class="default-layout__content">
        <PageTransition />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use '../shared' as *;

.default-layout {
  @include layout-shell(row);

  &__main {
    @include layout-main;
  }

  &__content {
    @include layout-content;
  }
}
</style>
