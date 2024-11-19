<template>
  <div class="topClass">
    <v-card
    class="py-12 px-8 text-center mx-auto ma-4"
    max-width="420"
    width="100%"
  >
    <h3 class="text-h6 mb-2">
      Please enter the one time password to verify your account
    </h3>

    <div>The code is 240132</div>

    <v-otp-input
      v-model="otp"
      :disabled="validating"
      color="blue"
      variant="plain"
    ></v-otp-input>

    <v-btn
      :loading="validating"
      class="mt-6 text-none bg-surface-variant"
      height="40"
      text="Validate"
      variant="plain"
      width="135"
      border
      rounded
      @click.prevent="checkNumber"
      ></v-btn>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
  const router = useRouter()
  //숫자불일치시 alert : 재입력
  const otp = ref(null)
  const checkNumber = function() {
    if (otp.value === '240132') { //맞추면 임시로 mainpage 이동
      alert('인증되었습니다.')
      router.push({name : 'main'})
    } else {
      alert('인증에 실패했습니다.')
    }
  }


</script>

<style scoped>
  .topClass {
    margin-top:150px;
  }
</style>