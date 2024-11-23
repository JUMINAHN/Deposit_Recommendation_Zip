<template>
  <div class="splash-container">
    <div class="logo-wrapper">
      <img 
        src="@/assets/images/logo.png" 
        alt="matzipLogo" 
        class="logo-image fade-in"
      >
      <h2 class="logo-text slide-up">예적금 맛ZIP</h2>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const router = useRouter()

onMounted(() => {
  setTimeout(() => {
    router.push({ name: 'main' })
  }, 3000)
})
</script>

<style scoped>
.splash-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
}

.logo-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3rem;  /* 2rem에서 3rem으로 증가하여 간격도 조정 */
}

.logo-image {
  width: 300px;  /* 200px에서 300px로 증가 */
  height: auto;
  opacity: 0;
  animation: fadeIn 1s ease-in forwards;
}


.logo-text {
  font-size: 3.5rem;  /* 2.5rem에서 3.5rem으로 증가 */
  font-weight: 800;
  font-style: italic;
  color: #4a90e2;
  background: linear-gradient(45deg, #4a90e2, #63b3ed);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  padding: 0.8rem 2.5rem;  /* 패딩도 약간 증가 */
  border-radius: 8px;
  opacity: 0;
  transform: translateY(20px);
  animation: slideUp 1s ease-out 0.5s forwards;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}


@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>