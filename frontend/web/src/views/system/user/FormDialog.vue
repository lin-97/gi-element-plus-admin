<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { RoleOption } from '@/apis/role'
import type { SysUserItem } from '@/apis/user'
import { ElMessage } from 'element-plus'
import { getRoleOptionsApi } from '@/apis/role'
import { AVATAR_MAX_LENGTH, createUserApi, updateUserApi } from '@/apis/user'
import { useDict } from '@/hooks/useDict'
import { EMAIL_REG, PHONE_REG } from '@/utils/regexp'

defineOptions({ name: 'SystemUserFormDialog' })

const emit = defineEmits<{
  (e: 'success'): void
}>()

const { dictData } = useDict(['STATUS'] as const)

interface UserFormData {
  username: string
  password: string
  nickname: string
  phone: string
  email: string
  avatar: string
  remark: string
  status: '0' | '1'
  sort: number
  roleIds: string[]
}

const visible = ref(false)
const isEdit = ref(false)
const isSuperAdmin = ref(false)
const currentId = ref('')
const formRef = useTemplateRef<FormInstance>('formRef')
const roleOptions = ref<RoleOption[]>([])
const formData = ref<UserFormData>(createEmptyForm())
const dialogTitle = computed(() => (isEdit.value ? '编辑用户' : '新增用户'))

function createEmptyForm(): UserFormData {
  return {
    username: '',
    password: '',
    nickname: '',
    phone: '',
    email: '',
    avatar: '',
    remark: '',
    status: '1',
    sort: 0,
    roleIds: [],
  }
}

const formRules = computed<FormRules>(() => ({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: isEdit.value
    ? []
    : [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码至少6位', trigger: 'blur' },
      ],
  phone: [{ pattern: PHONE_REG, message: '请输入正确的11位手机号', trigger: 'blur' }],
  email: [{ pattern: EMAIL_REG, message: '请输入正确的邮箱地址', trigger: 'blur' }],
  avatar: [{ max: AVATAR_MAX_LENGTH, message: `头像URL不能超过${AVATAR_MAX_LENGTH}个字符`, trigger: 'blur' }],
  roleIds: isSuperAdmin.value
    ? []
    : [{ required: true, type: 'array', min: 1, message: '请选择角色', trigger: 'change' }],
}))

const roleSelectOptions = computed(() =>
  roleOptions.value.map(r => ({ label: r.name, value: r.id })),
)

const formColumns = computed<FormColumnItem[]>(() => [
  { field: 'username', label: '用户名', type: 'input', props: { disabled: isEdit.value } },
  ...(isEdit.value
    ? []
    : [{ field: 'password', label: '密码', type: 'input', props: { type: 'password', showPassword: true } } as FormColumnItem]),
  { field: 'nickname', label: '昵称', type: 'input' },
  { field: 'phone', label: '手机', type: 'input' },
  { field: 'email', label: '邮箱', type: 'input' },
  {
    field: 'avatar',
    label: '头像URL',
    type: 'input',
    span: 24,
    props: {
      maxlength: AVATAR_MAX_LENGTH,
      showWordLimit: true,
      placeholder: `请输入头像图片地址，最多${AVATAR_MAX_LENGTH}字符`,
    },
  },
  {
    field: 'roleIds',
    label: '角色',
    type: 'select-v2',
    props: {
      options: roleSelectOptions.value,
      multiple: true,
      collapseTags: true,
      disabled: isSuperAdmin.value,
    },
  },
  {
    field: 'sort',
    label: '排序',
    type: 'input-number',
    props: { min: 0, controlsPosition: 'right' },
  },
  {
    field: 'status',
    label: '状态',
    type: 'radio-group',
    props: {
      options: dictData.value.STATUS,
      disabled: isSuperAdmin.value,
    },
  },
  {
    field: 'remark',
    label: '备注',
    type: 'textarea',
    span: 24,
    props: { maxlength: 500, showWordLimit: true, rows: 3 },
  },
])

async function loadRoleOptions() {
  roleOptions.value = await getRoleOptionsApi()
}

function toFormData(row: SysUserItem): UserFormData {
  return {
    username: row.username ?? '',
    password: '',
    nickname: row.nickname ?? '',
    phone: row.phone ?? '',
    email: row.email ?? '',
    avatar: row.avatar ?? '',
    remark: row.remark ?? '',
    status: row.status ?? '1',
    sort: row.sort ?? 0,
    roleIds: row.roleIds ?? [],
  }
}

function openAdd() {
  isEdit.value = false
  isSuperAdmin.value = false
  currentId.value = ''
  formData.value = createEmptyForm()
  loadRoleOptions()
  visible.value = true
}

function openEdit(row: SysUserItem) {
  isEdit.value = true
  isSuperAdmin.value = !!row.isSuperAdmin
  currentId.value = row.id
  formData.value = toFormData(row)
  loadRoleOptions()
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await formRef.value?.formRef?.validate()
    const trim = (v: string) => v.trim()
    const payload: Record<string, unknown> = {
      nickname: trim(formData.value.nickname) || undefined,
      phone: trim(formData.value.phone) || undefined,
      email: trim(formData.value.email) || undefined,
      avatar: trim(formData.value.avatar) || undefined,
      remark: trim(formData.value.remark) || undefined,
      sort: formData.value.sort,
    }
    if (!isSuperAdmin.value) {
      payload.status = formData.value.status
      payload.roleIds = formData.value.roleIds
    }
    if (isEdit.value && currentId.value) {
      await updateUserApi(currentId.value, {
        ...payload,
        username: formData.value.username,
      } as Parameters<typeof updateUserApi>[1])
      ElMessage.success('更新成功')
    }
    else {
      await createUserApi({
        ...payload,
        username: trim(formData.value.username),
        password: formData.value.password,
        status: formData.value.status,
        roleIds: formData.value.roleIds,
      } as Parameters<typeof createUserApi>[0])
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
