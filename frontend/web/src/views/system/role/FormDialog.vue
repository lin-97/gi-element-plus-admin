<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { RoleItem } from '@/apis/role'
import { ElMessage } from 'element-plus'
import { createRoleApi, STATUS_OPTIONS, updateRoleApi } from '@/apis/role'
import { SUPER_ADMIN_ROLE } from '@/core/config'

defineOptions({ name: 'SystemRoleFormDialog' })

const emit = defineEmits<{ success: [] }>()

interface RoleFormData {
  code: string
  name: string
  status: '0' | '1'
  sort: number
  remark: string
}

const visible = ref(false)
const isEdit = ref(false)
const isSystemRole = ref(false)
const currentId = ref<number>()
const formRef = ref<FormInstance>()
const formData = ref<RoleFormData>(createEmptyForm())
const dialogTitle = computed(() => (isEdit.value ? '编辑角色' : '新增角色'))

function createEmptyForm(): RoleFormData {
  return { code: '', name: '', status: '1', sort: 0, remark: '' }
}

const formRules: FormRules = {
  code: [{ required: true, message: '请输入角色标识', trigger: 'blur' }],
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
}

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'code', label: '角色标识', type: 'input', props: { disabled: isEdit.value } },
  { field: 'name', label: '角色名称', type: 'input' },
  {
    field: 'status',
    label: '状态',
    type: 'radio-group',
    props: { options: STATUS_OPTIONS, disabled: isSystemRole.value },
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

function toFormData(row: RoleItem): RoleFormData {
  return {
    code: row.code ?? '',
    name: row.name ?? '',
    status: row.status ?? '1',
    sort: row.sort ?? 0,
    remark: row.remark ?? '',
  }
}

function openAdd() {
  isEdit.value = false
  isSystemRole.value = false
  currentId.value = undefined
  formData.value = createEmptyForm()
  visible.value = true
}

function openEdit(row: RoleItem) {
  isEdit.value = true
  isSystemRole.value = row.code === SUPER_ADMIN_ROLE
  currentId.value = row.id
  formData.value = toFormData(row)
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await formRef.value?.formRef?.validate()
    const { code, ...rest } = formData.value
    if (isEdit.value && currentId.value) {
      const payload = isSystemRole.value ? { name: rest.name, sort: rest.sort, remark: rest.remark } : rest
      await updateRoleApi(currentId.value, payload)
      ElMessage.success('更新成功')
    }
    else {
      await createRoleApi(formData.value)
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
  <GiDialog
    v-model="visible"
    :title="dialogTitle"
    width="calc(100% - 20px)"
    :style="{ maxWidth: '600px' }"
    destroy-on-close
    :on-before-ok="handleBeforeOk"
  >
    <GiForm
      ref="formRef"
      v-model="formData"
      :columns="formColumns"
      :rules="formRules"
      label-width="90px"
    />
  </GiDialog>
</template>
