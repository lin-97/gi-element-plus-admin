<script setup lang="ts">
import type { Component } from 'vue'
import type { RouteRecordRaw } from 'vue-router'
import * as ElementPlusIcons from '@element-plus/icons-vue'

defineOptions({ name: 'AppMenuItem' })

const { item } = defineProps<{
  item: RouteRecordRaw
}>()

function getIcon(name?: string) {
  if (!name)
    return undefined
  const iconName = name
    .split('-')
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join('')
  return (ElementPlusIcons as Record<string, Component>)[iconName]
}

const menuIcon = computed(() => getIcon(item.meta?.icon as string | undefined))
</script>

<template>
  <el-menu-item v-if="!item.children?.length" :index="item.path">
    <el-icon v-if="menuIcon">
      <component :is="menuIcon" />
    </el-icon>
    <template #title>
      {{ item.meta?.title }}
    </template>
  </el-menu-item>

  <el-sub-menu v-else :index="item.path">
    <template #title>
      <el-icon v-if="menuIcon">
        <component :is="menuIcon" />
      </el-icon>
      <span>{{ item.meta?.title }}</span>
    </template>
    <AppMenuItem
      v-for="child in item.children"
      :key="child.path"
      :item="child"
    />
  </el-sub-menu>
</template>
