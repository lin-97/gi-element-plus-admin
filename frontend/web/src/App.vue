<script setup lang="ts">
import zhCn from 'element-plus/es/locale/lang/zh-cn'

defineOptions({ name: 'App' })
</script>

<template>
  <el-config-provider :locale="zhCn" size="default">
    <router-view />
  </el-config-provider>
</template>
