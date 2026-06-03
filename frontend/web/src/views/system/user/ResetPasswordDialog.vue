<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { resetUserPasswordApi } from '@/apis/user'

defineOptions({ name: 'ResetPasswordDialog' })

const visible = ref(false)
const userId = ref<string>()
const username = ref('')
const formRef = useTemplateRef<FormInstance>('formRef')
const formData = ref({ password: '', confirmPassword: '' })

const formRules: FormRules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== formData.value.password)
          callback(new Error('两次输入的密码不一致'))
        else
          callback()
      },
      trigger: 'blur',
    },
  ],
}

function open(id: string, name: string) {
  userId.value = id
  username.value = name
  formData.value = { password: '', confirmPassword: '' }
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await formRef.value?.validate()
    if (!userId.value)
      return false
    await resetUserPasswordApi(userId.value, formData.value.password)
    ElMessage.success('密码重置成功')
    return true
  }
  catch {
    return false
  }
}

defineExpose({ open })
</script>

<template>
  <gi-dialog
    v-model="visible"
    :title="`重置密码 - ${username}`"
    width="440px"
    destroy-on-close
    :on-before-ok="handleBeforeOk"
  >
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="90px">
      <el-form-item label="新密码" prop="password">
        <el-input v-model="formData.password" type="password" show-password autocomplete="new-password" />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="formData.confirmPassword" type="password" show-password autocomplete="new-password" />
      </el-form-item>
    </el-form>
  </gi-dialog>
</template>
