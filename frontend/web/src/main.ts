import GiComponent, { Drawer } from 'gi-component'
import { createApp } from 'vue'
import directives from '@/core/directives'
import pinia from '@/stores'
import { removeAppLoading } from '@/utils/app-loading'
import App from './App.vue'
import router from './router'
import 'gi-component/dist/gi.css'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import '@/plugins/echarts'
import '@/plugins/iconify'
import '@/styles/index.scss'

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(GiComponent)
app.use(directives)

Object.assign(Drawer._context, app._context)

app.mount('#app')

router.isReady().finally(() => {
  removeAppLoading()
})
