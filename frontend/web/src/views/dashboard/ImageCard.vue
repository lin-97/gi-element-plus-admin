<script setup lang="ts">
import homeDesignImg from '@/assets/images/home-design.svg'

defineOptions({ name: 'ImageCard' })
</script>

<template>
  <GiCard class="image-card" :header-style="{ display: 'none' }">
    <img
      :src="homeDesignImg"
      alt="工作台插图"
      class="image-card__img"
    >
  </GiCard>
</template>

<style lang="scss" scoped>
.image-card {
  &__img {
    display: block;
    width: 100%;
    height: auto;
  }
}
</style>
