import GiComponent from 'gi-component'
import { createApp } from 'vue'
import pinia from '@/stores'
import App from './App.vue'
import directives from './directives'
import router from './router'
import 'gi-component/dist/gi.css'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import 'animate.css/animate.min.css'
import 'virtual:svg-icons-register'
import '@/plugins/echarts'
import '@/styles/index.scss'

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(GiComponent)
app.use(directives)

app.mount('#app')
