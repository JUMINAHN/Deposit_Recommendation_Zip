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
      <v-text-field
        v-model.trim="name"
        color="primary"
        label="Name"
        variant="underlined"
      ></v-text-field>

      <v-text-field
        v-model.trim="nickname"
        color="primary"
        label="Nickname"
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
        @click.prevent="signUpDone">
        Complete Registration

        <v-icon icon="mdi-chevron-right" end></v-icon>
      </v-btn>
    </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
  const router = useRouter()
  //체크 박스 확인 완료
  const terms = ref(null)
  const signUpDone = async function() { //비동기 처리 == 요청
  
    if (terms.value === true) {
      alert('회원 가입 완료')
      //store에서 해당 내용을 기반으로 처리 => 진행해야 함
      router.push({name : 'login'}) //회원 가입 했으니 로그인 시도
      //메인 페이지 전달
    } else { //값이 하나라도 비어있으면
      alert('동의하지 않으면 회원가입 진행이 어렵습니다.')
    }

  }

</script>

<style scoped>
  .topClass {
    margin-top:40px;
  }
</style>