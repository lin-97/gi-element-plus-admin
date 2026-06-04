<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useClipboard } from '@vueuse/core'
import { ElMessage } from 'element-plus'

defineOptions({ name: 'SystemIconGrid' })

const { icons } = defineProps<{
  icons: string[]
}>()

const { copy, copied, isSupported } = useClipboard()

async function copyIconName(name: string) {
  if (!isSupported.value) {
    ElMessage.warning('当前环境不支持剪贴板')
    return
  }
  await copy(name)
  if (copied.value)
    ElMessage.success(`已复制：${name}`)
}

function displayName(fullName: string) {
  const idx = fullName.indexOf(':')
  return idx >= 0 ? fullName.slice(idx + 1) : fullName
}
</script>

<template>
  <ul v-if="icons.length" class="icon-grid">
    <li
      v-for="name in icons"
      :key="name"
      class="icon-grid__item"
      :title="name"
      @click="copyIconName(name)"
    >
      <span class="icon-grid__preview">
        <Icon :icon="name" width="28" height="28" />
      </span>
      <span class="icon-grid__name">{{ displayName(name) }}</span>
      <span class="icon-grid__copy">复制</span>
    </li>
  </ul>
  <el-empty v-else description="暂无匹配的图标" />
</template>

<style scoped lang="scss">
.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.icon-grid__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--el-border-radius-base);
  background: var(--el-bg-color);
  cursor: pointer;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;

  &:hover {
    border-color: var(--el-color-primary-light-5);
    box-shadow: var(--el-box-shadow-lighter);
  }
}

.icon-grid__preview {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--el-text-color-primary);
}

.icon-grid__name {
  max-width: 100%;
  font-size: 12px;
  color: var(--el-text-color-regular);
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.icon-grid__copy {
  font-size: 12px;
  color: var(--el-color-primary);
  opacity: 0;
  transition: opacity 0.2s ease;

  .icon-grid__item:hover & {
    opacity: 1;
  }
}
</style>
