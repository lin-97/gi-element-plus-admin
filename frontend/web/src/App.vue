<script setup lang="ts">
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { useAppStore } from '@/core/stores'

defineOptions({ name: 'App' })

// 独立全屏页（/ai-chat、/login 等）不经过 AppLayout，需在此初始化以应用系统主题色
useAppStore()
</script>

<template>
  <el-config-provider :locale="zhCn" size="default">
    <router-view />
  </el-config-provider>
</template>
