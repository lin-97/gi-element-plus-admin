<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ColorPicker } from 'vue-color-kit'
import { useTheme } from '@/core/hooks'
import { useAppStore } from '@/core/stores'
import { PRESET_THEME_COLORS } from '@/core/utils/theme'
import 'vue-color-kit/dist/vue-color-kit.css'

defineOptions({ name: 'AppSettingDrawer' })

const visible = defineModel({ default: false })

const appStore = useAppStore()
const { isDark } = useTheme()

const presetColors = [...PRESET_THEME_COLORS]

function handleChangeColor(color: { hex: string }) {
  appStore.themeColor = color.hex
}

function handleReset() {
  appStore.resetSetting()
  isDark.value = false
}
</script>

<template>
  <el-drawer v-model="visible" title="系统设置" direction="rtl" size="320px" :append-to-body="true">
    <el-divider content-position="center">
      布局模式
    </el-divider>
    <el-radio-group v-model="appStore.layoutMode">
      <el-radio value="left">
        侧边栏
      </el-radio>
      <el-radio value="top">
        顶栏
      </el-radio>
    </el-radio-group>

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
        <el-switch v-model="isDark" inline-prompt>
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
    </el-descriptions>

    <template #footer>
      <el-button type="primary" style="width: 100%" @click="handleReset">
        恢复默认配置
      </el-button>
    </template>
  </el-drawer>
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
