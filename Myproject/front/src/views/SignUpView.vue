<template>
  <!-- 
    네비게이션 바가 fixed position으로 설정되어 있어 컨텐츠와 겹치는 문제 해결을 위해
    전체 컨테이너에 최소 높이를 설정하고 flex로 중앙 정렬
  -->
  <div class="signup-container">
    <v-card
      class="mx-auto pa-12 pb-8"
      elevation="8"
      max-width="448"
      rounded="lg"
      title="User Registration 🤗"
    >
      <v-container>
        <v-text-field
          v-model.trim="name"
          color="primary"
          label="Name"
          variant="underlined"
        ></v-text-field>

        <v-text-field
          v-model.trim="email"
          color="primary"
          label="Email"
          variant="underlined"
        ></v-text-field>

        <v-text-field
          v-model.trim="password1"
          color="primary"
          label="Password1"
          placeholder="Enter your password"
          variant="underlined"
          type="password"
        ></v-text-field>

        <v-text-field
          v-model.trim="password2"
          color="primary"
          label="Password2"
          placeholder="Enter your password"
          variant="underlined"
          type="password"
        ></v-text-field>

        <v-checkbox
          v-model="terms"
          color="blue"
          label="I agree to site terms and conditions"
          @click.prevent="showTermsDialog"
        ></v-checkbox>
      </v-container>

      <!-- 약관 동의 다이얼로그 -->
      <v-dialog v-model="dialog" max-width="500">
        <v-card>
          <v-card-title class="text-h5">
            이용약관 동의
          </v-card-title>
          <v-card-text>
            <div class="terms-content">
              <h3>서비스 이용약관</h3>
              <p>1. 본 약관은 당사가 제공하는 모든 서비스의 이용조건 및 절차, 이용자와 당사의 권리, 의무, 책임사항을 규정합니다.</p>
              <p>2. 당사는 이용자의 개인정보를 보호하기 위해 최선을 다하며, 관련 법령을 준수합니다.</p>
              <p>3. 이용자는 관련 법령과 본 약관의 규정을 준수하여야 합니다.</p>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="rejectTerms">거절</v-btn>
            <v-btn color="primary" @click="acceptTerms">동의</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn 
          color="blue"
          @click.prevent="checkLogin(userData)"
          :disabled="!terms"
        >
          Complete Registration
          <v-icon icon="mdi-chevron-right" end></v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import { useBankStore } from '@/stores/bank'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const store = useBankStore()
const router = useRouter()
const dialog = ref(false)
const terms = ref(false)
const name = ref(null)
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const showTermsDialog = () => {
  dialog.value = true
}

const acceptTerms = () => {
  terms.value = true
  dialog.value = false
}

const rejectTerms = () => {
  terms.value = false
  dialog.value = false
}

const userData = {
  'name': name,
  'email': email,
  'password1': password1,
  'password2': password2,
}

// 기존 checkLogin 함수 유지
const checkLogin = async function (userData) {
  // 입력값 검증
  if (!userData.name.value || !userData.email.value || !userData.password1.value || !userData.password2.value) {
    alert('모든 필드를 입력해주세요.')
    return
  }
  // 비밀번호 일치 확인
  if (userData.password1.value !== userData.password2.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  // 약관 동의 확인
  if (!terms.value) {
    alert('이용약관에 동의해주세요.')
    return
  }

  try {
    // bank.js의 signUpComplete 함수 형식에 맞게 데이터 전달
    const result = await store.signUpComplete({
      name: userData.name,
      email: userData.email,
      password1: userData.password1,
      password2: userData.password2
    })
    
    if (result) {
      alert('회원가입이 완료되었습니다.')
      router.push({ name: 'login' })
    } else {
      alert('회원가입 처리 중 오류가 발생했습니다.')
    }
  } catch (error) {
    console.error('회원가입 오류:', error)
    alert('회원가입 처리 중 오류가 발생했습니다.')
  }
}
</script>

<style scoped>
/* 
  문제 원인:
  1. margin-top만으로는 네비게이션 바의 높이를 고려하지 못함
  2. 컨텐츠가 화면 상단에 고정되어 있어 반응형 레이아웃에 적합하지 않음
  
  해결 방법:
  1. 컨테이너에 min-height: 100vh 설정으로 전체 화면 높이 확보
  2. padding-top으로 네비게이션 바 높이만큼 여백 확보
  3. flex 레이아웃으로 수직/수평 중앙 정렬
*/
.signup-container {
  min-height: 100vh;
  padding-top: 80px; /* 네비게이션 바 높이만큼 상단 패딩 */
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
}

.terms-content {
  max-height: 300px;
  overflow-y: auto;
  padding: 16px;
}

.terms-content h3 {
  margin-bottom: 16px;
  font-weight: bold;
}

.terms-content p {
  margin-bottom: 12px;
  line-height: 1.6;
}

/* 반응형 디자인을 위한 미디어 쿼리 추가 */
@media (max-width: 600px) {
  .signup-container {
    padding: 60px 16px; /* 모바일에서는 패딩 축소 */
  }
}
</style>