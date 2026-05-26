<script setup lang="ts">
import { useBreadcrumb } from '@/core/hooks'

const { breadcrumbList } = useBreadcrumb()
</script>

<template>
  <el-breadcrumb v-if="breadcrumbList.length" class="app-breadcrumb" separator="/">
    <el-breadcrumb-item
      v-for="item in breadcrumbList"
      :key="item.path"
      :to="item.path"
    >
      {{ item.meta?.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<style lang="scss" scoped>
.app-breadcrumb {
  margin-bottom: 12px;
}
</style>
