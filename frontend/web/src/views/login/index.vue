<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import type { LoginParams } from '@/types/user'
import { Lock, User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { appConfig } from '@/config'
import { useUserStore } from '@/stores/modules/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive<LoginParams>({
  username: 'admin',
  password: '123456',
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    await userStore.login(form)
    ElMessage.success('登录成功')
    const redirect = (route.query.redirect as string) || appConfig.homePath
    router.push(redirect)
  }
  finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-page__card">
      <h1 class="login-page__title">
        {{ appConfig.title }}
      </h1>
      <p class="login-page__desc">
        企业级 Vue3 + Element Plus 后台模板
      </p>
      <el-form ref="formRef" :model="form" :rules="rules" size="large" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            show-password
            :prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button type="primary" class="login-page__btn" :loading="loading" @click="handleLogin">
          登 录
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #165dff 100%);

  &__card {
    width: 400px;
    padding: 40px;
    background: var(--el-bg-color);
    border-radius: 12px;
    box-shadow: var(--el-box-shadow);
  }

  &__title {
    margin: 0 0 8px;
    font-size: 24px;
    text-align: center;
    color: var(--el-text-color-primary);
  }

  &__desc {
    margin: 0 0 32px;
    font-size: 13px;
    text-align: center;
    color: var(--el-text-color-regular);
  }

  &__btn {
    width: 100%;
  }
}
</style>
