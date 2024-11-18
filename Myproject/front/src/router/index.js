import HomeView from '@/views/HomeView.vue'
import MainView from '@/views/MainView.vue'
import RecommendView from '@/views/RecommendView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path : '/',
      name : 'home',
      component : HomeView
    },
    {
      path : '/main/',
      name : 'main',
      component : MainView
    },
    {
      path : '/main/recommend/',
      name : 'recommend',
      component : RecommendView
    },
  ],
})

export default router
