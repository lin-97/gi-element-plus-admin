<script setup lang="ts">
/** 用于标签页刷新的中转页 */

defineOptions({ name: 'Redirect' })

const route = useRoute()
const router = useRouter()

onMounted(() => {
  const path = route.params.path as string
  router.replace(`/${path}`)
})
</script>

<template>
  <div />
</template>
