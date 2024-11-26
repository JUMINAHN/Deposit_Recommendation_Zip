<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <img src="@/assets/images/logo.png" alt="Logo" class="logo">
        <RouterLink to="/" class="brand-name">예적금 맛ZIP</RouterLink>
      </div>

      <div class="navbar-menu">
        <RouterLink :to="{name: 'main'}" class="nav-link">메인 페이지</RouterLink>
        <RouterLink v-if="isLoggedIn" :to="{name: 'recommendations'}" class="nav-link">예적금 추천</RouterLink>
        <RouterLink :to="{name: 'recommend'}" class="nav-link">예적금 비교</RouterLink>
        <RouterLink v-if="isLoggedIn" :to="{name: 'community'}" class="nav-link">게시판</RouterLink>
        <RouterLink :to="{name: 'map'}" class="nav-link">주변 은행 검색</RouterLink>
        <RouterLink :to="{name: 'exchangerate'}" class="nav-link">환율 검색</RouterLink> 
        <RouterLink v-if="isLoggedIn" :to="{name: 'teachablemachine'}" class="nav-link">내가 지폐가 될 상인가?</RouterLink> <br>

      </div>
      
      <div class="navbar-auth">
        <RouterLink v-if="isLoggedIn" :to="{name: 'profile'}" class="auth-link">
          <i class="fas fa-user"></i> 마이페이지
        </RouterLink>
        <RouterLink v-if="!isLoggedIn" :to="{name: 'login'}" class="auth-link login-btn">
          로그인
        </RouterLink>
        <a v-else @click.prevent="handleLogout" href="#" class="auth-link logout-btn">
          로그아웃
        </a>

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
}
</script>


<style scoped>
.navbar {
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 0.8rem 0;
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 3rem; /* 2rem에서 3rem으로 증가 */
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.logo {
  width: 40px;
  height: 34px;
}

.brand-name {
  font-size: 1.3rem;
  font-weight: 600;
  color: #4a90e2;
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  gap: 2rem;
  align-items: center;
}

/* auth-link 버튼들의 패딩도 약간 조정 */
.auth-link {
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  color: #4a5568;
  transition: all 0.2s;
  padding: 0.5rem 0.8rem; /* 패딩 추가 */
}

.nav-link:hover {
  color: #4a90e2;
}

.navbar-auth {
  display: flex;
  gap: 2rem; /* 1.5rem에서 2rem으로 증가 */
  align-items: center;
  margin-left: auto; /* 오른쪽 정렬을 위해 추가 */
  padding-right: 1rem; /* 오른쪽 여백 추가 */
}

.auth-link {
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  color: #4a5568;
  transition: all 0.2s;
}

.login-btn {
  background-color: #4a90e2;
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
}

.login-btn:hover {
  background-color: #357abd;
}

.logout-btn {
  color: #e53e3e;
}

.logout-btn:hover {
  color: #c53030;
}

@media (max-width: 1024px) {
  .navbar-menu {
    gap: 1rem;
  }
  
  .nav-link {
    font-size: 0.9rem;
  }
}
</style>