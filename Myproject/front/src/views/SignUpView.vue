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
        v-model.trim="password"
        color="primary"
        label="Password"
        placeholder="Enter your password"
        variant="underlined"
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
        @click.prevent="store.signUpComplete(userData)">
        Complete Registration

        <v-icon icon="mdi-chevron-right" end></v-icon>
      </v-btn>
    </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import { useBankStore } from '@/stores/bank'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

  const store = useBankStore()
  const router = useRouter()
  //체크 박스 확인 완료
  const terms = ref(null)
  const nickname = ref(null)
  const name = ref(null)
  const email = ref(null)
  const password = ref(null)
  //상기 값 userdata로 생성
  const userData = { //이중으로 반응형 데이터를 넣을 필요가 없음
    // 'nickname' : nickname,
    'name' : name,
    'email' : email,
    'password' : password
  }

  // //더미 데이터이기 때문에 async -> await 사용하지 않음 : 추후 추가 예정
  // const signUpDone = function() { //비동기 처리 == 요청
  //   //회원가입 .. store에서 받아와서 ture로 받아오면 login 페이지로 이동하게   
  //   const complete = store.signUpComplete(userData) 
  //   if (terms.value === true && complete === true) { //true만이 아니라 회원가입 데이터도 받아와야함
  //     alert('회원 가입 완료')
  //     //store에서 해당 내용을 기반으로 처리 => 진행해야 함
  //     router.push({name : 'login'}) //회원 가입 했으니 로그인 시도
  //     //메인 페이지 전달
  //   } else { //값이 하나라도 비어있으면
  //     //해당 값에 에러는 없음
  //     console.log(userData.email.value, '이메일') //해당 값이 맞는지? => 현재 userData가 어떤 값으로 오는건지?
  //     console.log(terms.value)
  //     console.log(complete, '현재 complete확인')
  //     alert('데이터를 채우지 않거나, 약관에 동의하지 않으면 회원가입 진행이 어렵습니다.')
  //   }
  // }



</script>

<style scoped>
  .topClass {
    margin-top:40px;
  }
</style>