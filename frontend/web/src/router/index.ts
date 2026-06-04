import { createRouter, createWebHashHistory } from 'vue-router'
import { setupRouterGuard } from './guard'
import { constantRoutes } from './routes'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.VITE_BASE),
  routes: constantRoutes,
  scrollBehavior: () => ({ left: 0, top: 0 }),
})

setupRouterGuard(router)

export default router
