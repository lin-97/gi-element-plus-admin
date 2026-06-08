<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { Lock, User } from '@element-plus/icons-vue'
import { Icon } from '@iconify/vue'
import { ElMessage } from 'element-plus'
import { appConfig } from '@/config'
import { useTheme } from '@/core/hooks'
import { markRoutesLoaded } from '@/router/route-load-state'
import { useUserStore } from '@/stores/useUserStore'

defineOptions({ name: 'Login' })

const REMEMBER_KEY = 'login_remember_username'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const { isDark, toggleDark } = useTheme()

const formRef = useTemplateRef<FormInstance>('formRef')
const loading = ref(false)
const rememberMe = ref(false)
const errorMessage = ref('')
const form = reactive<{ username: string, password: string }>({
  username: 'admin',
  password: '123456',
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const features = [
  {
    no: '01',
    title: '数据驱动决策',
    desc: '可视化工作台与业务看板，关键指标一目了然',
  },
  {
    no: '02',
    title: '精细化权限管控',
    desc: '角色、菜单、按钮级权限，满足企业安全合规',
  },
  {
    no: '03',
    title: '开箱即用脚手架',
    desc: 'Vue 3 + Element Plus，快速搭建可扩展中后台',
  },
]

onMounted(() => {
  const saved = localStorage.getItem(REMEMBER_KEY)
  if (saved) {
    form.username = saved
    rememberMe.value = true
  }
})

function getLoginErrorMessage(error: unknown) {
  if (error instanceof Error) {
    if (error.message === 'Network Error')
      return '无法连接服务器，请检查网络或后端服务是否可用'
    if (error.message)
      return error.message
  }
  return '登录失败，请稍后重试'
}

async function handleLogin() {
  errorMessage.value = ''
  try {
    await formRef.value?.validate()
  }
  catch {
    return
  }

  loading.value = true
  try {
    await userStore.login(form)
    if (rememberMe.value)
      localStorage.setItem(REMEMBER_KEY, form.username)
    else
      localStorage.removeItem(REMEMBER_KEY)
    markRoutesLoaded()
    ElMessage.success('登录成功')
    const redirect = (route.query.redirect as string) || appConfig.homePath
    await router.push(redirect)
  }
  catch (error) {
    const message = getLoginErrorMessage(error)
    errorMessage.value = message
    ElMessage.error(message)
  }
  finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <el-button
      class="login-page__theme-toggle"
      type="primary"
      text
      circle
      @click="toggleDark()"
    >
      <Icon
        :icon="!isDark ? 'custom:sun-fill' : 'custom:moon-fill'"
        width="18"
        height="18"
      />
    </el-button>

    <aside class="login-page__brand">
      <div class="login-page__brand-inner">
        <span class="login-page__badge">企业级中后台</span>

        <div class="login-page__illus" aria-hidden="true">
          <div class="login-page__illus-doc">
            <span class="login-page__illus-line" />
            <span class="login-page__illus-line login-page__illus-line--short" />
            <span class="login-page__illus-line" />
          </div>
          <div class="login-page__illus-chat">
            <span class="login-page__illus-dot" />
            <span class="login-page__illus-dot" />
            <span class="login-page__illus-dot" />
          </div>
        </div>

        <h1 class="login-page__brand-title">
          {{ appConfig.title }}
        </h1>
        <p class="login-page__brand-desc">
          统一权限、菜单与业务模块管理，助力团队高效协作与稳定交付。
        </p>

        <ul class="login-page__features">
          <li
            v-for="item in features"
            :key="item.no"
            class="login-page__feature"
          >
            <span class="login-page__feature-no">{{ item.no }}</span>
            <div>
              <strong>{{ item.title }}</strong>
              <p>{{ item.desc }}</p>
            </div>
          </li>
        </ul>
      </div>

      <svg
        class="login-page__wave"
        viewBox="0 0 48 800"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <path
          d="M48,0 C24,120 36,240 12,400 C36,560 24,680 48,800 L48,0 Z"
          fill="var(--login-panel-bg)"
        />
      </svg>
    </aside>

    <main class="login-page__panel">
      <div class="login-page__form-wrap">
        <header class="login-page__form-header">
          <h2 class="login-page__form-title">
            欢迎回来
          </h2>
          <p class="login-page__form-desc">
            登录以继续使用您的工作空间
          </p>
        </header>

        <el-alert
          v-if="errorMessage"
          class="login-page__error"
          :title="errorMessage"
          type="error"
          show-icon
          :closable="true"
          @close="errorMessage = ''"
        />

        <el-form
          ref="formRef"
          class="login-page__form"
          :model="form"
          :rules="rules"
          size="large"
          label-position="top"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="用户名" prop="username" required>
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              :prefix-icon="User"
            />
          </el-form-item>
          <el-form-item label="密码" prop="password" required>
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              show-password
              :prefix-icon="Lock"
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-checkbox v-model="rememberMe" class="login-page__remember">
            记住我（7 天内免登录）
          </el-checkbox>

          <el-button
            type="primary"
            class="login-page__submit"
            size="large"
            :loading="loading"
            @click="handleLogin"
          >
            登 录
          </el-button>
        </el-form>

        <p class="login-page__hint">
          演示账号：admin / 123456
        </p>
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  position: relative;

  --login-primary: #2563eb;
  --login-primary-hover: #1d4ed8;
  --login-brand-bg: linear-gradient(160deg, #eff6ff 0%, #f5f3ff 48%, #eef2ff 100%);
  --login-panel-bg: #fff;
  --login-text: #0f172a;
  --login-text-muted: #64748b;
  --login-card-bg: #fff;
  --login-card-border: #e2e8f0;
  --login-badge-bg: #2563eb;
  --login-badge-text: #fff;

  display: flex;
  min-height: 100vh;
  background: var(--login-panel-bg);

  &__theme-toggle {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 10;
    color: var(--el-text-color-primary);
  }

  &__brand {
    position: relative;
    display: flex;
    flex: 1;
    align-items: center;
    justify-content: center;
    min-width: 0;
    padding: 48px 64px 48px 48px;
    background: var(--login-brand-bg);
  }

  &__brand-inner {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 480px;
    color: var(--login-text);
  }

  &__badge {
    display: inline-block;
    padding: 6px 14px;
    margin-bottom: 32px;
    font-size: 13px;
    font-weight: 500;
    color: var(--login-badge-text);
    background: var(--login-badge-bg);
    border-radius: 999px;
  }

  &__illus {
    display: flex;
    gap: 20px;
    align-items: center;
    justify-content: center;
    margin-bottom: 28px;
  }

  &__illus-doc {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 88px;
    padding: 16px;
    background: rgb(255 255 255 / 85%);
    border: 1px solid var(--login-card-border);
    border-radius: 12px;
    box-shadow: 0 8px 24px rgb(37 99 235 / 8%);
  }

  &__illus-line {
    display: block;
    height: 8px;
    background: linear-gradient(90deg, #93c5fd, #c4b5fd);
    border-radius: 4px;

    &--short {
      width: 70%;
    }
  }

  &__illus-chat {
    display: flex;
    gap: 6px;
    align-items: center;
    padding: 14px 18px;
    background: var(--login-primary);
    border-radius: 16px 16px 16px 4px;
    box-shadow: 0 12px 28px rgb(37 99 235 / 28%);
  }

  &__illus-dot {
    width: 8px;
    height: 8px;
    background: rgb(255 255 255 / 90%);
    border-radius: 50%;
  }

  &__brand-title {
    margin: 0 0 10px;
    font-size: clamp(26px, 2.8vw, 34px);
    font-weight: 700;
    line-height: 1.3;
    color: var(--login-text);
    letter-spacing: -0.02em;
  }

  &__brand-desc {
    margin: 0 0 28px;
    font-size: 14px;
    line-height: 1.7;
    color: var(--login-text-muted);
  }

  &__features {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 0;
    margin: 0;
    list-style: none;
  }

  &__feature {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    padding: 16px 18px;
    background: var(--login-card-bg);
    border: 1px solid var(--login-card-border);
    border-radius: 12px;
    box-shadow: 0 4px 16px rgb(15 23 42 / 4%);
    transition:
      box-shadow 0.2s ease,
      border-color 0.2s ease;

    &:hover {
      border-color: #bfdbfe;
      box-shadow: 0 8px 24px rgb(37 99 235 / 10%);
    }

    strong {
      display: block;
      margin-bottom: 4px;
      font-size: 15px;
      font-weight: 600;
      color: var(--login-text);
    }

    p {
      margin: 0;
      font-size: 13px;
      line-height: 1.55;
      color: var(--login-text-muted);
    }
  }

  &__feature-no {
    flex-shrink: 0;
    font-size: 20px;
    font-weight: 700;
    line-height: 1;
    color: var(--login-primary);
  }

  &__wave {
    position: absolute;
    top: 0;
    right: -1px;
    z-index: 2;
    width: 48px;
    height: 100%;
    pointer-events: none;
  }

  &__panel {
    display: flex;
    flex: 1;
    align-items: center;
    justify-content: center;
    min-width: 0;
    padding: 48px 40px;
    background: var(--login-panel-bg);
  }

  &__form-wrap {
    width: 100%;
    max-width: 400px;
  }

  &__form-header {
    margin-bottom: 32px;
  }

  &__error {
    margin-bottom: 16px;
  }

  &__form-title {
    margin: 0 0 8px;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.25;
    color: var(--login-text);
    letter-spacing: -0.02em;
  }

  &__form-desc {
    margin: 0;
    font-size: 14px;
    line-height: 1.6;
    color: var(--login-text-muted);
  }

  &__form {
    :deep(.el-form-item__label) {
      padding-bottom: 6px;
      font-size: 14px;
      font-weight: 500;
      color: var(--login-text);
    }

    :deep(.el-input__wrapper) {
      padding: 4px 12px;
      border-radius: 8px;
      box-shadow: 0 0 0 1px var(--el-border-color) inset;
      transition: box-shadow 0.2s ease;

      &:hover {
        box-shadow: 0 0 0 1px var(--el-border-color-hover) inset;
      }

      &.is-focus {
        box-shadow: 0 0 0 1px var(--login-primary) inset;
      }
    }

    :deep(.el-button) {
      height: 46px;
      border-radius: 8px;
      font-size: 15px;
    }
  }

  &__remember {
    margin-bottom: 20px;

    :deep(.el-checkbox__label) {
      font-size: 13px;
      color: var(--login-text-muted);
    }
  }

  &__submit {
    --el-button-bg-color: var(--login-primary);
    --el-button-border-color: var(--login-primary);
    --el-button-hover-bg-color: var(--login-primary-hover);
    --el-button-hover-border-color: var(--login-primary-hover);
    --el-button-active-bg-color: var(--login-primary-hover);
    --el-button-active-border-color: var(--login-primary-hover);

    width: 100%;
  }

  &__hint {
    margin: 28px 0 0;
    font-size: 12px;
    color: var(--login-text-muted);
    text-align: center;
  }
}

html.dark .login-page {
  --login-brand-bg: linear-gradient(160deg, #0f172a 0%, #1e293b 50%, #1e1b4b 100%);
  --login-panel-bg: var(--el-bg-color);
  --login-text: var(--el-text-color-primary);
  --login-text-muted: var(--el-text-color-secondary);
  --login-card-bg: var(--el-bg-color-overlay);
  --login-card-border: var(--el-border-color);
  --login-badge-bg: #3b82f6;

  &__illus-doc {
    background: rgb(30 41 59 / 80%);
  }

  &__wave path {
    fill: var(--el-bg-color);
  }
}

@media (width <= 992px) {
  .login-page__brand {
    display: none;
  }

  .login-page__panel {
    flex: 1;
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .login-page__feature,
  .login-page__form :deep(.el-input__wrapper),
  .login-page__submit {
    transition: none;
  }
}
</style>
