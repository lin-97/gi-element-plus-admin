<script setup lang="ts">
import type { RouteRecordRaw } from 'vue-router'

defineOptions({ name: 'AppMenuItem' })

const { item } = defineProps<{
  item: RouteRecordRaw
}>()

const menuIcon = computed(() => item.meta?.icon as string | undefined)
</script>

<template>
  <el-menu-item v-if="!item.children?.length" :index="item.path">
    <AppMenuIcon :icon="menuIcon" />
    <template #title>
      {{ item.meta?.title }}
    </template>
  </el-menu-item>

  <el-sub-menu v-else :index="item.path">
    <template #title>
      <AppMenuIcon :icon="menuIcon" />
      <span>{{ item.meta?.title }}</span>
    </template>
    <AppMenuItem
      v-for="child in item.children"
      :key="child.path"
      :item="child"
    />
  </el-sub-menu>
</template>
