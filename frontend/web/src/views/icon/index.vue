<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useDebounceFn } from '@vueuse/core'
import {
  customIconList,
  filterIcons,
  iconParkList,
  paginateIcons,
} from './iconCatalog'
import IconGrid from './IconGrid.vue'

defineOptions({ name: 'SystemIcon' })

const PAGE_SIZE = 308

const tabOptions = [
  { label: 'Icon Park Outline', name: 'park' },
  { label: '自定义图标', name: 'custom' },
]

const activeTab = ref<'park' | 'custom'>('park')
const keyword = ref('')
const debouncedKeyword = ref('')
const parkPage = ref(1)

const applyKeyword = useDebounceFn((val: string) => {
  debouncedKeyword.value = val
  parkPage.value = 1
}, 200)

watch(keyword, (val) => {
  applyKeyword(val)
})

const filteredParkIcons = computed(() =>
  filterIcons(iconParkList, debouncedKeyword.value),
)

const filteredCustomIcons = computed(() =>
  filterIcons(customIconList, debouncedKeyword.value),
)

const pagedParkIcons = computed(() =>
  paginateIcons(filteredParkIcons.value, parkPage.value, PAGE_SIZE),
)

const displayIcons = computed(() =>
  activeTab.value === 'park' ? pagedParkIcons.value : filteredCustomIcons.value,
)

const parkTotal = computed(() => filteredParkIcons.value.length)

const resultCountText = computed(() => {
  const total = activeTab.value === 'park'
    ? parkTotal.value
    : filteredCustomIcons.value.length
  return `共 ${total} 个图标`
})

const showParkPager = computed(
  () => activeTab.value === 'park' && parkTotal.value > PAGE_SIZE,
)

watch(activeTab, () => {
  parkPage.value = 1
})
</script>

<template>
  <gi-page-layout class="system-icon-page g-page-layout">
    <gi-tabs v-model="activeTab" :options="tabOptions" inner>
      <template #extra>
        <el-space alignment="center">
          <el-input
            v-model="keyword"
            class="system-icon-page__search"
            placeholder="搜索图标名称，如 user、setting"
            clearable
          >
            <template #prefix>
              <Icon icon="icon-park-outline:search" width="16" height="16" />
            </template>
          </el-input>
          <span class="system-icon-page__count">{{ resultCountText }}</span>
        </el-space>
      </template>
    </gi-tabs>

    <div class="system-icon-page__body">
      <div class="system-icon-page__list">
        <IconGrid :icons="displayIcons" />
      </div>
      <footer v-if="showParkPager" class="system-icon-page__pager">
        <el-pagination
          v-model:current-page="parkPage"
          :page-size="PAGE_SIZE"
          :total="parkTotal"
          layout="total, prev, pager, next, jumper"
          background
        />
      </footer>
    </div>
  </gi-page-layout>
</template>

<style scoped lang="scss">
.system-icon-page__search {
  width: 280px;
}

.system-icon-page__count {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.system-icon-page__body {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.system-icon-page__list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 12px 0;
}

.system-icon-page__pager {
  flex-shrink: 0;
  display: flex;
  justify-content: flex-end;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
}
</style>
