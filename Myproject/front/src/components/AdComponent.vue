<template>
  <div class="ad-overlay">
    <div class="ad-popup">
      <div class="ad-content">
        <h3>광고</h3>
        <div class="ad-image-placeholder"></div>
        <div class="timer">{{ remainingTime }}초 후에 닫힙니다</div>
        <button 
          :disabled="remainingTime > 0" 
          @click="completeAd"
          class="close-button"
        >
          {{ remainingTime > 0 ? `${remainingTime}초 대기` : '광고 닫기' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['ad-completed'])
const remainingTime = ref(5)

const completeAd = () => {
  emit('ad-completed')
}

onMounted(() => {
  const timer = setInterval(() => {
    remainingTime.value--
    if (remainingTime.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
})
</script>

<style scoped>
.ad-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.ad-popup {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

.ad-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ad-image-placeholder {
  width: 100%;
  height: 200px;
  background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
  border-radius: 8px;
}

.close-button {
  background: #1976D2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>