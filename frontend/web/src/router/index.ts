import { createRouter, createWebHashHistory } from 'vue-router'
import { setupRouterGuard } from './guard'
import { CONSTANT_ROUTES } from './routes'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.VITE_BASE),
  routes: CONSTANT_ROUTES,
  scrollBehavior: () => ({ left: 0, top: 0 }),
})

setupRouterGuard(router)

export default router
