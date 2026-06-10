<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { DictDataItem } from '@/apis/dict'
import { ElMessage } from 'element-plus'
import { createDictDataApi, updateDictDataApi } from '@/apis/dict'
import { clearDictCache, useDict } from '@/hooks/useDict'
import { useFormDialog } from '@/hooks/useFormDialog'

defineOptions({ name: 'DictDataFormDialog' })

const props = defineProps<{
  typeId: string
  typeCode: string
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

const formRef = useTemplateRef<FormInstance>('formRef')

function createEmptyForm(): DictDataFormData {
  return { label: '', value: '', status: '1', sort: 0, remark: '' }
}

const formRules: FormRules = {
  label: [{ required: true, message: '请输入数据标签', trigger: 'blur' }],
  value: [{ required: true, message: '请输入数据键值', trigger: 'blur' }],
}

const {
  visible,
  formData,
  dialogTitle,
  openAdd,
  openEdit,
  handleBeforeOk,
} = useFormDialog<DictDataFormData, DictDataItem>({
  formRef,
  createEmptyForm,
  toFormData: row => ({
    label: row.label,
    value: row.value,
    status: row.status,
    sort: row.sort ?? 0,
    remark: row.remark ?? '',
  }),
  titles: { add: '新增字典数据', edit: '编辑字典数据' },
  submit: async ({ isEdit, id, data }) => {
    if (isEdit && id) {
      await updateDictDataApi(id, {
        label: data.label,
        value: data.value,
        status: data.status,
        sort: data.sort,
        remark: data.remark,
      })
      ElMessage.success('更新成功')
    }
    else {
      await createDictDataApi({
        typeId: props.typeId,
        ...data,
      })
      ElMessage.success('添加成功')
    }
    if (props.typeCode) {
      clearDictCache(props.typeCode)
    }
  },
  onSuccess: () => emit('success'),
})

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
