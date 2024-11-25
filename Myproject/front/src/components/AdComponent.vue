<!-- AdComponent.vue -->
<template>
  <div class="ad-container">
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-YOUR_PUBLISHER_ID"
         data-ad-slot="YOUR_AD_SLOT_ID"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // 광고 로드
  try {
    (window.adsbygoogle = window.adsbygoogle || []).push({})
  } catch (error) {
    console.error('광고 로드 실패:', error)
  }
})
</script>