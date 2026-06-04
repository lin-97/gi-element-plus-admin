import type { RouteRecordRaw } from 'vue-router'

const Layout = () => import('@/layouts/AppLayout.vue')

/** 静态路由（无需权限） */
export const CONSTANT_ROUTES: RouteRecordRaw[] = [
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
  {
    path: '/',
    component: Layout,
    meta: { title: '', hidden: false, icon: 'icon-park-outline:workbench' },
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '工作台', affix: true, hidden: false, icon: 'Monitor' },
      },
    ],
  },
  {
    path: '/icon',
    name: 'Icon',
    component: Layout,
    meta: { title: '', hidden: false, icon: 'icon-park-outline:instagram', sort: 99 },
    redirect: '/icon',
    children: [
      {
        path: '/icon/index',
        name: 'IconIndex',
        component: () => import('@/views/icon/index.vue'),
        meta: { title: '图标列表', hidden: false, icon: 'icon-park-outline:instagram' },
      },
    ],
  },
  {
    path: '/about',
    name: 'About',
    component: Layout,
    meta: { title: '', hidden: false, icon: 'icon-park-outline:info', sort: 100 },
    redirect: '/about',
    children: [
      {
        path: '/about/index',
        name: 'AboutIndex',
        component: () => import('@/views/about/index.vue'),
        meta: { title: '关于项目', hidden: false, icon: 'icon-park-outline:info' },
      },
    ],
  },
]
