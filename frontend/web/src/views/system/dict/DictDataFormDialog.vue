<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { DictDataItem } from '@/apis/dict'
import { ElMessage } from 'element-plus'
import { createDictDataApi, updateDictDataApi } from '@/apis/dict'
import { useDict } from '@/hooks/useDict'

defineOptions({ name: 'DictDataFormDialog' })

const props = defineProps<{
  typeId: string
}>()

const emit = defineEmits<{
  (e: 'success'): void
}>()

const { dictData } = useDict(['STATUS'] as const)

interface DictDataFormData {
  label: string
  value: string
  status: '0' | '1'
  sort: number
  remark: string
}

const visible = ref(false)
const isEdit = ref(false)
const currentId = ref('')
const formRef = useTemplateRef<FormInstance>('formRef')
const formData = ref<DictDataFormData>(createEmptyForm())
const dialogTitle = computed(() => (isEdit.value ? '编辑字典数据' : '新增字典数据'))

function createEmptyForm(): DictDataFormData {
  return { label: '', value: '', status: '1', sort: 0, remark: '' }
}

const formRules: FormRules = {
  label: [{ required: true, message: '请输入数据标签', trigger: 'blur' }],
  value: [{ required: true, message: '请输入数据键值', trigger: 'blur' }],
}

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'label', label: '数据标签', type: 'input' },
  { field: 'value', label: '数据键值', type: 'input', props: { placeholder: '字符串，如 1' } },
  {
    field: 'status',
    label: '状态',
    type: 'radio-group',
    props: { options: dictData.value.STATUS },
  },
  {
    field: 'sort',
    label: '排序',
    type: 'input-number',
    props: { min: 0, controlsPosition: 'right' },
  },
  {
    field: 'remark',
    label: '备注',
    type: 'textarea',
    span: 24,
    props: { maxlength: 500, showWordLimit: true, rows: 3 },
  },
])

function openAdd() {
  isEdit.value = false
  currentId.value = ''
  formData.value = createEmptyForm()
  visible.value = true
}

function openEdit(row: DictDataItem) {
  isEdit.value = true
  currentId.value = row.id
  formData.value = {
    label: row.label,
    value: row.value,
    status: row.status,
    sort: row.sort ?? 0,
    remark: row.remark ?? '',
  }
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await formRef.value?.formRef?.validate()
    if (isEdit.value && currentId.value) {
      await updateDictDataApi(currentId.value, {
        label: formData.value.label,
        value: formData.value.value,
        status: formData.value.status,
        sort: formData.value.sort,
        remark: formData.value.remark,
      })
      ElMessage.success('更新成功')
    }
    else {
      await createDictDataApi({
        typeId: props.typeId,
        ...formData.value,
      })
      ElMessage.success('添加成功')
    }
    emit('success')
    return true
  }
  catch {
    return false
  }
}

defineExpose({ openAdd, openEdit })
</script>

<template>
  <gi-dialog
    v-model="visible"
    :title="dialogTitle"
    width="calc(100% - 20px)"
    :style="{ maxWidth: '600px' }"
    destroy-on-close
    :on-before-ok="handleBeforeOk"
  >
    <gi-form
      ref="formRef"
      v-model="formData"
      :columns="formColumns"
      :rules="formRules"
      label-width="90px"
    />
  </gi-dialog>
</template>
