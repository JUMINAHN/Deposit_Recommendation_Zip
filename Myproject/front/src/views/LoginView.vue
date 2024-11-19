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
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Password

        <a
          class="text-caption text-decoration-none text-blue"
          href="#"
          rel="noopener noreferrer"
          target="_blank"
        >
          Forgot login password?</a>
      </div>

      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
      ></v-text-field>

      <v-card
        class="mb-12"
        color="surface-variant"
        variant="tonal"
      >
        <v-card-text class="text-medium-emphasis text-caption">
          경고: 5번 로그인을 시도하게 되면, 당신의 계정은 3시간 동안 잠깁니다. 
          만약 로그인을 원하면 "Forgot login password?" 을 클릭하고 패스워드를 변경해주세요.
        </v-card-text>
      </v-card>

      <v-btn
        class="mb-8"
        color="blue"
        size="large"
        variant="tonal"
        block
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
import { RouterLink } from 'vue-router'

</script>


<style scoped>
  .topClass {
    margin-top:30px;
  }
</style>