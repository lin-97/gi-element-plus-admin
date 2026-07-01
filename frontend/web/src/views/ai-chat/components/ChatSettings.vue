<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { testChatConnection } from '../apis/chat'
import { CHAT_PROVIDERS } from '../providers'
import { useChatConfigStore } from '../stores/useChatConfigStore'

defineOptions({ name: 'ChatSettings' })

const visible = defineModel<boolean>({ default: false })

const configStore = useChatConfigStore()
const showApiKey = ref(false)
const testing = ref(false)

const modelOptions = computed(() => configStore.currentProvider.models)

function handleProviderChange(id: string) {
  configStore.applyProvider(id)
}

async function handleTestConnection() {
  if (!configStore.isConfigured) {
    ElMessage.warning('请先填写 API Key')
    return
  }

  testing.value = true
  try {
    await testChatConnection(configStore.getConfig())
    ElMessage.success('连接成功，API Key 与模型可用')
  }
  catch (error) {
    ElMessage.error((error as Error).message || '连接失败')
  }
  finally {
    testing.value = false
  }
}

function handleClose() {
  visible.value = false
}
</script>

<template>
  <gi-dialog
    v-model="visible"
    title="AI 对话设置"
    width="calc(100vw - 20px)"
    :style="{ maxWidth: '680px' }"
    destroy-on-close
    :footer="false"
  >
    <el-alert
      type="warning"
      :closable="false"
      show-icon
      title="OpenRouter 的 deepseek-chat-v3-0324:free 已下线。免费用 openrouter/free；要指定 DeepSeek 请选「OpenRouter DeepSeek（付费）」并充值 Credits。"
      style="margin-bottom: 12px"
    />

    <el-form label-width="100px" label-position="left">
      <el-form-item label="服务商">
        <el-select
          :model-value="configStore.providerId"
          style="width: 100%"
          @change="handleProviderChange"
        >
          <el-option
            v-for="item in CHAT_PROVIDERS"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
        <div class="chat-settings__hint">
          {{ configStore.currentProvider.description }}
          <el-link
            type="primary"
            :href="configStore.currentProvider.registerUrl"
            target="_blank"
            style="margin-left: 4px"
          >
            去注册 / 获取 Key
          </el-link>
        </div>
      </el-form-item>

      <el-form-item label="API Key" required>
        <el-input
          v-model="configStore.apiKey"
          :type="showApiKey ? 'text' : 'password'"
          :placeholder="configStore.currentProvider.keyPlaceholder"
          clearable
        >
          <template #append>
            <el-button @click="showApiKey = !showApiKey">
              {{ showApiKey ? '隐藏' : '显示' }}
            </el-button>
          </template>
        </el-input>
        <div class="chat-settings__hint">
          {{ configStore.currentProvider.keyHint }}
        </div>
      </el-form-item>

      <el-form-item label="Base URL">
        <el-input
          v-model="configStore.baseUrl"
          :placeholder="configStore.currentProvider.baseUrl"
          clearable
        />
      </el-form-item>

      <el-form-item label="模型">
        <el-select v-model="configStore.model" style="width: 100%">
          <el-option
            v-for="item in modelOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="System Prompt">
        <el-input
          v-model="configStore.systemPrompt"
          type="textarea"
          :rows="4"
          placeholder="系统提示词"
        />
      </el-form-item>
    </el-form>

    <div class="chat-settings__footer">
      <el-space>
        <el-button type="success" text bg :loading="testing" @click="handleTestConnection">
          测试连接
        </el-button>
        <el-button type="primary" @click="handleClose">
          关闭
        </el-button>
      </el-space>
    </div>
  </gi-dialog>
</template>

<style scoped lang="scss">
.chat-settings__hint {
  margin-top: 6px;
  font-size: 12px;
  line-height: 1.5;
  color: var(--el-text-color-secondary);
}

.chat-settings__footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
}
</style>
