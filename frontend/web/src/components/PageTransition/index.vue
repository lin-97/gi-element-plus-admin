<script setup lang="ts">
import { useAppStore } from '@/core/stores/useAppStore'
import { useTabsStore } from '@/core/stores/useTabsStore'

const appStore = useAppStore()
const tabsStore = useTabsStore()

/** 需要缓存的组件名列表 */
const cachedViews = computed(() => tabsStore.cacheList.map(String))
</script>

<template>
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
</template>
