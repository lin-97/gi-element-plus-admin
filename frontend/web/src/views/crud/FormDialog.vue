<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { GenderValue, StudentItem } from '@/apis/student'
import { ElMessage } from 'element-plus'
import { createStudentApi, updateStudentApi } from '@/apis/student'
import { useDict } from '@/hooks/useDict'
import { EMAIL_REG, PHONE_REG } from '@/utils/regexp'

defineOptions({ name: 'FormDialog' })

const emit = defineEmits<{
  (e: 'success'): void
}>()

const { dictData } = useDict(['GENDER'] as const)

interface StudentFormData {
  name: string
  studentNo: string
  gender?: GenderValue
  age?: number
  phone: string
  email: string
  address: string
}

const visible = ref(false)
const isEdit = ref(false)
const currentId = ref('')
const formRef = useTemplateRef<FormInstance>('formRef')
const formData = ref<StudentFormData>(createEmptyForm())
const dialogTitle = computed(() => (isEdit.value ? '编辑学生' : '新增学生'))

function createEmptyForm(): StudentFormData {
  return {
    name: '',
    studentNo: '',
    gender: '1',
    age: 18,
    phone: '',
    email: '',
    address: '',
  }
}

const formRules: FormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  studentNo: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  phone: [{ pattern: PHONE_REG, message: '请输入正确的11位手机号', trigger: 'blur' }],
  email: [{ pattern: EMAIL_REG, message: '请输入正确的邮箱地址', trigger: 'blur' }],
  address: [{
    validator: (_rule, value, callback) => {
      if (String(value ?? '').length <= 200)
        return callback()
      callback(new Error('地址不能超过200字'))
    },
    trigger: 'blur',
  }],
}

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'name', label: '姓名', type: 'input' },
  { field: 'studentNo', label: '学号', type: 'input' },
  {
    field: 'gender',
    label: '性别',
    type: 'radio-group',
    props: {
      options: dictData.value.GENDER,
    },
  },
  {
    field: 'age',
    label: '年龄',
    type: 'input-number',
    props: { min: 0, max: 150, controlsPosition: 'right' },
  },
  { field: 'phone', label: '电话', type: 'input' },
  { field: 'email', label: '邮箱', type: 'input' },
  {
    field: 'address',
    label: '地址',
    type: 'textarea',
    span: 24,
    props: { maxlength: 200, showWordLimit: true, rows: 3 },
  },
])

function toFormData(student: StudentItem): StudentFormData {
  return {
    name: student.name ?? '',
    studentNo: student.studentNo ?? '',
    gender: student.gender,
    age: student.age,
    phone: student.phone ?? '',
    email: student.email ?? '',
    address: student.address ?? '',
  }
}

function toPayload(data: StudentFormData): Partial<StudentItem> {
  const trim = (v: string) => v.trim()
  return {
    name: trim(data.name),
    studentNo: trim(data.studentNo),
    ...(data.gender && { gender: data.gender }),
    ...(data.age != null && { age: data.age }),
    ...(trim(data.phone) && { phone: trim(data.phone) }),
    ...(trim(data.email) && { email: trim(data.email) }),
    ...(trim(data.address) && { address: trim(data.address) }),
  }
}

function openAdd() {
  isEdit.value = false
  currentId.value = ''
  formData.value = createEmptyForm()
  visible.value = true
}

function openEdit(row: StudentItem) {
  isEdit.value = true
  currentId.value = row.id
  formData.value = toFormData(row)
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await formRef.value?.formRef?.validate()
    const payload = toPayload(formData.value)
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
  <gi-dialog
    v-model="visible"
    :title="dialogTitle"
    width="600px"
    :style="{ maxWidth: '600px' }"
    destroy-on-close
    :on-before-ok="handleBeforeOk"
  >
    <gi-form
      ref="formRef"
      v-model="formData"
      :columns="formColumns"
      :rules="formRules"
      label-width="80px"
    />
  </gi-dialog>
</template>
