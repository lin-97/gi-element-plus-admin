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
    <WelcomeCard class="g-mb" />

    <el-row :gutter="16" class="dashboard__main">
      <el-col :xs="24" :lg="15">
        <ProjectCard class="g-mb" />
        <MessageCard class="g-mb" />
      </el-col>

      <el-col :xs="24" :lg="9">
        <QuickActionCard class="g-mb" />
        <ImageCard class="g-mb" />
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

:deep(.gi-card-header__title) {
  font-weight: 600;
}
</style>
