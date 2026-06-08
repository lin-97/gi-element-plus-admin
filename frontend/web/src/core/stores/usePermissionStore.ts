import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * Permission Store 的核心设置逻辑
 */
function storeSetup() {
  const roles = ref<string[]>([]) // 角色
  const permissions = ref<string[]>([]) // 权限

  const setRoles = (value: string[]) => {
    roles.value = value
  }

  const setPermissions = (value: string[]) => {
    permissions.value = value
  }

  return {
    roles,
    permissions,
    setRoles,
    setPermissions,
  }
}

// 创建并导出 Permission Store，启用持久化存储
export const usePermissionStore = defineStore('permission', storeSetup, { persist: true })
