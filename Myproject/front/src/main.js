import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

//bootstrap import 실행
//npm 터미널 설치 :  npm install bootstrap@5.3.0-alpha1

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
