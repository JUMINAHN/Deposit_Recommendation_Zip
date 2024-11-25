<template>
  <div class="teachable-machine">
    <h2 class="text-xl mb-4">Teachable Machine Image Model</h2>

    <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded">
      {{ error }}
    </div>

    <div class="mb-4">
      <input
        type="file"
        @change="handleImageUpload"
        accept="image/*"
        class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 
               file:rounded-full file:border-0 file:text-sm file:font-semibold 
               file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />
    </div>

    <div v-if="imageUrl" class="mb-4">
      <img
        ref="imagePreview"
        :src="imageUrl"
        alt="uploaded image"
        class="max-w-xs rounded shadow"
        @load="analyzeImage"
      />
    </div>

    <div v-if="predictions.length > 0" class="mt-4 p-4 bg-gray-50 rounded">
      <h3 class="font-bold mb-2">분석 결과:</h3>
      <div v-for="(prediction, index) in predictions" :key="index" class="mb-2">
        <div class="flex justify-between items-center">
          <span class="font-medium">{{ prediction.className }}:</span>
          <span>{{ (prediction.probability * 100).toFixed(2) }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded h-2">
          <div
            class="bg-blue-600 rounded h-2"
            :style="{ width: `${prediction.probability * 100}%` }"
          ></div>
        </div>
      </div>

      <div class="mt-4 space-x-2">
        <button
          @click="getFormattedResults('object')"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          객체로 내보내기
        </button>
        <button
          @click="getFormattedResults('array')"
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          배열로 내보내기
        </button>
      </div>

      <div v-if="formattedResult" class="mt-4">
        <h4 class="font-bold mb-2">포맷된 결과:</h4>
        <pre class="bg-gray-100 p-4 rounded overflow-x-auto">{{ formattedResult }}</pre>
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

const modelPath = ref("/models/my_model/");

async function loadTensorFlow() {
  if (window.tf) return;
  
  await loadScript(
    "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"
  );
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
  if (!window.tmImage) {
    error.value = "Teachable Machine 라이브러리가 아직 로드되지 않았습니다.";
    return;
  }

  try {
    // 기존 모델 정리
    if (model) {
      await model.dispose();
    }
    
    // TensorFlow 메모리 정리
    tf.engine().startScope();  // 스코프 시작
    window.tf.disposeVariables();

    const modelURL = `${modelPath.value}model.json`;
    const metadataURL = `${modelPath.value}metadata.json`;

    model = await window.tmImage.load(modelURL, metadataURL);
    console.log("모델 로드 성공");
    
    tf.engine().endScope();  // 스코프 종료
  } catch (err) {
    error.value = "모델을 불러오는 중 오류가 발생했습니다.";
    console.error("모델 로드 오류:", err);
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
  color: white;
  padding: 20px;
}
</style>