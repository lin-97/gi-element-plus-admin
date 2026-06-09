<script setup lang="ts">
/**
 * 顶栏布局模式
 * 菜单置于顶部，适用于菜单较少的场景
 */
import AppHeader from '@/components/AppHeader/index.vue'
import AppTabs from '@/components/AppTabs/index.vue'
import PageTransition from '@/components/PageTransition/index.vue'
import { useAppStore } from '@/core/stores'

defineOptions({ name: 'TopLayout' })

const appStore = useAppStore()
</script>

<template>
  <div class="top-layout">
    <AppHeader mode="top" />
    <AppTabs v-if="appStore.isShowTabs" />
    <div class="top-layout__content">
      <PageTransition />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use '../shared' as *;

.top-layout {
  @include layout-shell(column);

  &__content {
    @include layout-content;
  }
}
</style>
