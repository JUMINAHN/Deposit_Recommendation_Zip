<template>
  <div class="login-page-container">
    <!-- 왼쪽 브랜딩 섹션 -->
    <div class="brand-section">
      <!-- 로고 이미지 -->
      <v-img
        class="brand-logo"
        max-width="800"
        :src="loginLogo"
        contain
      ></v-img>
      <div class="overlay-content">
        <h2 class="text-h4 mb-4">예적금 맛ZIP과 함께</h2>
        <p class="text-h6">새로운 금융 생활을 시작하세요</p>
      </div>
    </div>

    <!-- 오른쪽 로그인 섹션 -->
    <div class="login-section">
      <v-card
        class="login-card"
        elevation="3"
        rounded="lg"
      >
        <div class="text-h5 mb-6">로그인하세요</div>
        
        <div class="text-subtitle-1 text-medium-emphasis mb-2">Username</div>
        <v-text-field
          density="comfortable"
          placeholder="Username"
          prepend-inner-icon="mdi-account"
          variant="outlined"
          v-model.trim="username"
          class="mb-4"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis mb-2">Email</div>
        <v-text-field
          density="comfortable"
          placeholder="Email address"
          prepend-inner-icon="mdi-email"
          variant="outlined"
          v-model.trim="email"
          class="mb-4"
        ></v-text-field>

        <div class="password-header">
          <span class="text-subtitle-1 text-medium-emphasis">Password</span>
          <RouterLink 
            :to="{name : 'retry'}"
            class="forgot-password"
          >비밀번호를 잊으셨나요?</RouterLink>
        </div>

        <v-text-field
          :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          :type="visible ? 'text' : 'password'"
          density="comfortable"
          placeholder="Enter your password"
          prepend-inner-icon="mdi-lock"
          variant="outlined"
          v-model.trim="password"
          @click:append-inner="visible = !visible"
          class="mb-4"
        ></v-text-field>

        <v-alert
          type="warning"
          variant="tonal"
          density="comfortable"
          class="mb-4"
        >
          5번 로그인 실패 시 계정이 비활성화될 수 있습니다.
        </v-alert>

        <v-btn
          block
          color="#90CAF9"
          size="large"
          class="login-btn mb-4"
          @click.prevent="IsUserValid"
        >
          로그인
        </v-btn>

        <div class="text-center">
          <span class="text-medium-emphasis">계정이 없으신가요? </span>
          <RouterLink 
            :to="{name : 'signup'}"
            class="signup-link"
          >회원가입</RouterLink>
        </div>
      </v-card>
    </div>
  </div>
</template>


<script setup>
import loginLogo from '@/assets/images/logo.png'
import { useBankStore } from '@/stores/bank'
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'


const store = useBankStore()
const router = useRouter()
//사용자에게 input 받을 로그인 관련 데이터
const email = ref(null)
const password = ref(null)
const username = ref(null)

//서버에 사용자가 입력한 데이터를 전달해서 일치 여부 판단
const userLoginData = {
  username,
  email,
  password
}
//서버에 데이터를 보내주고 사용자가 맞다면? True 값이라면 router MainPage
const IsUserValid = async function(){
  const result = await store.findUser(userLoginData)
  console.log('result : ', result)
  if (result === true) {//true이면 alert
    
    alert('로그인에 성공하였습니다!')
    router.push({name : 'main'})
  } else {
    alert('로그인에 실패하였습니다! 다시 확인해주세요!')
  }
}

//visible 로직 구현 => password 눈을 눌렀을 때
const visible = ref(true) //true -> false : 눈감기 data

//password를 까먹었을 때 => NewPage


</script>


<style scoped>
.login-page-container {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.brand-section {
  background: linear-gradient(135deg, #33c5f2 0%, #83dcee 100%); /* 더 옅은 파란색으로 변경 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
}


/* v-img 컴포넌트의 max-width 속성이 이를 제한/ */
.brand-logo {
  width: 800px;
  height: auto;
  margin-bottom: 1rem;
  z-index: 2;
  position: relative;
  display: block; /* 추가 */
  object-fit: contain; /* 추가 */
}

.overlay-content {
  text-align: center;
  color: white; /* 배경색 변경에 따른 텍스트 색상 조정 */
  z-index: 2;
  margin-top: -2rem; /* 간격 줄이기 */
}

.login-section {
  background: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.login-card {
  width: 100%;
  max-width: 440px;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
}


.password-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.forgot-password {
  color: var(--v-primary-base);
  text-decoration: none;
  font-size: 0.875rem;
}

.signup-link {
  color: var(--v-primary-base);
  text-decoration: none;
  font-weight: 500;
}

.image-section {
  background: linear-gradient(135deg, #909ead 0%, #6c99c6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
}

.overlay-content {
  color: white;
  text-align: center;
  z-index: 1;
}

.login-btn {
  height: 48px;
  font-weight: 500;
  text-transform: none;
  background-color: #4B9FFF !important;
  color: white !important; /* 로그인 버튼 텍스트 색상 흰색으로 변경 */
}

.login-btn:hover {
  background-color: #6B8CFF !important;
}

@media (max-width: 960px) {
  .login-page-container {
    grid-template-columns: 1fr;
  }

  .image-section {
    display: none;
  }

  .login-section {
    padding: 1rem;
  }
}
</style>