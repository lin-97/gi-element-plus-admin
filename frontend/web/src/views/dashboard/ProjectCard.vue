<script setup lang="ts">
import { useTheme } from '@/core/hooks'

defineOptions({ name: 'ProjectCard' })

interface ProjectItem {
  name: string
  desc: string
  source: string
  icon: string
  iconDark?: string
}

const list: ProjectItem[] = [
  {
    name: 'Github',
    desc: '是一个面向开源及私有软件项目的托管平台',
    source: '开源君',
    icon: 'https://cdn.simpleicons.org/github/181717',
    iconDark: 'https://cdn.simpleicons.org/github/ffffff',
  },
  {
    name: 'Vue',
    desc: '渐进式 JavaScript 框架',
    source: '学不动也要学',
    icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg',
  },
  {
    name: 'Html5',
    desc: 'HTML5是互联网的下一代标准',
    source: '撸码也是一种艺术',
    icon: 'https://cdn.simpleicons.org/html5/e34f26',
  },
  {
    name: 'Angular',
    desc: '现代 Web 开发平台 百万粉丝热捧',
    source: '铁粉君',
    icon: 'https://cdn.simpleicons.org/angular/dd0031',
  },
  {
    name: 'React',
    desc: '用于构建用户界面的 JavaScript 库',
    source: '技术牛',
    icon: 'https://cdn.simpleicons.org/react/61dafb',
  },
  {
    name: 'JavaScript',
    desc: '路是走出来的 而不是空想出来的',
    source: '架构组',
    icon: 'https://cdn.simpleicons.org/javascript/f7df1e',
  },
]

const { isDark } = useTheme()

function getProjectIcon(item: ProjectItem) {
  if (isDark.value && item.iconDark)
    return item.iconDark
  return item.icon
}
</script>

<template>
  <gi-card title="项目" class="project-card">
    <el-row :gutter="0" class="project-card__list">
      <el-col
        v-for="item in list"
        :key="item.name"
        :xs="24"
        :sm="12"
        :md="8"
      >
        <div class="project-card__item">
          <div class="project-card__head">
            <img
              :src="getProjectIcon(item)"
              :alt="item.name"
              class="project-card__icon"
            >
            <span class="project-card__name">{{ item.name }}</span>
          </div>
          <p class="project-card__desc">
            {{ item.desc }}
          </p>
          <div class="project-card__footer">
            {{ item.source }}
          </div>
        </div>
      </el-col>
    </el-row>
  </gi-card>
</template>

<style lang="scss" scoped>
.project-card {
  &__list {
    border-top: 1px solid var(--el-border-color-lighter);
    border-left: 1px solid var(--el-border-color-lighter);
  }

  &__item {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 140px;
    padding: 16px;
    border-right: 1px solid var(--el-border-color-lighter);
    border-bottom: 1px solid var(--el-border-color-lighter);
    transition: background-color 0.2s;

    &:hover {
      background-color: var(--el-fill-color-light);
    }
  }

  &__head {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 10px;
  }

  &__icon {
    flex-shrink: 0;
    width: 22px;
    height: 22px;
    object-fit: contain;
  }

  &__name {
    font-size: 15px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }

  &__desc {
    display: -webkit-box;
    flex: 1;
    margin: 0 0 12px;
    overflow: hidden;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    font-size: 13px;
    line-height: 1.6;
    color: var(--el-text-color-regular);
    -webkit-box-orient: vertical;
  }

  &__footer {
    font-size: 12px;
    color: var(--el-text-color-placeholder);
  }
}
</style>
