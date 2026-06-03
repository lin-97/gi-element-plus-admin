<script setup lang="ts">
import type { Component } from 'vue'
import type { RouteRecordRaw } from 'vue-router'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import { Icon } from '@iconify/vue'

defineOptions({ name: 'AppMenuItem' })

const { item } = defineProps<{
  item: RouteRecordRaw
}>()

type MenuIconType = 'none' | 'svg' | 'iconify' | 'element'

function isSvgIcon(value?: string) {
  const text = value?.trim()
  return !!text && /^<svg[\s>]/i.test(text)
}

function isIconifyIcon(value?: string) {
  const text = value?.trim()
  return !!text && /^[\w-]+:[\w-]+$/.test(text)
}

function resolveMenuIconType(value?: string): MenuIconType {
  const text = value?.trim()
  if (!text)
    return 'none'
  if (isSvgIcon(text))
    return 'svg'
  if (isIconifyIcon(text))
    return 'iconify'
  return 'element'
}

function getElementIcon(name?: string) {
  if (!name)
    return undefined
  const iconName = name
    .split('-')
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join('')
  return (ElementPlusIcons as Record<string, Component>)[iconName]
}

const iconValue = computed(() => item.meta?.icon as string | undefined)
const menuIconType = computed(() => resolveMenuIconType(iconValue.value))
const menuIconifyName = computed(() => iconValue.value?.trim() ?? '')
const menuIconSvg = computed(() => iconValue.value?.trim() ?? '')
const menuIcon = computed(() => {
  if (menuIconType.value !== 'element')
    return undefined
  return getElementIcon(iconValue.value)
})
const hasMenuIcon = computed(() => menuIconType.value !== 'none')
</script>

<template>
  <el-menu-item v-if="!item.children?.length" :index="item.path">
    <el-icon v-if="hasMenuIcon">
      <span
        v-if="menuIconType === 'svg'"
        class="app-menu-item__svg"
        v-html="menuIconSvg"
      />
      <Icon
        v-else-if="menuIconType === 'iconify'"
        :icon="menuIconifyName"
        class="app-menu-item__iconify"
        width="1em"
        height="1em"
      />
      <component :is="menuIcon" v-else />
    </el-icon>
    <template #title>
      {{ item.meta?.title }}
    </template>
  </el-menu-item>

  <el-sub-menu v-else :index="item.path">
    <template #title>
      <el-icon v-if="hasMenuIcon">
        <span
          v-if="menuIconType === 'svg'"
          class="app-menu-item__svg"
          v-html="menuIconSvg"
        />
        <Icon
          v-else-if="menuIconType === 'iconify'"
          :icon="menuIconifyName"
          class="app-menu-item__iconify"
          width="1em"
          height="1em"
        />
        <component :is="menuIcon" v-else />
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

<style lang="scss" scoped>
.app-menu-item {
  &__svg {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1em;
    height: 1em;
    line-height: 1;

    :deep(svg) {
      width: 1em;
      height: 1em;
    }
  }

  &__iconify {
    display: inline-flex;
    font-size: inherit;
  }
}
</style>
