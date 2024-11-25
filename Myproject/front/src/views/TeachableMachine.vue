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
      <div v-for="(prediction, index) in predictions" 
           :key="index" 
           class="prediction-item">
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

      <!-- <div class="export-buttons">
        <v-btn
          @click="getFormattedResults('object')"
          color="primary"
          class="export-btn"
        >
          <v-icon left>mdi-file-document</v-icon>
          객체로 내보내기
        </v-btn>
        <v-btn
          @click="getFormattedResults('array')"
          color="success"
          class="export-btn"
        >
          <v-icon left>mdi-file-table</v-icon>
          배열로 내보내기
        </v-btn>
      </div> -->

      <div v-if="formattedResult" class="formatted-result">
        <h4 class="formatted-title">상세 분석 결과</h4>
        <pre class="result-code">{{ formattedResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const error = ref(null);
const imageUrl = ref(null);
const imagePreview = ref(null);
const predictions = ref([]);
const formattedResult = ref(null);
let model = null;


onMounted(async () => {
  try {
    // 1. TensorFlow.js 로드
    await loadTensorFlow();
    
    // 2. Teachable Machine 라이브러리 로드
    await loadTeachableMachine();
    
    // 3. 모델 초기화
    await initModel();
  } catch (error) {
    console.error('모델 초기화 실패:', error);
    error.value = '모델을 불러오는데 실패했습니다.';
  }
});

const modelPath = ref("/models/my_model/");

async function loadTensorFlow() {
  if (window.tf) {
    console.log('TensorFlow.js already loaded');
    return;
  }
  
  console.log('Loading TensorFlow.js...');
  await loadScript("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js");
  console.log('TensorFlow.js loaded successfully');
}

async function loadTeachableMachine() {
  if (window.tmImage) return;
  
  await loadScript(
    "https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"
  );
}

function getFormattedResults(format = "object") {
  if (!predictions.value.length) return null;

  const imageInfo = {
    url: imageUrl.value,
    timestamp: new Date().toISOString(),
  };

  if (format === "object") {
    const resultObject = {
      image: imageInfo,
      predictions: predictions.value.reduce((acc, pred) => {
        acc[pred.className] = {
          probability: pred.probability,
          percentage: (pred.probability * 100).toFixed(2) + "%",
        };
        return acc;
      }, {}),
      highestPrediction: {
        className: predictions.value[0].className,
        probability: predictions.value[0].probability,
        percentage: (predictions.value[0].probability * 100).toFixed(2) + "%",
      },
    };
    formattedResult.value = JSON.stringify(resultObject, null, 2);
    return resultObject;
  } else {
    const resultArray = predictions.value.map((pred) => ({
      className: pred.className,
      probability: pred.probability,
      percentage: (pred.probability * 100).toFixed(2) + "%",
    }));
    formattedResult.value = JSON.stringify(resultArray, null, 2);
    return resultArray;
  }
}

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    error.value = "파일 크기는 5MB 이하여야 합니다.";
    return;
  }

  if (!file.type.startsWith("image/")) {
    error.value = "이미지 파일만 업로드 가능합니다.";
    return;
  }

  error.value = null;
  imageUrl.value = URL.createObjectURL(file);
  formattedResult.value = null;
}

async function analyzeImage() {
  if (!model || !imagePreview.value) {
    error.value = "모델이 준비되지 않았습니다.";
    return;
  }

  try {
    const results = await model.predict(imagePreview.value);
    predictions.value = results.sort((a, b) => b.probability - a.probability);
    formattedResult.value = null;
  } catch (err) {
    error.value = "이미지 분석 중 오류가 발생했습니다.";
    console.error("분석 오류:", err);
  }
}

async function initModel() {
  try {
    if (!window.tmImage) {
      throw new Error('Teachable Machine 라이브러리가 로드되지 않았습니다.');
    }

    if (model) {
      await model.dispose();
    }
    
    console.log('모델 경로:', `${modelPath.value}model.json`);
    
    model = await window.tmImage.load(
      `${modelPath.value}model.json`,
      `${modelPath.value}metadata.json`
    );
    
    console.log('모델 로드 성공');
  } catch (err) {
    error.value = `모델 로드 실패: ${err.message}`;
    console.error('모델 로드 오류:', err);
  }
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

onUnmounted(() => {
  tf.engine().startScope();
  if (model) {
    model.dispose();
  }
  window.tf.disposeVariables();
  tf.engine().endScope();
})

onUnmounted(async () => {
  if (model) {
    await model.dispose();
  }
  if (window.tf) {
    window.tf.disposeVariables();
  }
});

defineExpose({
  getFormattedResults,
});
</script>

<style>
.teachable-machine {
  max-width: 800px;
  /* margin-top: 100px; */
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
  margin: 2rem 0;
  width: 100%;
  max-width: 300px; /* 컨테이너 크기도 제한 */
  margin: 2rem auto; /* 중앙 정렬 */
}

.preview-image {
  max-width: 300px;  /* 400px에서 300px로 축소 */
  max-height: 300px; /* 400px에서 300px로 축소 */
  width: 100%;       /* 컨테이너에 맞춰 반응형으로 조정 */
  object-fit: contain; /* 비율 유지 */
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

.export-buttons {
  display: flex;
  gap: 1rem;
  margin: 2rem 0;
}

.export-btn {
  flex: 1;
}

.formatted-result {
  margin-top: 2rem;
}

.formatted-title {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.result-code {
  background: #2c3e50;
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  font-family: monospace;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}
</style>