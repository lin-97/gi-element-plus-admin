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
  <gi-flex column class="top-layout">
    <AppHeader mode="top" />
    <AppTabs v-if="appStore.isShowTabs" />
    <gi-flex flex="1" column>
      <PageTransition />
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
