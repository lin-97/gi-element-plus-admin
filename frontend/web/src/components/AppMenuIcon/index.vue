<script setup lang="ts">
import type { Component } from 'vue'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import { Icon } from '@iconify/vue'

defineOptions({ name: 'AppMenuIcon' })

type MenuIconType = 'none' | 'svg' | 'iconify' | 'element'

const { icon, size = '1em', wrap = true } = defineProps<{
  icon?: string
  size?: string | number
  wrap?: boolean
}>()

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

const iconValue = computed(() => icon?.trim() ?? '')
const iconType = computed(() => resolveMenuIconType(icon))
const elementIcon = computed(() => {
  if (iconType.value !== 'element')
    return undefined
  return getElementIcon(icon)
})
const hasIcon = computed(() => iconType.value !== 'none')

const elIconSize = computed(() => {
  if (typeof size === 'number')
    return size
  if (typeof size === 'string' && /^\d+$/.test(size))
    return Number(size)
  return undefined
})

const iconWrapStyle = computed(() => {
  if (wrap || iconType.value === 'element')
    return undefined
  if (typeof size === 'number')
    return { fontSize: `${size}px` }
  if (typeof size === 'string' && size !== '1em')
    return { fontSize: size }
  return undefined
})
</script>

<template>
  <el-icon v-if="wrap && hasIcon" :size="elIconSize">
    <span
      v-if="iconType === 'svg'"
      class="app-menu-icon__svg"
      v-html="iconValue"
    />
    <Icon
      v-else-if="iconType === 'iconify'"
      :icon="iconValue"
      class="app-menu-icon__iconify"
      :width="size"
      :height="size"
    />
    <component :is="elementIcon" v-else />
  </el-icon>
  <span v-else-if="hasIcon" class="app-menu-icon" :style="iconWrapStyle">
    <span
      v-if="iconType === 'svg'"
      class="app-menu-icon__svg"
      v-html="iconValue"
    />
    <Icon
      v-else-if="iconType === 'iconify'"
      :icon="iconValue"
      class="app-menu-icon__iconify"
      :width="size"
      :height="size"
    />
    <el-icon v-else :size="elIconSize">
      <component :is="elementIcon" />
    </el-icon>
  </span>
</template>

<style lang="scss" scoped>
.app-menu-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;

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
