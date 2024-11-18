<template>
  <NavVar />
  <RouterView /> <!--main에 있는 view화면 출력 -->
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavVar from '@/components/NavVar.vue'
import HomeView from './views/HomeView.vue';



</script>


<style>

</style>
