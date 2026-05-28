<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { DictDataItem, DictTypeItem, StatusValue } from '@/apis/dict'
import { Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  deleteDictDataApi,
  deleteDictTypeApi,
  getDictDataListApi,
  getDictTypeListApi,
  updateDictDataStatusApi,
} from '@/apis/dict'
import { useDict } from '@/hooks/useDict'
import { useTable } from '@/hooks/useTable'
import DictDataFormDialog from './DictDataFormDialog.vue'
import DictTypeFormDialog from './DictTypeFormDialog.vue'

defineOptions({ name: 'SystemDict' })

const TypeFormDialogRef = useTemplateRef('TypeFormDialogRef')
const DataFormDialogRef = useTemplateRef('DataFormDialogRef')

const { options: statusOptions } = useDict('STATUS')

const typeLoading = ref(false)
const typeList = ref<DictTypeItem[]>([])
const selectedType = ref<DictTypeItem>()
const typeSearchName = ref('')
const typeStatusFilter = ref<StatusValue | ''>('')

const typeStatusSegmentedOptions: { label: string, value: StatusValue | '' }[] = [
  { label: '全部', value: '' },
  { label: '启用', value: '1' },
  { label: '禁用', value: '0' },
]

const dataQueryForm = reactive({
  label: '',
  status: undefined as StatusValue | undefined,
})

const dataFormColumns = computed<FormColumnItem[]>(() => [
  { field: 'label', label: '数据标签', type: 'input' },
  {
    field: 'status',
    label: '状态',
    type: 'select-v2',
    props: { options: statusOptions.value, clearable: true },
  },
])

const dataTableColumns: TableColumnItem[] = [
  { type: 'selection', width: 48, align: 'center' },
  { prop: 'label', label: '数据标签', minWidth: 120 },
  { prop: 'value', label: '数据键值', minWidth: 120 },
  { prop: 'status', label: '状态', width: 100, align: 'center', slotName: 'status' },
  { prop: 'sort', label: '排序', width: 80, align: 'center' },
  { prop: 'createTime', label: '创建时间', width: 180 },
  { prop: 'remark', label: '备注', minWidth: 200, showOverflowTooltip: true },
  {
    prop: 'action',
    label: '操作',
    width: 120,
    align: 'center',
    fixed: 'right',
    slotName: 'action',
  },
]

const {
  tableData,
  loading: dataLoading,
  pagination,
  selectedKeys,
  search: searchData,
  refresh: refreshData,
  onDelete: onDeleteData,
  onBatchDelete: onBatchDeleteData,
  onSelectionChange,
} = useTable({
  rowKey: 'id',
  immediate: false,
  listAPI: p => getDictDataListApi({
    ...p,
    typeId: selectedType.value!.id,
    label: dataQueryForm.label || undefined,
    status: dataQueryForm.status,
  }),
  deleteAPI: deleteDictDataApi,
})

const canAddData = computed(() => selectedType.value?.status === '1')

async function loadTypes() {
  typeLoading.value = true
  try {
    typeList.value = await getDictTypeListApi({
      name: typeSearchName.value || undefined,
      status: typeStatusFilter.value || undefined,
    })
    if (selectedType.value) {
      const found = typeList.value.find(t => t.id === selectedType.value!.id)
      if (found)
        selectedType.value = found
      else
        selectedType.value = typeList.value[0]
    }
    else {
      selectedType.value = typeList.value[0]
    }
    if (selectedType.value)
      searchData()
  }
  finally {
    typeLoading.value = false
  }
}

function selectType(row: DictTypeItem) {
  selectedType.value = row
  dataQueryForm.label = ''
  dataQueryForm.status = undefined
  searchData()
}

function handleTypeSearch() {
  loadTypes()
}

function handleTypeStatusChange() {
  loadTypes()
}

function handleTypeAdd() {
  TypeFormDialogRef.value?.openAdd()
}

function handleTypeEdit() {
  if (!selectedType.value) {
    ElMessage.warning('请先选择字典类型')
    return
  }
  TypeFormDialogRef.value?.openEdit(selectedType.value)
}

async function handleTypeDelete() {
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

function handleDataSearch() {
  if (!selectedType.value) {
    ElMessage.warning('请先选择字典类型')
    return
  }
  searchData()
}

function handleDataReset() {
  dataQueryForm.label = ''
  dataQueryForm.status = undefined
  handleDataSearch()
}

function handleDataAdd() {
  if (!selectedType.value) {
    ElMessage.warning('请先选择字典类型')
    return
  }
  if (!canAddData.value) {
    ElMessage.warning('字典类型已禁用，无法新增数据')
    return
  }
  DataFormDialogRef.value?.openAdd()
}

function handleDataEdit(row: DictDataItem) {
  DataFormDialogRef.value?.openEdit(row)
}

async function handleDataStatusSwitch(row: DictDataItem, val: string | number | boolean) {
  const next: StatusValue = val ? '1' : '0'
  if (row.status === next)
    return
  try {
    await updateDictDataStatusApi(row.id, next)
    row.status = next
    ElMessage.success(next === '1' ? '已启用' : '已禁用')
  }
  catch {
    refreshData()
  }
}

async function onTypeSuccess() {
  await loadTypes()
}

function onDataSuccess() {
  refreshData()
}

onMounted(loadTypes)
</script>

<template>
  <GiPageLayout class="g-page-layout">
    <template #left>
      <div v-loading="typeLoading" class="dict-type-panel">
        <el-input
          v-model="typeSearchName"
          placeholder="输入字典名称搜索"
          clearable
          @keyup.enter="handleTypeSearch"
          @clear="handleTypeSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="handleTypeSearch" />
          </template>
        </el-input>

        <el-space wrap>
          <gi-button type="add" @click="handleTypeAdd">
            新增
          </gi-button>
          <el-button type="primary" plain :disabled="!selectedType" @click="handleTypeEdit">
            编辑
          </el-button>
          <el-button
            type="danger"
            plain
            :disabled="!selectedType || selectedType.isSystem"
            @click="handleTypeDelete"
          >
            删除
          </el-button>
        </el-space>

        <el-segmented
          v-model="typeStatusFilter"
          block
          :options="typeStatusSegmentedOptions"
          @change="handleTypeStatusChange"
        />

        <el-scrollbar class="dict-type-panel__scroll">
          <ul v-if="typeList.length" class="dict-type-list">
            <li
              v-for="item in typeList"
              :key="item.id"
              class="dict-type-list__item"
              :class="{ 'is-active': selectedType?.id === item.id }"
              @click="selectType(item)"
            >
              <span class="dict-type-list__name">{{ item.name }}</span>
              <span class="dict-type-list__code">({{ item.code }})</span>
            </li>
          </ul>
          <el-empty v-else description="暂无字典类型" :image-size="64" />
        </el-scrollbar>
      </div>
    </template>

    <template #header>
      <GiForm
        :model-value="dataQueryForm"
        :columns="dataFormColumns"
        search
        :grid-item-props="{ span: { xs: 24, sm: 12, md: 12, lg: 8, xl: 6, xxl: 6 } }"
        @update:model-value="Object.assign(dataQueryForm, $event)"
        @search="handleDataSearch"
        @reset="handleDataReset"
      />
    </template>

    <template #tool>
      <el-space>
        <gi-button type="add" :disabled="!canAddData" @click="handleDataAdd">
          新增
        </gi-button>
        <el-button type="danger" :disabled="!selectedKeys.length" @click="onBatchDeleteData">
          批量删除
        </el-button>
      </el-space>
    </template>

    <GiTable
      v-loading="dataLoading"
      border
      :data="tableData"
      :columns="dataTableColumns"
      row-key="id"
      :pagination="pagination"
      @selection-change="onSelectionChange"
    >
      <template #status="{ row }">
        <el-switch
          :model-value="row.status === '1'"
          inline-prompt
          active-text="启用"
          inactive-text="禁用"
          @change="(val: string | number | boolean) => handleDataStatusSwitch(row, val)"
        />
      </template>
      <template #action="{ row }">
        <el-space :size="4">
          <el-button type="primary" link @click="handleDataEdit(row)">
            编辑
          </el-button>
          <el-button type="danger" link @click="onDeleteData(row)">
            删除
          </el-button>
        </el-space>
      </template>
    </GiTable>

    <DictDataFormDialog
      :key="selectedType?.id"
      ref="DataFormDialogRef"
      :type-id="selectedType?.id ?? ''"
      @success="onDataSuccess"
    />

    <DictTypeFormDialog ref="TypeFormDialogRef" @success="onTypeSuccess" />
  </GiPageLayout>
</template>

<style scoped lang="scss">
.dict-type-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  height: 100%;
  padding: 16px;
  box-sizing: border-box;
}

.dict-type-panel__scroll {
  flex: 1;
  min-height: 0;

  :deep(.el-scrollbar__view) {
    padding-right: 4px;
  }
}

.dict-type-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.dict-type-list__item {
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

    .dict-type-list__code {
      color: var(--el-color-primary-light-3);
    }
  }

  &:last-child {
    margin-bottom: 0;
  }
}

.dict-type-list__name {
  font-size: 14px;
}

.dict-type-list__code {
  margin-left: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}
</style>
