<script setup lang="ts">
import { useBreadcrumb } from '@/core/hooks'

defineOptions({ name: 'AppBreadcrumb' })

const { breadcrumbs } = useBreadcrumb()
</script>

<template>
  <el-breadcrumb v-if="breadcrumbs.length" class="app-breadcrumb" separator="/">
    <el-breadcrumb-item
      v-for="item in breadcrumbs"
      :key="item.path"
      :to="item.to"
    >
      {{ item.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<style lang="scss" scoped>
.app-breadcrumb {
  white-space: nowrap;
  overflow: hidden;
  display: flex;
}
</style>
