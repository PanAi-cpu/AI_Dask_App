// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'  // 新增
import App from './App.vue'
import router from './router'
import './assets/styles/global.css'

// 创建 Pinia 实例
const pinia = createPinia()

const app = createApp(App)

// 先使用 Pinia，再使用路由
app.use(pinia)
app.use(router)

app.mount('#app')