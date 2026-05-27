import type { UserInfo } from '@/apis/auth'
import { defineStore } from 'pinia'
import { getUserInfoApi, loginApi, logoutApi } from '@/apis/auth'
import { getRoutesApi } from '@/apis/menu'
import { useRouteStore } from '@/core/stores/useRouteStore'
import { constantRoutes } from '@/router/routes'

export const useUserStore = defineStore('user', () => {
  const routeStore = useRouteStore()
  const token = ref('')
  const userInfo = ref<UserInfo | null>(null)

  /** 是否已登录 */
  const isLogin = computed(() => !!token.value)

  /** 用户权限集合 */
  // const permissions = computed(() => userInfo.value?.permissions ?? [])

  /** 登录 */
  async function login(params: { username: string, password: string }) {
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

  async function generateRoutes() {
    try {
      const data = await getRoutesApi()
      routeStore.setRoutes({ constantRoutes, asyncData: data })
      return true
    }
    catch (error) {
      console.error('[permission] generateRoutes error:', error)
      throw error
    }
  }

  return {
    token,
    userInfo,
    isLogin,
    login,
    fetchUserInfo,
    logout,
    generateRoutes,
  }
}, {
  persist: {
    key: 'user',
    pick: ['token', 'userInfo'],
  },
})
