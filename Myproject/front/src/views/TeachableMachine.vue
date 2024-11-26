<template>
  <div class="teachable-machine">
    <h2 class="title">나와 닮은 지폐 찾기</h2>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div class="upload-container">
      <label for="file-upload" class="upload-button">
        <v-icon>mdi-cloud-upload</v-icon>
        사진 업로드하기
      </label>
      <input
        id="file-upload"
        type="file"
        @change="handleImageUpload"
        accept="image/*"
        class="hidden-input"
      />
      <p class="upload-hint">5MB 이하의 이미지 파일을 선택해주세요</p>
    </div>

    <div v-if="imageUrl" class="image-preview-container">
      <img
        ref="imagePreview"
        :src="imageUrl"
        alt="uploaded image"
        class="preview-image"
        @load="analyzeImage"
      />
    </div>

    <div v-if="predictions.length > 0" class="results-container">
      <h3 class="results-title">분석 결과</h3>
      <div v-for="(prediction, index) in predictions" :key="index" class="prediction-item">
        <div class="prediction-header">
          <span class="prediction-name">{{ prediction.className }}</span>
          <span class="prediction-value">{{ (prediction.probability * 100).toFixed(2) }}%</span>
        </div>
        
        <div class="progress-bar-bg">
          <div
            class="progress-bar-fill"
            :style="{ width: `${prediction.probability * 100}%` }"
          ></div>
        </div>
      </div>

      <div v-if="formattedResult" class="formatted-result">
        <h4 class="formatted-title">상세 분석 결과</h4>
        <pre class="result-code">{{ formattedResult }}</pre>
      </div>
    </div>
    
    <!-- 광고 표시 섹션 -->
    <div v-if="!canUploadImage" class="ad-section">
      <p>새로운 시도를 위해 광고를 시청해주세요</p>
      <AdComponent @ad-completed="watchAd" />
    </div>
  </div>
</template>

<script setup>
import AdComponent from '@/components/AdComponent.vue'  // components 폴더에 있는 경우
import { ref, onMounted, onUnmounted } from 'vue'

const error = ref(null)
const imageUrl = ref(null)
const imagePreview = ref(null)
const predictions = ref([])
const formattedResult = ref(null)
const canUploadImage = ref(true)
let model = null

const modelPath = ref("/models/my_model/")


const showAdComponent = ref(false)

function showAd() {
  showAdComponent.value = true
}

async function loadTensorFlow() {
  if (window.tf) {
    console.log('TensorFlow.js already loaded')
    return
  }
  console.log('Loading TensorFlow.js...')
  await loadScript("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js")
  console.log('TensorFlow.js loaded successfully')
}

async function loadTeachableMachine() {
  if (window.tmImage) return
  await loadScript(
    "https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"
  )
}

async function handleImageUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    error.value = "파일 크기는 5MB 이하여야 합니다."
    return
  }

  if (!file.type.startsWith("image/")) {
    error.value = "이미지 파일만 업로드 가능합니다."
    return
  }

  error.value = null
  imageUrl.value = URL.createObjectURL(file)
  formattedResult.value = null
}

async function analyzeImage() {
  if (!model || !imagePreview.value) {
    error.value = "모델이 준비되지 않았습니다."
    return
  }

  try {
    const results = await model.predict(imagePreview.value)
    predictions.value = results.sort((a, b) => b.probability - a.probability)
    formattedResult.value = null
    canUploadImage.value = false  // 분석 완료 후 광고 시청 필요
  } catch (err) {
    error.value = "이미지 분석 중 오류가 발생했습니다."
    console.error("분석 오류:", err)
  }
}

async function initModel() {
  try {
    if (!window.tmImage) {
      throw new Error('Teachable Machine 라이브러리가 로드되지 않았습니다.')
    }

    if (model) {
      await model.dispose()
    }
    
    console.log('모델 경로:', `${modelPath.value}model.json`)
    model = await window.tmImage.load(
      `${modelPath.value}model.json`,
      `${modelPath.value}metadata.json`
    )
    console.log('모델 로드 성공')
  } catch (err) {
    error.value = `모델 로드 실패: ${err.message}`
    console.error('모델 로드 오류:', err)
  }
}

async function watchAd() {
  try {
    // axios 요청 대신 직접 상태 변경
    canUploadImage.value = true
    console.log('광고 시청 완료')
  } catch (error) {
    console.error('광고 처리 실패:', error)
  }
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script")
    script.src = src
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

onMounted(async () => {
  try {
    await loadTensorFlow()
    await loadTeachableMachine()
    await initModel()
  } catch (error) {
    console.error('모델 초기화 실패:', error)
    error.value = '모델을 불러오는데 실패했습니다.'
  }
})

onUnmounted(async () => {
  if (model) {
    await model.dispose()
  }
  if (window.tf) {
    window.tf.disposeVariables()
  }
})
</script>

<style scoped>
.teachable-machine {
  max-width: 800px;
  margin: 150px auto;
  padding: 30px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.title {
  font-size: 2rem;
  color: #1976D2;
  text-align: center;
  margin-bottom: 2rem;
}

.upload-container {
  text-align: center;
  padding: 2rem;
  border: 2px dashed #e0e0e0;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.upload-button {
  display: inline-block;
  padding: 12px 24px;
  background: #1976D2;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-button:hover {
  background: #1565C0;
  transform: translateY(-2px);
}

.hidden-input {
  display: none;
}

.upload-hint {
  color: #666;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.image-preview-container {
  text-align: center;
  margin: 2rem auto;
  width: 100%;
  max-width: 300px;
}

.preview-image {
  max-width: 300px;
  max-height: 300px;
  width: 100%;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.results-container {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
}

.results-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.prediction-item {
  margin-bottom: 1.5rem;
}


.prediction-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.prediction-name {
  font-weight: 600;
  color: #2c3e50;
}

.prediction-value {
  color: #1976D2;
  font-weight: 600;
}

.progress-bar-bg {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #1976D2, #64B5F6);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}
.next-attempt-section {
  margin-top: 2rem;
  text-align: center;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.next-attempt-text {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.watch-ad-button {
  background: #1976D2;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.watch-ad-button:hover {
  background: #1565C0;
  transform: translateY(-2px);
}

</style>