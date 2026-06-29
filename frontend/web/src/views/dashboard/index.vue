<script setup lang="ts">
import ImageCard from './ImageCard.vue'
import MessageCard from './MessageCard.vue'
import ProjectCard from './ProjectCard.vue'
import QuickActionCard from './QuickActionCard.vue'
import WelcomeCard from './WelcomeCard.vue'

defineOptions({ name: 'Dashboard' })
</script>

<template>
  <div class="dashboard">
    <WelcomeCard class="g-mb g-radius" />

    <el-row :gutter="16" class="dashboard__main">
      <el-col :xs="24" :lg="15">
        <ProjectCard class="g-mb g-radius" />
        <MessageCard class="g-mb g-radius" />
      </el-col>

      <el-col :xs="24" :lg="9">
        <QuickActionCard class="g-mb g-radius" />
        <ImageCard class="g-mb g-radius" />
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
.dashboard {
  height: 100%;
  padding: 16px;
  overflow: hidden auto;

  &__main {
    align-items: flex-start;
  }
}
</style>
