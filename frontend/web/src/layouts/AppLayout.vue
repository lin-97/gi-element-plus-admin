<script setup lang="ts">
import { useAppStore } from '@/core/stores'
import DefaultLayout from '@/layouts/default/index.vue'
import MixLayout from '@/layouts/mix/index.vue'
import TopLayout from '@/layouts/top/index.vue'

defineOptions({ name: 'AppLayout' })

const appStore = useAppStore()

const LAYOUT_MAP = {
  left: DefaultLayout,
  top: TopLayout,
  mix: MixLayout,
}

const layoutComponent = computed(() => LAYOUT_MAP[appStore.layoutMode] || DefaultLayout)
</script>

<template>
  <component :is="layoutComponent" />
</template>
