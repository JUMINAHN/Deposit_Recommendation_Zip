<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary justify-content-center">
    <div class="container-fluid">
      <img src="@/assets/images/logo.png" alt="Logo" width="40" height="34" class="d-inline-block align-text-top">
      <a class="navbar-brand" href="#">예적금 맛ZIP</a> 
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <RouterLink :to="{name : 'main'}" class="nav-link" >메인 페이지</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{name : 'recommend'}" class="nav-link" >예적금 추천</RouterLink>
          </li>
          <!-- <li class="nav-item">
            <RouterLink :to="{name : 'compared'}" class="nav-link" @click.prevent="handleProductCompare">예적금 상품비교</RouterLink>
          </li> -->
  
          <li class="nav-item">
            <RouterLink :to="{name: 'exchangerate'}" class="nav-link">환율 검색</RouterLink> 
          </li>
          <li class="nav-item">
            <RouterLink :to="{name: 'map'}" class="nav-link" >주변 은행 검색</RouterLink> 
          </li>
          <li class="nav-item">
            <RouterLink :to="{name: 'community'}" class="nav-link">게시판</RouterLink> 
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">내가 지폐가 될 상인가?</a> 
          </li>
          <li class="nav-item">
          <RouterLink 
            v-if="!isLoggedIn" 
            :to="{name : 'login'}" 
            class="nav-link">
            로그인
          </RouterLink>
          <a 
            v-else 
            href="#" 
            class="nav-link"
            @click.prevent="handleLogout">
            로그아웃  
          </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  
  </template>
  
  <script setup>
  import { RouterLink, useRouter } from 'vue-router'
  import { ref, computed, onMounted } from 'vue'
  import { useBankStore } from '@/stores/bank'
  
  const store = useBankStore()
  const router = useRouter()
  
  const isLoggedIn = computed(() => !!store.token)
  
  onMounted(() => {
    // 페이지 로드 시 로컬 스토리지에서 토큰을 확인하고 store에 설정
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      store.token = storedToken
    }
  })
  
  const handleLogout = async () => {
    const success = await store.logoutUser()
    if (success) {
      router.push({ name: 'login' })
    } else {
      alert('로그아웃 실패')
    }
  }
  
  const handleProductCompare = () => {
    if (!isLoggedIn.value) {
      alert('로그인이 필요한 서비스입니다.')
      router.push({ name: 'login' })
      return
    }
    // // 로그인 되어있으면 해당 페이지로 이동
    // router.push({ name: 'product-compare' })
  }
  
  </script>
  
  <style scoped>
    /*  */
    .navbar-nav {
    margin: 0 auto;
    }
  
  .navbar-collapse {
    justify-content: center !important; 
    /* center로 넣는데 먼저 => important로 우선적으로 걸기 */
  }
  </style>