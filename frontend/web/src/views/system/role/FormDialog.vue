<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { MenuItem } from '@/apis/menu'
import type { RoleItem } from '@/apis/role'
import { ElMessage } from 'element-plus'
import { getMenuTreeApi } from '@/apis/menu'
import {
  createRoleApi,
  getRoleMenusApi,
  updateRoleApi,
  updateRoleMenusApi,
} from '@/apis/role'
import { SUPER_ADMIN_ROLE } from '@/core/config'
import { useDict } from '@/hooks/useDict'
import { useUserStore } from '@/stores/useUserStore'

defineOptions({ name: 'SystemRoleFormDialog' })

const emit = defineEmits<{ success: [] }>()

const userStore = useUserStore()
const { options: statusOptions } = useDict('STATUS')

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
const menuTreeRef = ref()
const menuTreeData = ref<MenuItem[]>([])
const checkedMenuIds = ref<number[]>([])
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
    props: { options: statusOptions.value, disabled: isSystemRole.value },
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

const menuTreeProps = { label: 'title', children: 'children' }

async function loadMenuTree() {
  menuTreeData.value = await getMenuTreeApi()
}

async function loadRoleMenus(roleId: number) {
  const { menuIds } = await getRoleMenusApi(roleId)
  checkedMenuIds.value = menuIds
  await nextTick()
  menuTreeRef.value?.setCheckedKeys(menuIds.map(String))
}

function toFormData(row: RoleItem): RoleFormData {
  return {
    code: row.code ?? '',
    name: row.name ?? '',
    status: row.status ?? '1',
    sort: row.sort ?? 0,
    remark: row.remark ?? '',
  }
}

async function openAdd() {
  isEdit.value = false
  isSystemRole.value = false
  currentId.value = undefined
  formData.value = createEmptyForm()
  checkedMenuIds.value = []
  visible.value = true
  await loadMenuTree()
  await nextTick()
  menuTreeRef.value?.setCheckedKeys([])
}

async function openEdit(row: RoleItem) {
  isEdit.value = true
  isSystemRole.value = row.code === SUPER_ADMIN_ROLE
  currentId.value = row.id
  formData.value = toFormData(row)
  visible.value = true
  await loadMenuTree()
  if (!isSystemRole.value)
    await loadRoleMenus(row.id)
}

function getSelectedMenuIds(): number[] {
  if (isSystemRole.value)
    return []
  const checked = (menuTreeRef.value?.getCheckedKeys(false) ?? []) as Array<string | number>
  const half = (menuTreeRef.value?.getHalfCheckedKeys() ?? []) as Array<string | number>
  return [...new Set([...checked, ...half])].map(id => Number(id))
}

async function handleBeforeOk() {
  try {
    await formRef.value?.formRef?.validate()
    const menuIds = getSelectedMenuIds()
    let roleId = currentId.value
    if (isEdit.value && roleId) {
      const payload = isSystemRole.value
        ? { name: formData.value.name, sort: formData.value.sort, remark: formData.value.remark }
        : { name: formData.value.name, status: formData.value.status, sort: formData.value.sort, remark: formData.value.remark }
      await updateRoleApi(roleId, payload)
      if (!isSystemRole.value) {
        await updateRoleMenusApi(roleId, menuIds)
      }
      ElMessage.success('更新成功')
    }
    else {
      const created = await createRoleApi(formData.value)
      roleId = created.id
      if (roleId && menuIds.length) {
        await updateRoleMenusApi(roleId, menuIds)
      }
      ElMessage.success('添加成功')
    }
    if (!isSystemRole.value) {
      await userStore.refreshRoutes()
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
    :style="{ maxWidth: '720px' }"
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
    <el-divider content-position="left">
      菜单权限
    </el-divider>
    <p v-if="isSystemRole" class="menu-tree-tip">
      超级管理员拥有全部菜单，无需分配。
    </p>
    <el-tree
      v-else
      ref="menuTreeRef"
      :data="menuTreeData"
      show-checkbox
      node-key="id"
      :props="menuTreeProps"
      default-expand-all
      :default-checked-keys="checkedMenuIds"
    />
  </GiDialog>
</template>

<style scoped>
.menu-tree-tip {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}
</style>
