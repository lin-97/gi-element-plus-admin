<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { StudentInfo } from '@/apis/student'
import { ElMessage } from 'element-plus'
import { GiDialog, GiForm } from 'gi-component'
import { createStudentApi, getStudentDetailApi, updateStudentApi } from '@/apis/student'

defineOptions({ name: 'FormDialog' })

const emit = defineEmits<{
  success: []
}>()

const visible = ref(false)
const isEdit = ref(false)
const currentId = ref<number>()
const formRef = ref<FormInstance>()

interface StudentFormData {
  name: string
  student_no: string
  gender: string
  age: string
  phone: string
  email: string
  address: string
}

function getDefaultFormData(): StudentFormData {
  return {
    name: '',
    student_no: '',
    gender: '',
    age: '',
    phone: '',
    email: '',
    address: '',
  }
}

/** GiForm 每次输入会 emit 新对象，需用 ref 承接 v-model */
const formData = ref<StudentFormData>(getDefaultFormData())

const dialogTitle = computed(() => (isEdit.value ? '编辑学生' : '新增学生'))

const formRules: FormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
}

const formColumns: FormColumnItem[] = [
  { field: 'name', label: '姓名', type: 'input' },
  { field: 'student_no', label: '学号', type: 'input' },
  {
    field: 'gender',
    label: '性别',
    type: 'select-v2',
    props: {
      options: [
        { label: '男', value: '男' },
        { label: '女', value: '女' },
      ],
    },
  },
  { field: 'age', label: '年龄', type: 'input' },
  { field: 'phone', label: '电话', type: 'input' },
  { field: 'email', label: '邮箱', type: 'input' },
  { field: 'address', label: '地址', type: 'input' },
]

function mapStudentToForm(res: StudentInfo): StudentFormData {
  return {
    name: res.name ?? '',
    student_no: res.student_no ?? '',
    gender: res.gender ?? '',
    age: res.age != null ? String(res.age) : '',
    phone: res.phone ?? '',
    email: res.email ?? '',
    address: res.address ?? '',
  }
}

function mapFormToPayload(data: StudentFormData): Partial<StudentInfo> {
  const payload: Partial<StudentInfo> = { name: data.name.trim() }
  const textFields = ['student_no', 'gender', 'phone', 'email', 'address'] as const
  for (const key of textFields) {
    const value = data[key]?.trim()
    if (value)
      payload[key] = value
  }
  if (data.age) {
    const age = Number(data.age)
    if (!Number.isNaN(age))
      payload.age = age
  }
  return payload
}

function openAdd() {
  isEdit.value = false
  currentId.value = undefined
  formData.value = getDefaultFormData()
  visible.value = true
}

async function openEdit(row: StudentInfo) {
  isEdit.value = true
  currentId.value = row.id
  const res = await getStudentDetailApi(row.id)
  formData.value = mapStudentToForm(res)
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await formRef.value?.formRef?.validate()
    const payload = mapFormToPayload(formData.value)
    if (isEdit.value && currentId.value) {
      await updateStudentApi(currentId.value, payload)
      ElMessage.success('更新成功')
    }
    else {
      await createStudentApi(payload)
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
    width="600px"
    :style="{ maxWidth: '600px' }"
    destroy-on-close
    :on-before-ok="handleBeforeOk"
  >
    <GiForm
      ref="formRef"
      v-model="formData"
      :columns="formColumns"
      :rules="formRules"
      label-width="80px"
    />
  </GiDialog>
</template>
