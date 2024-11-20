<template>
  <div class="topClass">
    <div class="loginTag">
      <v-img
      class="mx-auto my-6 imgLogo"
      max-width="228"
      :src="loginLogo"
    ></v-img>

    <v-card
      class="mx-auto pa-12 pb-8"
      elevation="8"
      max-width="448"
      rounded="lg"
    >
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>

      <v-text-field
        density="compact"
        placeholder="Email address"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
        v-model="email"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Password
        <RouterLink 
        :to="{name : 'retry'}"
          class="text-caption text-decoration-none text-blue"
          rel="noopener noreferrer"
          target="_blank">Forgot login password?</RouterLink>
      </div>

      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        v-model="password"
        @click:append-inner="visible = !visible"
      ></v-text-field>

      <v-card
        class="mb-12"
        color="surface-variant"
        variant="tonal"
      >
        <v-card-text class="text-medium-emphasis text-caption">
          ⚠️ : 5번 로그인을 실패하게 되면, 해킹으로 판단하여 <br>관리자가 당신의 계정을 비활성화시킬 수 있습니다.<br> 
          만약 로그인을 원하면 "Forgot login password?" 을 <br>클릭해주세요.
        </v-card-text>
      </v-card>

      <!--여기에 인증된 사용자가 아니면 로그인 하라는 alert 메세지, 로그인에 성공했다면 alert 성공 메세지 -->
      <v-btn
        class="mb-8"
        color="blue"
        size="large"
        variant="tonal"
        block
        @click.prevent="IsUserValid"
      >
        Log In
      </v-btn>

      <v-card-text class="text-center">
        <RouterLink 
        :to="{name : 'signup'}"
          class="text-blue text-decoration-none"
          rel="noopener noreferrer"
          target="_blank">Sign up now</RouterLink>
      </v-card-text>
    </v-card>
    
    </div>
  </div>
</template>

<script setup>
import loginLogo from '@/assets/images/loginLogo.png'
import { useBankStore } from '@/stores/bank'
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'


const store = useBankStore()
const router = useRouter()
//사용자에게 input 받을 로그인 관련 데이터
const email = ref(null)
const password = ref(null)

//서버에 사용자가 입력한 데이터를 전달해서 일치 여부 판단
const userLoginData = ref({
  'email' : email,
  'password' : password
})
//서버에 데이터를 보내주고 사용자가 맞다면? True 값이라면 router MainPage
const IsUserValid = async function(){
  const result = await store.findUser(userLoginData.value)
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
  .topClass {
    margin-top:30px;
  }
</style>