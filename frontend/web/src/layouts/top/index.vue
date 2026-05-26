<script setup lang="ts">
/**
 * 顶栏布局模式
 * 菜单置于顶部，适用于菜单较少的场景
 */
import AppHeader from '@/components/AppHeader/index.vue'
import AppTabs from '@/components/AppTabs/index.vue'
import PageTransition from '@/components/PageTransition/index.vue'
</script>

<template>
  <div class="layout">
    <AppHeader mode="top" />
    <AppTabs />
    <div class="layout__content">
      <PageTransition />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--el-fill-color-light);
}

.layout__content {
  flex: 1;
  padding: 16px;
  overflow: hidden;
}
</style>
