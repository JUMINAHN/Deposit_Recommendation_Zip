<template>
  <div class="topClass">
    <v-card
    class="mx-auto pa-12 pb-8"
    elevation="8"
    max-width="448"
    rounded="lg"
    title="User Registration 🤗"
  >
    <v-container>
      <!-- <v-text-field
        v-model.trim="nickname"
        color="primary"
        label="Nickname"
        variant="underlined"
      ></v-text-field> -->

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
        @click="terms = !terms"
      ></v-checkbox>
    </v-container>

    <v-divider></v-divider>

    <v-card-actions>
      <v-spacer></v-spacer>

      <!--router 회원 가입 완료-->
      <v-btn color="blue"
        @click.prevent="checkLogin(userData)">
        Complete Registration

        <v-icon icon="mdi-chevron-right" end></v-icon>
      </v-btn>
      <!-- @click.prevent="store.signUpComplete(userData)"> -->
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
  //체크 박스 확인 완료
  const terms = ref(null)
  const name = ref(null)
  const email = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)
  //상기 값 userdata로 생성


  const userData = { //이중으로 반응형 데이터를 넣을 필요가 없음
    // 'nickname' : nickname,
    'name' : name,
    'email' : email,
    'password1' : password1,
    'password2' : password2,
  }

  //여기서 8글자 아니면 오류
  const checkLength = computed(() => {
    return password1.value.length > 8 ? true : false
  })
  if (checkLength === false) {
    alert('내용 다시 확인하세요')
  }

  //value로 접근 확인? 
  const checkLogin = function (userData) {
  // 이메일 도메인 검증
  const allowedDomains = ['@naver.com', '@google.com', '@kakao.com', '@nate.com', '@daum.net']
  const isValidEmailDomain = allowedDomains.some(domain => userData.email.value.endsWith(domain))

  // 비밀번호 길이 검증
  const isPasswordLongEnough = computed(() => userData.password1.value.length >= 8)

  // 비밀번호 일치 여부 검증
  const doPasswordsMatch = computed(() => userData.password1.value === userData.password2.value)

  // 비밀번호와 사용자 이름 유사성 검증
  const isPasswordTooSimilarToUsername = computed(() => {
    const username = userData.email.value.split('@')[0] // 이메일에서 사용자 이름 부분 추출
    return userData.password1.value.toLowerCase().includes(username.toLowerCase())
  })

  // 각 조건 검증
  if (!isValidEmailDomain) {
    alert('알맞은 이메일 도메인 형식이 아닙니다.')
    return
  }

  if (!isPasswordLongEnough.value) {
    alert('비밀번호는 8글자 이상이어야 합니다.')
    return
  }

  if (!doPasswordsMatch.value) {
    alert('비밀번호1, 비밀번호2가 일치하지 않습니다.')
    return
  }

  if (isPasswordTooSimilarToUsername.value) {
    alert('비밀번호가 사용자 이름과 너무 유사합니다.')
    return
  }

  // 모든 조건을 통과한 경우
  store.signUpComplete(userData)
}



</script>

<style scoped>
  .topClass {
    margin-top:40px;
  }
</style>