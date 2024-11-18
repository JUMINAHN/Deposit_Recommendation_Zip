import './assets/main.css'

//뷰티파이 설치
//npm install vuetify@next
// npm i -D vuetify vite-plugin-vuetify
//npm i @mdi/font

import { createApp } from 'vue'
import { createPinia } from 'pinia'

//bootstrap import 실행
//npm 터미널 설치 :  npm install bootstrap@5.3.0-alpha1

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

import App from '@/App.vue'
import router from '@/router'
import vuetify from '@/plugins/vuetify' 

const app = createApp(App)

app.use(createPinia())
app.use(vuetify)
app.use(router)

app.mount('#app')
