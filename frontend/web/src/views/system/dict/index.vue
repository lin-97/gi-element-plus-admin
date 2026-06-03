<script setup lang="ts">
import type { FormColumnItem, TableColumnItem } from 'gi-component'
import type { DictDataItem, DictTypeItem, StatusValue } from '@/apis/dict'
import { ElMessage } from 'element-plus'
import {
  deleteDictDataApi,
  getDictDataListApi,
  updateDictDataStatusApi,
} from '@/apis/dict'
import { useDict } from '@/hooks/useDict'
import { useTable } from '@/hooks/useTable'
import DictDataFormDialog from './DictDataFormDialog.vue'
import DictTypePane from './DictTypePane.vue'

defineOptions({ name: 'SystemDict' })

const DataFormDialogRef = useTemplateRef('DataFormDialogRef')

const { dictData } = useDict(['STATUS'] as const)

const selectedType = ref<DictTypeItem>()

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
    props: { options: dictData.value.STATUS, clearable: true },
  },
])

const dataTableColumns: TableColumnItem[] = [
  { type: 'selection', width: 48, align: 'center', selectable: () => !selectedType?.value?.isSystem },
  { prop: 'label', label: '数据标签', minWidth: 120 },
  { prop: 'value', label: '数据键值', minWidth: 120 },
  { prop: 'status', label: '状态', width: 100, align: 'center', slotName: 'status' },
  { prop: 'sort', label: '排序', width: 80, align: 'center' },
  { prop: 'isSystem', label: '是否系统内置', width: 120, align: 'center', slotName: 'isSystem' },
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

function clearDataTable() {
  tableData.value = []
  pagination.total = 0
  pagination.currentPage = 1
  selectedKeys.value = []
}

function handleTypeSelect(type?: DictTypeItem) {
  if (!type) {
    clearDataTable()
    return
  }
  dataQueryForm.label = ''
  dataQueryForm.status = undefined
  searchData()
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
  if (!row?.id)
    return
  const status = val as StatusValue
  try {
    await updateDictDataStatusApi(row.id, status)
    ElMessage.success(status === '1' ? '已启用' : '已禁用')
  }
  catch {
    refreshData()
  }
}

function onDataSuccess() {
  refreshData()
}
</script>

<template>
  <gi-page-layout class="g-page-layout" :collapse="false">
    <template #left>
      <DictTypePane v-model="selectedType" @select="handleTypeSelect" />
    </template>

    <template #header>
      <gi-form
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
        <gi-button type="add" :disabled="!canAddData || selectedType?.isSystem" @click="handleDataAdd">
          新增
        </gi-button>
        <el-button type="danger" :disabled="!selectedKeys.length || selectedType?.isSystem" @click="onBatchDeleteData">
          批量删除
        </el-button>
      </el-space>
    </template>

    <gi-table
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
          v-model="row.status"
          active-value="1"
          inactive-value="0"
          inline-prompt
          active-text="启用"
          inactive-text="禁用"
          :disabled="selectedType?.isSystem"
          @change="val => handleDataStatusSwitch(row, val)"
        />
      </template>
      <template #isSystem>
        <el-tag v-if="selectedType?.isSystem" type="success">
          是
        </el-tag>
        <el-tag v-else type="info">
          否
        </el-tag>
      </template>
      <template #action="{ row }">
        <el-space :size="4">
          <el-button type="primary" link :disabled="selectedType?.isSystem" @click="handleDataEdit(row)">
            编辑
          </el-button>
          <el-button type="danger" link :disabled="selectedType?.isSystem" @click="onDeleteData(row)">
            删除
          </el-button>
        </el-space>
      </template>
    </gi-table>

    <DictDataFormDialog
      :key="selectedType?.id"
      ref="DataFormDialogRef"
      :type-id="selectedType?.id ?? ''"
      @success="onDataSuccess"
    />
  </gi-page-layout>
</template>
