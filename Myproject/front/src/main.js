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
// npm install chart.js
// npm install echarts vue-echarts
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

// import App from '@/App.vue'
import router from '@/router'
import vuetify from '@/plugins/vuetify'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import ECharts from 'vue-echarts'
import { use } from "echarts/core"
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'


const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.component('v-chart', ECharts)
app.use(pinia)
app.use(vuetify)
app.use(router)
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

app.mount('#app')