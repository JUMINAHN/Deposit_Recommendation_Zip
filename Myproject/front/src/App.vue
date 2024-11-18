
<template>
  <NavVar />
  <HomeView 
  class="bodyHome"/>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavVar from '@/components/NavVar.vue'
import HomeView from '@/views/HomeView.vue'

</script>


<style>
  .bodyHome {
    margin: auto;
  }
</style>
