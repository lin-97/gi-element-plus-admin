<script setup lang="ts">
import { useAppStore, useTabsStore } from '@/core/stores'

defineOptions({ name: 'PageTransition' })

const appStore = useAppStore()
const tabsStore = useTabsStore()

/** 需要缓存的组件名列表 */
const cachedViews = computed(() => tabsStore.cacheList.map(String))
</script>

<template>
  <div class="page-view">
    <router-view v-slot="{ Component, route: currentRoute }">
      <transition :name="appStore.transitionName" mode="out-in">
        <keep-alive v-if="tabsStore.reloadFlag" :include="cachedViews">
          <component
            :is="Component"
            v-if="Component"
            :key="currentRoute.fullPath"
          />
        </keep-alive>
      </transition>
    </router-view>
  </div>
</template>

<style scoped lang="scss">
.page-view {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
