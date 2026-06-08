<script setup lang="ts">
import type { DictTypeItem, StatusValue } from '@/apis/dict'
import { Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { deleteDictTypeApi, getDictTypeListApi } from '@/apis/dict'
import DictTypeFormDialog from './DictTypeFormDialog.vue'

defineOptions({ name: 'DictTypePane' })

const emit = defineEmits<{
  (e: 'select', type?: DictTypeItem): void
}>()

const selectedType = defineModel<DictTypeItem | undefined>()

const TypeFormDialogRef = useTemplateRef('TypeFormDialogRef')

const loading = ref(false)
const typeList = ref<DictTypeItem[]>([])
const searchName = ref('')
const statusFilter = ref<StatusValue | ''>('')

const statusOptions: { label: string, value: StatusValue | '' }[] = [
  { label: '全部', value: '' },
  { label: '启用', value: '1' },
  { label: '禁用', value: '0' },
]

async function loadTypes() {
  loading.value = true
  try {
    const res = await getDictTypeListApi({
      name: searchName.value || undefined,
      status: statusFilter.value || undefined,
    })
    typeList.value = res ?? []

    let next: DictTypeItem | undefined
    if (!typeList.value.length) {
      next = undefined
    }
    else if (selectedType.value) {
      next = typeList.value.find(t => t.id === selectedType.value!.id) ?? typeList.value[0]
    }
    else {
      next = typeList.value[0]
    }

    selectedType.value = next
    // defineModel 赋值后同步读取 selectedType.value 可能仍是父组件旧值，emit 使用局部变量 next
    emit('select', next)
  }
  finally {
    loading.value = false
  }
}

function handleSearch() {
  loadTypes()
}

function handleStatusChange() {
  loadTypes()
}

function handleSelect(row: DictTypeItem) {
  selectedType.value = row
  emit('select', row)
}

function handleAdd() {
  TypeFormDialogRef.value?.openAdd()
}

function handleEdit() {
  if (!selectedType.value) {
    ElMessage.warning('请先选择字典类型')
    return
  }
  TypeFormDialogRef.value?.openEdit(selectedType.value)
}

async function handleDelete() {
  if (!selectedType.value) {
    ElMessage.warning('请先选择字典类型')
    return
  }
  if (selectedType.value.isSystem) {
    ElMessage.warning('系统字典不可删除')
    return
  }
  try {
    await ElMessageBox.confirm(
      `删除字典类型「${selectedType.value.name}」将同时删除其下所有字典数据，是否继续？`,
      '提示',
      { type: 'warning' },
    )
    await deleteDictTypeApi([selectedType.value.id])
    ElMessage.success('删除成功')
    selectedType.value = undefined
    await loadTypes()
  }
  catch {
    /* cancelled */
  }
}

async function handleFormSuccess() {
  await loadTypes()
}

onMounted(loadTypes)

defineExpose({ reload: loadTypes })
</script>

<template>
  <div v-loading="loading" class="dict-type-pane">
    <el-input v-model="searchName" placeholder="输入字典名称搜索" clearable @keyup.enter="handleSearch" @clear="handleSearch">
      <template #append>
        <el-button :icon="Search" @click="handleSearch" />
      </template>
    </el-input>

    <el-row>
      <gi-button type="add" class="g-flex-1" @click="handleAdd">
        新增
      </gi-button>
      <el-button type="primary" plain class="g-flex-1" :disabled="!selectedType" @click="handleEdit">
        编辑
      </el-button>
      <el-button type="danger" plain class="g-flex-1" :disabled="!selectedType || selectedType.isSystem" @click="handleDelete">
        删除
      </el-button>
    </el-row>

    <el-radio-group v-model="statusFilter" class="dict-type-pane__status" @change="handleStatusChange">
      <el-radio-button v-for="item in statusOptions" :key="item.label" :value="item.value">
        {{ item.label }}
      </el-radio-button>
    </el-radio-group>

    <el-scrollbar class="dict-type-pane__scroll">
      <ul v-if="typeList.length" class="dict-type-pane__list">
        <li
          v-for="item in typeList" :key="item.id" class="dict-type-pane__item"
          :class="{ 'is-active': selectedType?.id === item.id }" @click="handleSelect(item)"
        >
          <span class="dict-type-pane__name">{{ item.name }}</span>
          <span class="dict-type-pane__code">({{ item.code }})</span>
        </li>
      </ul>
      <el-empty v-else description="暂无字典类型" :image-size="64" />
    </el-scrollbar>

    <DictTypeFormDialog ref="TypeFormDialogRef" @success="handleFormSuccess" />
  </div>
</template>

<style scoped lang="scss">
.dict-type-pane {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  height: 100%;
  padding: 16px;
  box-sizing: border-box;
}

.dict-type-pane__status {
  display: flex;
  width: 100%;

  :deep(.el-radio-button) {
    flex: 1;
  }

  :deep(.el-radio-button__inner) {
    width: 100%;
  }
}

.dict-type-pane__scroll {
  flex: 1;
  min-height: 0;
}

.dict-type-pane__list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.dict-type-pane__item {
  display: block;
  padding: 10px 12px;
  margin-bottom: 4px;
  border-radius: var(--el-border-radius-base);
  cursor: pointer;
  transition:
    background-color 0.2s,
    color 0.2s;
  line-height: 1.5;

  &:hover {
    background-color: var(--el-fill-color-light);
  }

  &.is-active {
    background-color: var(--el-color-primary-light-9);
    color: var(--el-color-primary);

    .dict-type-pane__code {
      color: var(--el-color-primary-light-3);
    }
  }

  &:last-child {
    margin-bottom: 0;
  }
}

.dict-type-pane__name {
  font-size: 14px;
}

.dict-type-pane__code {
  margin-left: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}
</style>
