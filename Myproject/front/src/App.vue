<template>
  <NavVar />
  <RouterView /> <!--main에 있는 view화면 출력 -->
  <div>
    <ChatBot />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavVar from '@/components/NavVar.vue'
import HomeView from './views/HomeView.vue';
import ChatBot from '@/components/ChatBot.vue'


</script>


<style>

</style>
