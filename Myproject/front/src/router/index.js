import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import CommunityView from '@/views/CommunityView.vue'
import HomeView from '@/views/HomeView.vue'
import LoginRetryView from '@/views/LoginRetryView.vue'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import RecommendView from '@/views/RecommendView.vue'

import DepositCompareView from '@/views/DepositDetail.vue'
import BankMapView from '@/views/BankMapView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import ProfileView from '@/views/ProfileView.vue'
import UserProfile from '@/components/UserProfile.vue'
import SignUpView from '@/views/SignUpView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'



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
    {
      path : '/main/recommend/:bankName/:productName',
      name : 'compared',
      component : DepositCompareView
    },
    {
      path : '/main/profile',
      name : 'profile',
      component : ProfileView
    },
    {
      path: '/profile/:username', 
      name: 'userProfile',
      component: UserProfile // 직접 import한 컴포넌트 사용
    },
    {
      path : '/main/login',
      name : 'login',
      component : LoginView
    },
    {
      path : '/main/signup',
      name : 'signup',
      component : SignUpView
    },
    {
      path : '/main/login/retry',
      name : 'retry',
      component : LoginRetryView
    },
    {
      path : '/main/community',
      name : 'community',
      component : CommunityView
    },
    {
      path : '/main/community/:id',
      name : 'articleDetail',
      component : ArticleDetailView
    },
    {
      path: '/main/community/create',
      name: 'article-create',
      component: ArticleCreateView
    },
    {
      path : '/main/map',
      name : 'map',
      component : BankMapView
    },
    {
      path : '/main/exchangerate',
      name : 'exchangerate',
      component : ExchangeRateView
    },
  ],
})

export default router
