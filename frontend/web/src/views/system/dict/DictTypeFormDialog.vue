<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { DictTypeItem } from '@/apis/dict'
import { ElMessage } from 'element-plus'
import { createDictTypeApi, updateDictTypeApi } from '@/apis/dict'
import { clearDictCache, useDict } from '@/hooks/useDict'
import { useFormDialog } from '@/hooks/useFormDialog'

defineOptions({ name: 'DictTypeFormDialog' })

const emit = defineEmits<{
  (e: 'success'): void
}>()

const { dictData } = useDict(['STATUS'] as const)

interface DictTypeFormData {
  name: string
  code: string
  status: '0' | '1'
  sort: number
  remark: string
}

const formRef = useTemplateRef<FormInstance>('formRef')

function createEmptyForm(): DictTypeFormData {
  return { name: '', code: '', status: '1', sort: 0, remark: '' }
}

const formRules: FormRules = {
  name: [{ required: true, message: '请输入字典名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入字典编码', trigger: 'blur' }],
}

const {
  visible,
  isEdit,
  formData,
  dialogTitle,
  openAdd,
  openEdit,
  handleBeforeOk,
} = useFormDialog<DictTypeFormData, DictTypeItem>({
  formRef,
  createEmptyForm,
  toFormData: row => ({
    name: row.name,
    code: row.code,
    status: row.status,
    sort: row.sort ?? 0,
    remark: row.remark ?? '',
  }),
  titles: { add: '新增字典类型', edit: '编辑字典类型' },
  submit: async ({ isEdit, id, data }) => {
    if (isEdit && id) {
      await updateDictTypeApi(id, {
        name: data.name,
        status: data.status,
        sort: data.sort,
        remark: data.remark,
      })
      ElMessage.success('更新成功')
    }
    else {
      await createDictTypeApi(data)
      ElMessage.success('添加成功')
    }
    clearDictCache(data.code)
  },
  onSuccess: () => emit('success'),
})

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'name', label: '字典名称', type: 'input' },
  {
    field: 'code',
    label: '字典编码',
    type: 'input',
    props: { disabled: isEdit.value, placeholder: '如 GENDER' },
  },
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
