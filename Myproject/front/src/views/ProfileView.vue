<template>
  <div class="profile-container">
    <!-- 왼쪽 섹션 -->
    <div class="left-section">
      <!-- 프로필 이미지 및 기본 정보 -->
      <div class="profile-card">
        <div class="profile-image">
          <img :src="bankchar" alt="프로필 이미지">
        </div>
        <div class="profile-info">
          <div class="info-row">
            <h2>{{ store.userInfo?.username }}</h2>
            <button class="edit-btn" @click="editField('username')">수정</button>
          </div>
          <p class="email">{{ store.userInfo?.email }}</p>
        </div>
      </div>
      
      <!-- 재무 정보 카드 -->
      <div class="financial-info">
        <div class="info-item">
          <span class="label">이메일</span>
          <div class="value-with-button">
            <span class="value">{{ store.userInfo?.email }}</span>
            <button class="edit-btn" @click="editField('email')">수정</button>
          </div>
        </div>
        <div class="info-item">
          <span class="label">닉네임</span>
          <div class="value-with-button">
            <span class="value">{{ store.userInfo?.nickname }}</span>
            <button class="edit-btn" @click="editField('nickname')">수정</button>
          </div>
        </div>
        <div class="info-item">
          <span class="label">나이</span>
          <div class="value-with-button">
            <span class="value">{{ store.userInfo?.age }}세</span>
            <button class="edit-btn" @click="editField('age')">수정</button>
          </div>
        </div>
        <div class="info-item">
          <span class="label">현재 자산</span>
          <div class="value-with-button">
            <span class="value">{{ store.userInfo?.asset }}원</span>
            <button class="edit-btn" @click="editField('asset')">수정</button>
          </div>
        </div>
        <div class="info-item">
          <span class="label">연봉</span>
          <div class="value-with-button">
            <span class="value">{{ store.userInfo?.income }}원</span>
            <button class="edit-btn" @click="editField('income')">수정</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 오른쪽 섹션 -->
    <div class="right-section">
      <h3>가입 상품 현황</h3>
      <div class="products-list">
        <div v-for="product in preferences" :key="product.bankname + product.products" class="product-card">
          <h4>{{ product.products }}</h4>
          <div class="product-info">
            <p>금리: {{ product.maxRate }}%</p>
            <p>최고 금리: {{ product.maxRate2 }}%</p>
          </div>
          <button @click="removePreference(product.bankname, product.products)">제거</button>
        </div>
      </div>
      <button class="compare-btn" @click="showGraph">
        상품 금리 비교
      </button>
    </div>

    <!-- 금리 비교 팝업 -->
    <div v-if="isGraphVisible" class="popup-overlay">
      <div class="popup-content">
        <button class="close-btn" @click="closeGraph">×</button>
        <h3>상품 금리 비교</h3>
        <div class="graph-container">
          <canvas id="interestChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import bankchar from '@/assets/images/bankchar.jpg'
import { computed, onMounted, ref } from 'vue'
import { Chart } from 'chart.js/auto'
import { useBankStore } from '@/stores/bank'
import { useRoute } from 'vue-router'

const store = useBankStore()
const userInfo = ref(null)
const route = useRoute();
const bankname = route.params.bankname
const productname = route.params.productname
const preferences = ref([])
const userName = computed(() => store.userInfo?.username || '')
const userEmail = computed(() => store.userInfo?.email || '')
const userNickName = computed(() => store.userInfo?.nickname || '')
const userAge = computed(() => store.userInfo?.age || '')
const userAsset = computed(() => store.userInfo?.asset || '')
const userIncome = computed(() => store.userInfo?.income || '')



onMounted(async () => {
  if (!store.userInfo) {
    await store.fetchUserInfo()
  }
  userInfo.value = store.userInfo
  loadPreferences()
})

const loadPreferences = async () => {
  await store.loadUserProduct()
  preferences.value = store.userProduct
}

const removePreference = async (bankName, productName) => {
  await store.removeFromPreference(bankName, productName)
  await loadPreferences()
}

const addToPreference = async (bankName, productName) => {
  await store.addToPreference(bankName, productName)
  await loadPreferences()
}


// onMounted(() => {
  //회원 정보 받아오기
  // const userInfo = store.getUserInfo() 
  // userInfo
  // .then((res) => {
  //   userName.value = res.username 
  //   userEmail.value = res.email
  // })
  // .catch((err) => {
  //   console.log('받아오는 과정에서 에러 발생', err)
  // })

  //회원이 가진 상품 받아오기 => bank.js에 선언했는데 현재 지금 이곳에서 사용
//})


// 팝업 상태 관리
const isGraphVisible = ref(false)
let chart: Chart | null = null

// 차트 생성 함수
const createChart = () => {
  const ctx = document.getElementById('interestChart') as HTMLCanvasElement
  if (ctx && preferences.value.length > 0) {
    if (chart) {
      chart.destroy()
    }
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: preferences.value.map(p => p.products),
        datasets: [
          {
            label: '기본금리 (%)',
            data: preferences.value.map(p => p.maxRate),
            backgroundColor: ['#90cdf4', '#63b3ed', '#4299e1'],
            borderColor: ['#63b3ed', '#4299e1', '#3182ce'],
            borderWidth: 1,
            order: 2
          },
          {
            label: '최고우대금리 (%)',
            data: preferences.value.map(p => p.maxRate2),
            backgroundColor: ['#fed7d7', '#feb2b2', '#fc8181'],
            borderColor: ['#feb2b2', '#fc8181', '#f56565'],
            borderWidth: 1,
            order: 1
          }
        ]
      },
      options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '금리 (%)',
            color: '#2d3748',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          ticks: {
            color: '#2d3748',
            font: {
              size: 12
            }
          }
        },
        x: {
          ticks: {
            color: '#2d3748',
            font: {
              size: 12,
              weight: 'bold'
            }
          }
        }
      },
      plugins: {
      legend: {
      display: true,
      position: 'top',
      labels: {
        padding: 20,
        color: '#2d3748',
        font: {
          size: 14,
          weight: 'bold'
        },
        // 범례 클릭 가능하도록 설정
        usePointStyle: true,
        pointStyle: 'circle',
      },
      // 클릭 이벤트 활성화
      onClick: function(e, legendItem, legend) {
        const index = legendItem.datasetIndex;
        const ci = legend.chart;
        const meta = ci.getDatasetMeta(index);

        // 데이터셋 표시/숨김 토글
        meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;

        // 차트 업데이트
        ci.update();
      }
    }
  },
  onClick: (event, elements) => {
    if (elements.length > 0) {
      const datasetIndex = elements[0].datasetIndex;
      chart.data.datasets[datasetIndex].hidden = 
        !chart.data.datasets[datasetIndex].hidden;
      chart.update();
    }
  },
        barPercentage: 0.8,
        categoryPercentage: 0.9
      }
    })
  }
}

// 메서드
const editField = (field: string) => {
  console.log(`Editing ${field}`)
}

const showGraph = () => {
  isGraphVisible.value = true
  setTimeout(createChart, 100)
}

const closeGraph = () => {
  isGraphVisible.value = false
  if (chart) {
    chart.destroy()
    chart = null
  }
}
</script>

<style scoped>
.profile-container {
  display: flex;
  max-width: 1200px;
  margin: 2rem auto;
  margin-top: 80px;
  padding: 2rem;
  gap: 2rem;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}

.left-section {
  flex: 1;
  padding: 2rem;
}

.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: #f8fbff;
  border-radius: 12px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #e6f0ff;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  text-align: center;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.financial-info {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f0f7ff;
  border-radius: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.8rem 0;
  border-bottom: 1px solid #e6f0ff;
}

.value-with-button {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.edit-btn {
  padding: 0.3rem 0.8rem;
  background-color: #e6f0ff;
  color: #4a5568;
  border: none;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background-color: #d3e4ff;
}

.right-section {
  flex: 1.2;
  padding: 2rem;
  background-color: #f8fbff;
  border-radius: 12px;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.product-card {
  background-color: #ffffff;
  padding: 1.2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.product-card h4 {
  color: #2d3748;
  font-size: 1.1rem;
  margin-bottom: 0.8rem;
}

.product-info p {
  color: #4a5568;
  font-size: 0.95rem;
  margin: 0.4rem 0;
}

.compare-btn {
  width: 100%;
  padding: 1rem;
  background-color: #e6f0ff;
  color: #4a5568;
  border: none;
  border-radius: 8px;
  margin-top: 20px;
  cursor: pointer;
  display: block;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.compare-btn:hover {
  background-color: #d3e4ff;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background-color: var(--white);
  padding: 2rem;
  border-radius: 12px;
  position: relative;
  width: 80%;
  max-width: 800px;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.graph-container {
  width: 100%;
  height: 400px;
  padding: 20px;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

:root {
  --primary-blue: #4a90e2;
  --light-blue: #e6f0ff;
  --pastel-blue: #f0f7ff;
  --white: #ffffff;
}
</style>