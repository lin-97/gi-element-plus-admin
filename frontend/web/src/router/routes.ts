import type { RouteRecordRaw } from 'vue-router'

/** 静态路由（无需权限） */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', hidden: true, showInTabs: false },
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: { title: '404', hidden: true, showInTabs: false },
  },
  {
    path: '/redirect/:path(.*)',
    name: 'Redirect',
    component: () => import('@/views/redirect/index.vue'),
    meta: { hidden: true, showInTabs: false },
  },
]
