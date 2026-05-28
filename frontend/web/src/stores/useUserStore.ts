import type { UserInfo } from '@/apis/auth'
import { defineStore } from 'pinia'
import { getUserInfoApi, loginApi, logoutApi } from '@/apis/auth'
import { getRoutesApi } from '@/apis/menu'
import { usePermissionStore } from '@/core/stores/usePermissionStore'
import { useRouteStore } from '@/core/stores/useRouteStore'
import { useTabsStore } from '@/core/stores/useTabsStore'
import router from '@/router'
import { resetRoutesLoadedFlag } from '@/router/route-load-state'
import { constantRoutes } from '@/router/routes'

export const useUserStore = defineStore('user', () => {
  const routeStore = useRouteStore()
  const tabsStore = useTabsStore()
  const permissionStore = usePermissionStore()
  const token = ref('')
  const userInfo = ref<UserInfo | null>(null)

  const isLogin = computed(() => !!token.value)

  function applyPermissions(data: UserInfo) {
    permissionStore.setRoles(data.roles)
    permissionStore.setPermissions(data.permissions)
  }

  function resetRouteState() {
    routeStore.resetDynamicRoutes()
    routeStore.setRoutes({ constantRoutes, asyncData: [] })
    tabsStore.reset()
    resetRoutesLoadedFlag()
  }

  async function login(params: { username: string, password: string }) {
    resetRouteState()
    const res = await loginApi(params)
    token.value = res.token
    await fetchUserInfo()
    await generateRoutes()
    return res
  }

  async function fetchUserInfo() {
    const data = await getUserInfoApi()
    userInfo.value = data
    applyPermissions(data)
    return data
  }

  async function logout() {
    try {
      await logoutApi()
    }
    finally {
      token.value = ''
      userInfo.value = null
      permissionStore.setRoles([])
      permissionStore.setPermissions([])
      resetRouteState()
    }
  }

  async function generateRoutes() {
    const data = await getRoutesApi()
    routeStore.resetDynamicRoutes()
    routeStore.setRoutes({ constantRoutes, asyncData: data })
    return true
  }

  async function refreshRoutes() {
    routeStore.resetDynamicRoutes()
    await fetchUserInfo()
    const data = await getRoutesApi()
    routeStore.setRoutes({ constantRoutes, asyncData: data })
    const current = router.currentRoute.value
    if (current.name && !router.hasRoute(current.name as string)) {
      await router.replace(constantRoutes[0]?.path || '/')
    }
    return true
  }

  return {
    token,
    userInfo,
    isLogin,
    login,
    fetchUserInfo,
    logout,
    generateRoutes,
    refreshRoutes,
  }
}, {
  persist: {
    key: 'user',
    pick: ['token', 'userInfo'],
  },
})
