import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from "@/router.js"
import auth from '@/utils/auth.js'
import http from '@/utils/http.js'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.use(ElementPlus)
app.use(router);
app.config.globalProperties.$auth = auth
app.config.globalProperties.$http = http
app.mount('#app')

