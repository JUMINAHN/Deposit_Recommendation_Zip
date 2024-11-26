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
          <div>
            <h2>{{ store.userInfo?.username }}</h2>
          </div>
          <div>
            <p class="email">{{ store.userInfo?.email }}</p>
          </div>
        </div>
      </div>
      
<!-- 이메일 -->
<div class="info-item">
  <span class="label">이메일</span>
  <div class="value-with-button">
    <template v-if="editingField === 'email'">
      <input 
        v-model="editValue"
        class="edit-input"
        :placeholder="store.userInfo?.email || '이메일을 입력하세요'"
        type="email"
      >
      <button class="save-btn" @click="saveEdit('email')">저장</button>
      <button class="cancel-btn" @click="cancelEdit">취소</button>
    </template>
    <template v-else>
      <span class="value">{{ store.userInfo?.email }}</span>
      <button class="edit-btn" @click="startEdit('email')">수정</button>
    </template>
  </div>
</div>

<!-- 닉네임 -->
<div class="info-item">
  <span class="label">닉네임</span>
  <div class="value-with-button">
    <template v-if="editingField === 'nickname'">
      <input 
        v-model="editValue"
        class="edit-input"
        :placeholder="store.userInfo?.nickname || '닉네임을 입력하세요'"
      >
      <button class="save-btn" @click="saveEdit('nickname')">저장</button>
      <button class="cancel-btn" @click="cancelEdit">취소</button>
    </template>
    <template v-else>
      <span class="value">{{ store.userInfo?.nickname }}</span>
      <button class="edit-btn" @click="startEdit('nickname')">수정</button>
    </template>
  </div>
</div>

<!-- 나이 -->
<div class="info-item">
  <span class="label">나이</span>
  <div class="value-with-button">
    <template v-if="editingField === 'age'">
      <input 
        v-model="editValue"
        class="edit-input"
        type="number"
        :placeholder="store.userInfo?.age || '나이를 입력하세요'"
      >
      <button class="save-btn" @click="saveEdit('age')">저장</button>
      <button class="cancel-btn" @click="cancelEdit">취소</button>
    </template>
    <template v-else>
      <span class="value">{{ store.userInfo?.age }}세</span>
      <button class="edit-btn" @click="startEdit('age')">수정</button>
    </template>
  </div>
</div>

<!-- 자산 -->
<div class="info-item">
  <span class="label">현재 자산</span>
  <div class="value-with-button">
    <template v-if="editingField === 'asset'">
      <input 
        v-model="editValue"
        class="edit-input"
        type="number"
        :placeholder="store.userInfo?.asset || '자산을 입력하세요'"
      >
      <button class="save-btn" @click="saveEdit('asset')">저장</button>
      <button class="cancel-btn" @click="cancelEdit">취소</button>
    </template>
    <template v-else>
      <span class="value">{{ formattedAsset }}원</span>
      <button class="edit-btn" @click="startEdit('asset')">수정</button>
    </template>
  </div>
</div>

<!-- 연봉 -->
<div class="info-item">
  <span class="label">연봉</span>
  <div class="value-with-button">
    <template v-if="editingField === 'income'">
      <input 
        v-model="editValue"
        class="edit-input"
        type="number"
        :placeholder="store.userInfo?.income || '연봉을 입력하세요'"
      >
      <button class="save-btn" @click="saveEdit('income')">저장</button>
      <button class="cancel-btn" @click="cancelEdit">취소</button>
    </template>
    <template v-else>
      <span class="value">{{ formattedIncome }}원</span>
      <button class="edit-btn" @click="startEdit('income')">수정</button>
    </template>
  </div>
</div>
<!-- 회원탈퇴 버튼 -->
<div class="info-item">
  <button class="delete-btn" @click="userDelete">회원탈퇴</button>
</div>
</div>

    <!-- 오른쪽 섹션 -->
    <div class="right-section">
      <h3>가입 상품 현황</h3>
      <div v-if="isLoading">로딩 중...</div>
      <div v-else-if="error">에러 발생: {{ error }}</div>
      <div v-else>
      <div class="products-list">
        <div v-for="product in preferences" :key="product.bankname + product.products" class="product-card">
          <h4>{{ product.bankname }} - {{ product.products }}</h4>
          <div class="product-info">
            <p>금리: {{ product.maxRate }}%</p>
            <p>최고 금리: {{ product.maxRate2 }}%</p>
          </div>
          <button class="remove-btn" @click="removePreference(product.bankname, product.products)">제거</button>
        </div>
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
import { useRoute, useRouter } from 'vue-router'

import axios from 'axios'

const store = useBankStore()
const userInfo = ref(null)
const route = useRoute()
const router = useRouter()
const bankname = route.params.bankname
const productname = route.params.productname
const preferences = ref([])
const userName = computed(() => store.userInfo?.username || '')
const userEmail = computed(() => store.userInfo?.email || '')
const userNickName = computed(() => store.userInfo?.nickname || '')
const userAge = computed(() => store.userInfo?.age || '')
const userAsset = computed(() => store.userInfo?.asset || '')
const userIncome = computed(() => store.userInfo?.income || '')
const isLoading = ref(true)
const error = ref(null)

// ===================== 숫자 포멧팅
const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}
const formattedAsset = computed(() => formatNumber(store.userInfo?.asset || 0))
const formattedIncome = computed(() => formatNumber(store.userInfo?.income || 0))
// ==================================

// ====================== 회원탈퇴 기능 ===============
const userDelete = async () => {
  if (confirm('정말로 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
    try {
      await axios.delete('http://127.0.0.1:8000/app/accounts/delete/', {
        headers: {
          Authorization: `Token ${store.token}`
        },
      })
      alert('회원 탈퇴가 완료되었습니다.')
      store.clearUserInfo() // 사용자 정보 및 토큰 삭제
      router.push({ name: 'main'} ) 
    } catch (error) {
      console.error('회원 탈퇴 중 오류 발생:', error)
      alert('회원 탈퇴 중 오류가 발생했습니다. 다시 시도해 주세요.')
    }
  }
}

onMounted(async () => {
  try {
    isLoading.value = true
    if (!store.userInfo) {
      await store.fetchUserInfo()
    }
    userInfo.value = store.userInfo
    await store.getOptionDeposit() // 상세 정보 먼저 로드
    await loadPreferences()
  } catch (error) {
    console.error('데이터 로딩 중 오류 발생:', error)
    error.value = error.message
  } finally {
    isLoading.value = false
  }
})

const loadPreferences = async () => {
  try {
    isLoading.value = true
    await store.getOptionDeposit() // 먼저 상세 정보 로드
    const prefs = await store.getPreferences()
    preferences.value = prefs.map(pref => ({
      ...pref,
      maxRate: parseFloat(pref.maxRate || 0).toFixed(2),
      maxRate2: parseFloat(pref.maxRate2 || 0).toFixed(2)
    }))
  } catch (err) {
    console.error('선호도 목록 로딩 실패:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

const removePreference = async (bankName, productName) => {
  await store.removeFromPreference(bankName, productName)
  await loadPreferences()
}

const addToPreference = async (bankName, productName) => {
  await store.addToPreference(bankName, productName)
  await loadPreferences()
}

const editingField = ref(null)
const editValue = ref('')

const startEdit = (field) => {
  editingField.value = field
  editValue.value = store.userInfo[field]
}

const cancelEdit = () => {
  editingField.value = null
  editValue.value = ''
}

const saveEdit = async (field) => {
  try {
    await store.updateUserProfile(field, editValue.value)
    editingField.value = null
    editValue.value = ''
  } catch (error) {
    alert('프로필 수정에 실패했습니다.')
  }
}

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
        const index = legendItem.datasetIndex
        const ci = legend.chart
        const meta = ci.getDatasetMeta(index)

        // 데이터셋 표시/숨김 토글
        meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null

        // 차트 업데이트
        ci.update()
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
.delete-btn {
  padding: 0.5rem 1rem;
  background-color: #e53e3e;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem;
}

.delete-btn:hover {
  background-color: #c53030;
}

.remove-btn {
  padding: 0.3rem 0.6rem; /* 버튼 크기 줄이기 */
  background-color: #ffcccc; /* 옅은 빨강 배경색 */
  color: #d32f2f; /* 어두운 빨강 텍스트 */
  border: 1px solid #ff9999; /* 옅은 빨강 테두리 */
  border-radius: 4px;
  font-size: 0.8rem; /* 글자 크기 줄이기 */
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

.remove-btn:hover {
  background-color: #ffb3b3; /* 호버 시 약간 더 어두운 옅은 빨강 */
  transform: scale(1.05); /* 호버 시 작은 확대 효과 */
}

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

.financial-info {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f0f7ff;
  border-radius: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.value-with-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.edit-input {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 200px;
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
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  text-align: center;
  align-items: center;
  font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
  font-weight: bold;
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

.save-btn {
  padding: 0.5rem 1rem;
  background-color: #48bb78;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-btn:hover {
  background-color: #38a169;
}

.cancel-btn {
  padding: 0.5rem 1rem;
  background-color: #e53e3e;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-btn:hover {
  background-color: #c53030;
}

.edit-btn {
  padding: 0.5rem 1rem;
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background-color: #cbd5e0;
}
</style>