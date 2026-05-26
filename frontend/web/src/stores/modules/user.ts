import type { LoginParams, UserInfo } from '@/types/user'
import { defineStore } from 'pinia'
import { getUserInfoApi, loginApi, logoutApi } from '@/apis/auth'
import { StorageKey } from '@/enums'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const userInfo = ref<UserInfo | null>(null)

  /** 是否已登录 */
  const isLogin = computed(() => !!token.value)

  /** 用户权限集合 */
  const permissions = computed(() => userInfo.value?.permissions ?? [])

  /** 登录 */
  async function login(params: LoginParams) {
    const res = await loginApi(params)
    token.value = res.token
    userInfo.value = res.user
    return res
  }

  /** 获取用户信息 */
  async function fetchUserInfo() {
    const data = await getUserInfoApi()
    userInfo.value = data
    return data
  }

  /** 退出登录 */
  async function logout() {
    try {
      await logoutApi()
    }
    finally {
      token.value = ''
      userInfo.value = null
    }
  }

  /** 判断是否有权限 */
  function hasPermission(permission?: string | string[]): boolean {
    if (!permission)
      return true
    const perms = permissions.value
    if (Array.isArray(permission))
      return permission.some(p => perms.includes(p))
    return perms.includes(permission)
  }

  return {
    token,
    userInfo,
    isLogin,
    permissions,
    login,
    fetchUserInfo,
    logout,
    hasPermission,
  }
}, {
  persist: {
    key: StorageKey.USER,
    pick: ['token', 'userInfo'],
  },
})
