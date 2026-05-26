<script setup lang="ts">
import type { FormColumnItem } from 'gi-component'
import { ElMessage } from 'element-plus'
import { GiForm } from 'gi-component'
import { useUserStore } from '@/stores/modules/user'

defineOptions({ name: 'Profile' })

const userStore = useUserStore()

const form = reactive({
  nickname: userStore.userInfo?.nickname ?? '',
  email: userStore.userInfo?.email ?? '',
  phone: userStore.userInfo?.phone ?? '',
})

const columns: FormColumnItem[] = [
  { field: 'nickname', label: '昵称', type: 'input', required: true, span: 24 },
  { field: 'email', label: '邮箱', type: 'input', span: 24 },
  { field: 'phone', label: '手机', type: 'input', span: 24 },
]

function handleSave() {
  ElMessage.success('保存成功（演示）')
}
</script>

<template>
  <el-card shadow="never">
    <template #header>
      用户信息
    </template>
    <div class="profile">
      <el-avatar :size="80" :src="userStore.userInfo?.avatar">
        {{ userStore.userInfo?.nickname?.[0] }}
      </el-avatar>
      <div class="profile__info">
        <p>用户名：{{ userStore.userInfo?.username }}</p>
        <p>角色：{{ userStore.userInfo?.roles?.join('、') }}</p>
      </div>
    </div>
    <GiForm v-model="form" :columns="columns" :span="24" />
    <el-button type="primary" @click="handleSave">
      保存
    </el-button>
  </el-card>
</template>

<style lang="scss" scoped>
.profile {
  display: flex;
  gap: 24px;
  align-items: center;
  margin-bottom: 24px;

  &__info p {
    margin: 4px 0;
    color: var(--el-text-color-regular);
  }
}
</style>
