import './assets/main.css'
// 뷰티파이 설치
// npm install vuetify@next
// npm i -D vuetify vite-plugin-vuetify
// npm i @mdi/font
// npm install axios

import { createApp } from 'vue'

// bootstrap import 실행
// npm i pinia-plugin-persistedstate 설치
// npm 터미널 설치: npm install bootstrap@5.3.0-alpha1
// alert
// npm install sweetalert2
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

import App from '@/App.vue'
import router from '@/router'
import vuetify from '@/plugins/vuetify'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(vuetify)
app.use(router)

app.mount('#app')