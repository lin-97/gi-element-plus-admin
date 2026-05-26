<script setup lang="ts">
import type { Component } from 'vue'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/core/stores/useAppStore'
import { usePermissionStore } from '@/stores/modules/permission'

interface MenuItem {
  path: string
  title: string
  icon?: string
}

function getIcon(name?: string) {
  if (!name)
    return undefined
  const iconName = name.charAt(0).toUpperCase() + name.slice(1)
  return (ElementPlusIcons as Record<string, Component>)[iconName]
}

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const permissionStore = usePermissionStore()

const menus = computed(() => {
  const result: MenuItem[] = []
  for (const r of permissionStore.routes) {
    if (r.meta?.hidden)
      continue
    const basePath = r.path === '/' ? '' : r.path
    if (r.children?.length) {
      for (const child of r.children) {
        if (child.meta?.hidden)
          continue
        if (child.meta?.title) {
          const path = basePath ? `${basePath}/${child.path}` : `/${child.path}`
          result.push({
            path,
            title: child.meta.title as string,
            icon: child.meta.icon as string,
          })
        }
      }
    }
  }
  return result
})

function handleSelect(path: string) {
  router.push(path)
}
</script>

<template>
  <aside
    class="app-sidebar"
    :class="{ 'app-sidebar--collapsed': appStore.isMenuAccordion }"
  >
    <div class="app-sidebar__logo">
      <span v-if="!appStore.isMenuAccordion" class="app-sidebar__logo-text">GI Admin</span>
      <span v-else class="app-sidebar__logo-text">GI</span>
    </div>
    <el-menu
      :default-active="route.path"
      :collapse="appStore.isMenuAccordion"
      @select="handleSelect"
    >
      <template v-for="item in menus" :key="item.path">
        <el-menu-item :index="item.path">
          <el-icon v-if="getIcon(item.icon)">
            <component :is="getIcon(item.icon)" />
          </el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </template>
    </el-menu>
  </aside>
</template>

<style lang="scss" scoped>
.app-sidebar {
  width: 220px;
  height: 100%;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color);
  transition: width 0.2s;
  overflow: hidden;

  &--collapsed {
    width: 64px;
  }

  :deep(.el-menu) {
    border-right: none;
  }

  &__logo {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
    color: var(--el-color-primary);
    border-bottom: 1px solid var(--el-border-color);

    &-text {
      font-size: 18px;
      font-weight: 600;
      color: var(--el-color-primary);
      white-space: nowrap;
    }
  }
}
</style>
