<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { appConfig } from '@/config'
import { useTheme } from '@/core/hooks'

defineOptions({ name: 'Error404' })

const router = useRouter()
const route = useRoute()
const { isDark, toggleDark } = useTheme()

const hints = [
  {
    icon: 'mdi:link-variant-off',
    title: '链接可能已失效',
    desc: '页面地址错误或资源已被删除',
  },
  {
    icon: 'mdi:keyboard-backspace',
    title: '尝试返回上一页',
    desc: '从浏览器历史记录中重新进入',
  },
  {
    icon: 'mdi:view-dashboard-outline',
    title: '从工作台重新开始',
    desc: '通过首页菜单导航到目标功能',
  },
]

function goHome() {
  router.push(appConfig.homePath)
}

function goBack() {
  if (window.history.length > 1)
    router.back()
  else
    goHome()
}
</script>

<template>
  <div class="not-found">
    <el-button
      class="not-found__theme-toggle"
      type="primary"
      text
      circle
      aria-label="切换明暗主题"
      @click="toggleDark()"
    >
      <Icon
        :icon="!isDark ? 'custom:sun-fill' : 'custom:moon-fill'"
        width="18"
        height="18"
      />
    </el-button>

    <aside class="not-found__visual" aria-hidden="true">
      <span class="not-found__watermark">404</span>

      <div class="not-found__scene">
        <div class="not-found__orbit not-found__orbit--1" />
        <div class="not-found__orbit not-found__orbit--2" />

        <svg
          class="not-found__compass"
          viewBox="0 0 240 240"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle
            cx="120"
            cy="120"
            r="96"
            class="not-found__ring not-found__ring--outer"
          />
          <circle
            cx="120"
            cy="120"
            r="72"
            class="not-found__ring not-found__ring--inner"
            stroke-dasharray="8 12"
          />
          <path
            d="M120 36 L128 108 L120 120 L112 108 Z"
            class="not-found__needle not-found__needle--north"
          />
          <path
            d="M120 204 L112 132 L120 120 L128 132 Z"
            class="not-found__needle not-found__needle--south"
          />
          <circle
            cx="120"
            cy="120"
            r="10"
            class="not-found__hub"
          />
        </svg>

        <div class="not-found__beacon">
          <Icon icon="mdi:map-marker-question-outline" width="28" height="28" />
        </div>
      </div>

      <p class="not-found__visual-caption">
        无法定位目标页面
      </p>

      <svg
        class="not-found__wave"
        viewBox="0 0 48 800"
        preserveAspectRatio="none"
      >
        <path
          d="M48,0 C24,120 36,240 12,400 C36,560 24,680 48,800 L48,0 Z"
          fill="var(--nf-panel-bg)"
        />
      </svg>
    </aside>

    <main class="not-found__panel" role="alert">
      <div class="not-found__content">
        <span class="not-found__badge">错误 404</span>

        <h1 class="not-found__title">
          找不到<br>您要访问的页面
        </h1>
        <p class="not-found__desc">
          当前路径
          <code class="not-found__path">{{ route.fullPath }}</code>
          不存在。您可以返回上一页，或从工作台重新导航。
        </p>

        <ul class="not-found__hints">
          <li
            v-for="item in hints"
            :key="item.title"
            class="not-found__hint"
          >
            <span class="not-found__hint-icon">
              <Icon :icon="item.icon" width="20" height="20" />
            </span>
            <div>
              <strong>{{ item.title }}</strong>
              <p>{{ item.desc }}</p>
            </div>
          </li>
        </ul>

        <div class="not-found__actions">
          <el-button
            type="primary"
            size="large"
            class="not-found__btn-primary"
            @click="goHome"
          >
            返回首页
          </el-button>
          <el-button
            size="large"
            class="not-found__btn-secondary"
            @click="goBack"
          >
            返回上页
          </el-button>
        </div>

        <p class="not-found__brand">
          {{ appConfig.title }}
        </p>
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.not-found {
  position: relative;

  --nf-primary: #2563eb;
  --nf-primary-hover: #1d4ed8;
  --nf-visual-bg: linear-gradient(155deg, #eff6ff 0%, #f5f3ff 42%, #eef2ff 100%);
  --nf-panel-bg: #fff;
  --nf-text: #0f172a;
  --nf-text-muted: #64748b;
  --nf-card-bg: #fff;
  --nf-card-border: #e2e8f0;
  --nf-badge-bg: #2563eb;
  --nf-badge-text: #fff;
  --nf-ring: rgb(37 99 235 / 18%);
  --nf-hub: #2563eb;

  display: flex;
  min-height: 100vh;
  background: var(--nf-panel-bg);

  &__theme-toggle {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 10;
    color: var(--el-text-color-primary);
  }

  &__visual {
    position: relative;
    display: flex;
    flex: 1.15;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 0;
    padding: 48px 72px 48px 48px;
    overflow: hidden;
    background: var(--nf-visual-bg);
  }

  &__watermark {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 0;
    font-size: clamp(180px, 22vw, 280px);
    font-weight: 800;
    line-height: 1;
    color: transparent;
    letter-spacing: -0.06em;
    pointer-events: none;
    user-select: none;
    transform: translate(-50%, -54%);
    -webkit-text-stroke: 1.5px rgb(37 99 235 / 12%);
  }

  &__scene {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 240px;
    height: 240px;
    margin-bottom: 28px;
    animation: not-found-rise 0.6s ease both;
  }

  &__orbit {
    position: absolute;
    border: 1px dashed rgb(37 99 235 / 20%);
    border-radius: 50%;

    &--1 {
      inset: -20px;
      animation: not-found-spin 48s linear infinite;
    }

    &--2 {
      inset: -44px;
      animation: not-found-spin 72s linear infinite reverse;
    }
  }

  &__compass {
    width: 100%;
    height: 100%;
  }

  &__ring {
    fill: none;
    stroke: var(--nf-ring);
    stroke-width: 2;

    &--outer {
      stroke: rgb(37 99 235 / 28%);
    }
  }

  &__needle {
    &--north {
      fill: #2563eb;
    }

    &--south {
      fill: rgb(148 163 184 / 55%);
    }
  }

  &__hub {
    fill: var(--nf-hub);
    stroke: #fff;
    stroke-width: 3;
  }

  &__beacon {
    position: absolute;
    top: 18%;
    right: 8%;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    color: #fff;
    background: linear-gradient(135deg, #6366f1, #2563eb);
    border-radius: 14px;
    box-shadow: 0 12px 28px rgb(37 99 235 / 32%);
    animation: not-found-pulse 2.8s ease-in-out infinite;
  }

  &__visual-caption {
    position: relative;
    z-index: 1;
    margin: 0;
    font-size: 14px;
    font-weight: 500;
    color: var(--nf-text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
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
    background: var(--nf-panel-bg);
  }

  &__content {
    width: 100%;
    max-width: 440px;
    animation: not-found-rise 0.6s ease 0.1s both;
  }

  &__badge {
    display: inline-block;
    padding: 6px 14px;
    margin-bottom: 28px;
    font-size: 13px;
    font-weight: 500;
    color: var(--nf-badge-text);
    background: var(--nf-badge-bg);
    border-radius: 999px;
  }

  &__title {
    margin: 0 0 16px;
    font-size: clamp(28px, 3.2vw, 38px);
    font-weight: 700;
    line-height: 1.25;
    color: var(--nf-text);
    letter-spacing: -0.03em;
  }

  &__desc {
    margin: 0 0 28px;
    font-size: 15px;
    line-height: 1.75;
    color: var(--nf-text-muted);
  }

  &__path {
    padding: 2px 8px;
    font-family: ui-monospace, 'Cascadia Code', 'Segoe UI Mono', monospace;
    font-size: 13px;
    color: var(--nf-text);
    word-break: break-all;
    background: rgb(241 245 249 / 90%);
    border: 1px solid var(--nf-card-border);
    border-radius: 6px;
  }

  &__hints {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0;
    margin: 0 0 32px;
    list-style: none;
  }

  &__hint {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    padding: 14px 16px;
    background: var(--nf-card-bg);
    border: 1px solid var(--nf-card-border);
    border-radius: 12px;
    transition:
      border-color 0.2s ease,
      box-shadow 0.2s ease;

    &:hover {
      border-color: #bfdbfe;
      box-shadow: 0 6px 20px rgb(37 99 235 / 8%);
    }

    strong {
      display: block;
      margin-bottom: 2px;
      font-size: 14px;
      font-weight: 600;
      color: var(--nf-text);
    }

    p {
      margin: 0;
      font-size: 13px;
      line-height: 1.5;
      color: var(--nf-text-muted);
    }
  }

  &__hint-icon {
    display: flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    color: var(--nf-primary);
    background: rgb(239 246 255 / 90%);
    border-radius: 10px;
  }

  &__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  &__btn-primary {
    --el-button-bg-color: var(--nf-primary);
    --el-button-border-color: var(--nf-primary);
    --el-button-hover-bg-color: var(--nf-primary-hover);
    --el-button-hover-border-color: var(--nf-primary-hover);
    --el-button-active-bg-color: var(--nf-primary-hover);
    --el-button-active-border-color: var(--nf-primary-hover);

    min-width: 132px;
    cursor: pointer;
    transition: box-shadow 0.2s ease;

    &:hover {
      box-shadow: 0 8px 20px rgb(37 99 235 / 22%);
    }

    &:focus-visible {
      outline: 2px solid var(--nf-primary);
      outline-offset: 2px;
    }
  }

  &__btn-secondary {
    min-width: 132px;
    cursor: pointer;

    &:focus-visible {
      outline: 2px solid var(--nf-primary);
      outline-offset: 2px;
    }
  }

  &__brand {
    margin: 32px 0 0;
    font-size: 12px;
    color: var(--nf-text-muted);
  }
}

html.dark .not-found {
  --nf-visual-bg: linear-gradient(155deg, #0f172a 0%, #1e293b 48%, #1e1b4b 100%);
  --nf-panel-bg: var(--el-bg-color);
  --nf-text: var(--el-text-color-primary);
  --nf-text-muted: var(--el-text-color-secondary);
  --nf-card-bg: var(--el-bg-color-overlay);
  --nf-card-border: var(--el-border-color);
  --nf-badge-bg: #3b82f6;
  --nf-ring: rgb(96 165 250 / 22%);
  --nf-hub: #60a5fa;

  .not-found__watermark {
    -webkit-text-stroke-color: rgb(96 165 250 / 14%);
  }

  .not-found__path {
    background: rgb(30 41 59 / 80%);
    border-color: var(--el-border-color);
  }

  .not-found__hint-icon {
    background: rgb(30 58 138 / 35%);
  }

  .not-found__needle--north {
    fill: #60a5fa;
  }

  .not-found__wave path {
    fill: var(--el-bg-color);
  }
}

@media (prefers-reduced-motion: reduce) {
  .not-found__scene,
  .not-found__content {
    animation: none;
  }

  .not-found__orbit,
  .not-found__beacon {
    animation: none;
  }
}

@media (width <= 992px) {
  .not-found {
    flex-direction: column;
  }

  .not-found__visual {
    flex: none;
    min-height: 42vh;
    padding: 64px 24px 48px;
  }

  .not-found__wave {
    display: none;
  }

  .not-found__panel {
    flex: 1;
    padding: 32px 24px 48px;
  }

  .not-found__watermark {
    font-size: clamp(120px, 36vw, 200px);
  }
}

@media (width <= 480px) {
  .not-found__actions {
    flex-direction: column;
  }

  .not-found__btn-primary,
  .not-found__btn-secondary {
    width: 100%;
    min-width: 0;
  }
}

@keyframes not-found-rise {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes not-found-spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes not-found-pulse {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-4px);
  }
}
</style>
