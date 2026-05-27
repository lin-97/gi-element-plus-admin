<script setup lang="ts">
import type { FormRules } from 'element-plus'
import type { FormColumnItem, FormInstance } from 'gi-component'
import type { MenuFormData, MenuItem, MenuType } from '@/apis/menu'
import { ElMessage } from 'element-plus'
import { createMenuApi, updateMenuApi } from '@/apis/menu'
import { STATUS_OPTIONS } from '@/apis/role'

defineOptions({ name: 'SystemMenuFormDialog' })

const emit = defineEmits<{ success: [] }>()

const TYPE_OPTIONS = [
  { label: '目录', value: 1 as MenuType },
  { label: '菜单', value: 2 as MenuType },
  { label: '按钮', value: 3 as MenuType },
]

const visible = ref(false)
const isEdit = ref(false)
const isSystemMenu = ref(false)
const currentId = ref<string>()
const formRef = ref<FormInstance>()
const formData = ref<MenuFormData>(createEmptyForm(2))
const dialogTitle = computed(() => (isEdit.value ? '编辑菜单' : '新增菜单'))

function createEmptyForm(type: MenuType, parentId = '0'): MenuFormData {
  return {
    parentId,
    type,
    title: '',
    path: '',
    component: '',
    redirect: '',
    icon: '',
    permission: '',
    sort: 0,
    status: '1',
    hidden: false,
    keepAlive: false,
    affix: false,
    alwaysShow: false,
    breadcrumb: true,
    showInTabs: true,
    activeMenu: '',
  }
}

const formRules = computed<FormRules>(() => ({
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  permission: formData.value.type === 3
    ? [{ required: true, message: '请输入权限标识', trigger: 'blur' }]
    : [],
}))

const formColumns = computed<FormColumnItem[]>(() => {
  const cols: FormColumnItem[] = [
    {
      field: 'type',
      label: '类型',
      type: 'select-v2',
      props: { options: TYPE_OPTIONS, disabled: isEdit.value || isSystemMenu.value },
    },
    { field: 'title', label: '标题', type: 'input' },
  ]
  if (formData.value.type !== 3) {
    cols.push(
      { field: 'path', label: '路径', type: 'input' },
      { field: 'icon', label: '图标', type: 'input' },
    )
  }
  if (formData.value.type === 1) {
    cols.push(
      { field: 'component', label: '组件', type: 'input', props: { placeholder: 'Layout' } },
      { field: 'redirect', label: '重定向', type: 'input' },
      { field: 'alwaysShow', label: '始终显示', type: 'switch' },
    )
  }
  if (formData.value.type === 2) {
    cols.push(
      { field: 'component', label: '组件路径', type: 'input', props: { placeholder: 'system/user/index' } },
      { field: 'permission', label: '页面权限', type: 'input' },
      { field: 'keepAlive', label: '缓存', type: 'switch' },
    )
  }
  if (formData.value.type === 3) {
    cols.push({ field: 'permission', label: '权限标识', type: 'input' })
  }
  cols.push(
    {
      field: 'status',
      label: '状态',
      type: 'radio-group',
      props: { options: STATUS_OPTIONS, disabled: isSystemMenu.value },
    },
    {
      field: 'sort',
      label: '排序',
      type: 'input-number',
      props: { min: 0, controlsPosition: 'right' },
    },
  )
  return cols
})

function toFormData(row: MenuItem): MenuFormData {
  return {
    parentId: row.parentId ?? '0',
    type: row.type,
    title: row.title ?? '',
    path: row.path ?? '',
    component: row.component ?? '',
    redirect: row.redirect ?? '',
    icon: row.icon ?? '',
    permission: row.permission ?? '',
    sort: row.sort ?? 0,
    status: row.status ?? '1',
    hidden: row.hidden ?? false,
    keepAlive: row.keepAlive ?? false,
    affix: row.affix ?? false,
    alwaysShow: row.alwaysShow ?? false,
    breadcrumb: row.breadcrumb ?? true,
    showInTabs: row.showInTabs ?? true,
    activeMenu: row.activeMenu ?? '',
  }
}

function openAdd(parent?: MenuItem, defaultType: MenuType = 1) {
  isEdit.value = false
  isSystemMenu.value = false
  currentId.value = undefined
  const parentId = parent?.id ?? '0'
  let type: MenuType = defaultType
  if (parent?.type === 1)
    type = 2
  else if (parent?.type === 2)
    type = 3
  formData.value = createEmptyForm(type, parentId)
  if (type === 1)
    formData.value.component = 'Layout'
  visible.value = true
}

function openEdit(row: MenuItem) {
  isEdit.value = true
  isSystemMenu.value = !!row.isSystem
  currentId.value = row.id
  formData.value = toFormData(row)
  visible.value = true
}

async function handleBeforeOk() {
  try {
    await formRef.value?.formRef?.validate()
    const payload = { ...formData.value, parentId: Number(formData.value.parentId) || 0 }
    if (isEdit.value && currentId.value) {
      await updateMenuApi(currentId.value, payload)
      ElMessage.success('更新成功')
    }
    else {
      await createMenuApi(payload)
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
    :style="{ maxWidth: '640px' }"
    destroy-on-close
    :on-before-ok="handleBeforeOk"
  >
    <GiForm
      ref="formRef"
      v-model="formData"
      :columns="formColumns"
      :rules="formRules"
      label-width="96px"
    />
  </GiDialog>
</template>
