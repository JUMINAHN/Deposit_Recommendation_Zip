<template>
  <div class="logo">
    <img src="@/assets/images/logo.png" alt="matzipLogo">
    <h2 class="font-weight-black font-italic">예적금 맛ZIP</h2>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter()

// 3초후에 페이지 이동하기
  setTimeout(function () {
    router.push({name : 'main'}) //3초뒤에 메인페이지로 이동하기
  }, 3000);
</script>

<style scoped>
  .logo {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-content: center;
    align-items: center
  }

  h2 {
    background-color: rgba(0, 238, 255, 0.882);
    width : 15%;
    color: white;
  }

  img {
    text-align: center !important;
  }
</style>