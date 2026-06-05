<script setup lang="ts">
import packageJson from '../../../package.json'

defineOptions({ name: 'About' })

interface DepItem {
  name: string
  version: string
}

const REPO_URL = 'https://github.com/lin-97/gi-element-plus-admin'
const CODE_PREVIEW_URL = 'https://github1s.com/lin-97/gi-element-plus-admin/blob/HEAD/frontend/web/'

function toDepList(deps: Record<string, string>): DepItem[] {
  return Object.entries(deps)
    .map(([name, version]) => ({ name, version }))
    .sort((a, b) => a.name.localeCompare(b.name))
}

const dependencies = toDepList(packageJson.dependencies)
const devDependencies = toDepList(packageJson.devDependencies)
</script>

<template>
  <div class="about-page">
    <gi-card title="项目信息" class="about-page__info g-mb">
      <template #extra>
        <el-space>
          <el-row justify="center" align="middle" :style="{ width: '24px', height: '24px', color: '#fff', backgroundColor: `var(--el-color-primary-dark-2)` }" />
          <el-row justify="center" align="middle" :style="{ width: '24px', height: '24px', color: '#fff', backgroundColor: `var(--el-color-primary)` }" />
          <el-row v-for="i in [3, 5, 7, 8, 9]" :key="i" justify="center" align="middle" :style="{ width: '24px', height: '24px', color: '#fff', backgroundColor: `var(--el-color-primary-light-${i})` }">
            {{ i }}
          </el-row>
        </el-space>
      </template>
      <el-descriptions :column="1" border class="about-page__descriptions">
        <el-descriptions-item label="项目名称">
          {{ packageJson.name }}
        </el-descriptions-item>
        <el-descriptions-item label="版本">
          v{{ packageJson.version }}
        </el-descriptions-item>
        <el-descriptions-item label="代码仓库">
          <el-link :href="REPO_URL" target="_blank" type="primary">
            {{ REPO_URL }}
          </el-link>
        </el-descriptions-item>
        <el-descriptions-item label="代码预览">
          <el-link :href="CODE_PREVIEW_URL" target="_blank" type="primary">
            {{ CODE_PREVIEW_URL }}
          </el-link>
        </el-descriptions-item>
      </el-descriptions>
    </gi-card>

    <el-row :gutter="16">
      <el-col :xs="24" :lg="12">
        <gi-card title="生产依赖" class="about-page__deps g-mb">
          <el-table :data="dependencies" border stripe>
            <el-table-column prop="name" label="依赖包" min-width="180" show-overflow-tooltip />
            <el-table-column prop="version" label="版本" width="120" />
          </el-table>
        </gi-card>
      </el-col>

      <el-col :xs="24" :lg="12">
        <gi-card title="开发依赖" class="about-page__deps g-mb">
          <el-table :data="devDependencies" border stripe>
            <el-table-column prop="name" label="依赖包" min-width="180" show-overflow-tooltip />
            <el-table-column prop="version" label="版本" width="120" />
          </el-table>
        </gi-card>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
.about-page {
  height: 100%;
  padding: 16px;
  overflow: hidden auto;

  &__descriptions {
    :deep(.el-descriptions__label) {
      width: 100px;
      min-width: 100px;
    }

    :deep(.el-descriptions__content) {
      word-break: break-all;
      white-space: normal;
    }

    :deep(.el-link) {
      word-break: break-all;
      white-space: normal;
    }
  }
}
</style>
