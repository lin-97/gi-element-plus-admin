<script setup lang="ts">
import { useAppStore } from '@/core/stores'
import DefaultLayout from '@/layouts/default/index.vue'
import TopLayout from '@/layouts/top/index.vue'

defineOptions({ name: 'AppLayout' })

const appStore = useAppStore()

const layoutComponent = computed(() =>
  appStore.layoutMode === 'top' ? TopLayout : DefaultLayout,
)
</script>

<template>
  <component :is="layoutComponent" />
</template>
