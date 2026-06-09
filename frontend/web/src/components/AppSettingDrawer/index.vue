<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ColorPicker } from 'vue-color-kit'
import { useTheme } from '@/core/hooks'
import { useAppStore } from '@/core/stores'
import { PRESET_THEME_COLORS } from '@/core/utils/theme'
import 'vue-color-kit/dist/vue-color-kit.css'

defineOptions({ name: 'AppSettingDrawer' })

const emit = defineEmits<{
  (e: 'closed'): void
}>()

const appStore = useAppStore()
const { isDark } = useTheme()

const presetColors = [...PRESET_THEME_COLORS]

function handleChangeColor(color: { hex: string }) {
  appStore.themeColor = color.hex
}

onUnmounted(() => {
  emit('closed')
})
</script>

<template>
  <div class="app-setting-drawer">
    <el-divider content-position="center">
      布局模式
    </el-divider>
    <el-row justify="center">
      <el-radio-group v-model="appStore.layoutMode">
        <el-radio value="left">
          侧边栏
        </el-radio>
        <el-radio value="top">
          顶栏
        </el-radio>
        <el-radio value="mix">
          混合
        </el-radio>
      </el-radio-group>
    </el-row>

    <el-divider content-position="center">
      主题色
    </el-divider>
    <el-row justify="center">
      <ColorPicker
        :color="appStore.themeColor"
        theme="dark"
        :colors-default="presetColors"
        :sucker-hide="true"
        style="width: 218px;"
        @change-color="handleChangeColor"
      />
    </el-row>

    <el-divider content-position="center">
      界面设置
    </el-divider>
    <el-descriptions :column="1">
      <el-descriptions-item label="暗黑模式">
        <el-switch v-model="isDark" class="g-theme-switch" inline-prompt>
          <template #active-action>
            <Icon icon="custom:moon-fill" width="12" height="12" />
          </template>
          <template #inactive-action>
            <Icon icon="custom:sun-fill" width="12" height="12" />
          </template>
        </el-switch>
      </el-descriptions-item>
      <el-descriptions-item label="显示页签">
        <el-switch v-model="appStore.isShowTabs" />
      </el-descriptions-item>
      <el-descriptions-item label="页面过渡动画">
        <el-switch v-model="appStore.isShowAnimation" />
      </el-descriptions-item>
      <el-descriptions-item label="手风琴模式">
        <el-switch v-model="appStore.isMenuAccordion" />
      </el-descriptions-item>
      <el-descriptions-item label="深色菜单">
        <el-switch v-model="appStore.isMenuDark" />
      </el-descriptions-item>
      <el-descriptions-item label="菜单宽度">
        <el-input-number
          v-model="appStore.menuWidth"
          :min="200"
          :max="250"
          :step="5"
          controls-position="right"
        >
          <template #suffix>
            <span>px</span>
          </template>
        </el-input-number>
      </el-descriptions-item>
      <el-descriptions-item label="顶栏高度">
        <el-input-number
          v-model="appStore.headerHeight"
          :min="50"
          :max="60"
          :step="2"
          controls-position="right"
        >
          <template #suffix>
            <span>px</span>
          </template>
        </el-input-number>
      </el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-descriptions__body) {
  background-color: transparent;
}

:deep(.el-descriptions__cell) {
  display: flex;
  align-items: center;

  .el-descriptions__content {
    flex: 1;
    display: flex;
    justify-content: end;
  }
}
</style>
