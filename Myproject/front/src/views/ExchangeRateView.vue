<template>
  <div class="exchange-rate-calculator">
    <h1>환율 검색</h1>
    <div class="input-section">
      <select v-model="selectedCurrency">
        <option value="" selected disabled>국가를 선택해주세요.</option>
        <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency">
          {{ currency.cur_nm }} ({{ currency.cur_unit }})
        </option>
      </select>
      <input type="number" v-model="amount" placeholder="금액 입력" />
      <select v-model="inputCurrency">
        <option value="KRW">원화 (KRW)</option>
        <option value="foreign">외화</option>
      </select>
    </div>
    <div class="result-section">
      <p>변환 결과: {{ convertedAmount }}</p>
    </div>

    <div class="chart-container">
      <div class="chart-header">
        <span class="chart-title">환율 추이</span>
      </div>
      <div class="comparison-card">
        <div class="comparison-item">
          <div class="comparison-label">현재 환율</div>
          <div class="comparison-value">
            {{ selectedCurrency ? selectedCurrency.deal_bas_r : '-' }} 원
          </div>
        </div>
      </div>
    </div>

    <!-- 모달 열림 상태를 관리하는 변수 -->
    <v-dialog v-model="showModal" persistent max-width="400px">
      <!-- 모달 내부 카드 -->
      <v-card>
        <!-- 모달 헤더 -->
        <v-card-title>
          <span class="text-h6">알림</span>
        </v-card-title>
        <!-- 모달 본문 -->
        <v-card-text>
          환율 정보를 불러오는데 실패했습니다.<br />
          잠시 후 다시 시도해주세요.
        </v-card-text>
        <!-- 모달 푸터 -->
        <v-card-actions>
          <v-btn color="primary" text @click="showModal = false, router.push({ name: 'main'})" >
            닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
// 나라들 정보 담기
const currencies = ref([])
// 선택된 국가
const selectedCurrency = ref('')
// 내가 입력할 돈정보
const amount = ref(null)
const inputCurrency = ref('KRW')
const showModal = ref(false) // 모달 표시 여부
const router = useRouter()


const convertedAmount = computed(() => {
  if (!selectedCurrency.value || !amount.value)
    return '선택된 국가가 없습니다.'
  // 매매기준율 기준으로 계산
  const rate = selectedCurrency.value.deal_bas_r
  if (inputCurrency.value === 'KRW') {
    return `${(amount.value / rate).toFixed(2)} ${selectedCurrency.value.cur_unit}`
  } else {
    return `${(amount.value * rate).toFixed(2)} KRW`
  }
})

// 환율 검색 페이지 들어가면 환율정보 먼저 비동기적으로 불러옴
const fetchExchangeRates = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v2/exchange-rates/')
    // 나라들 정보 담기
    currencies.value = response.data.filter(currency => currency.result === 1)
  } catch (error) {
    console.error('환율 정보를 가져오는 데 실패했습니다:', error)
    showModal.value = true // 모달 표시
  }
}

onMounted(() => {
  fetchExchangeRates()
})
</script>


<style scoped>

.exchange-rate-calculator {
  max-width: 800px;
  margin: 100px auto;
  padding: 80px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif;
}

h1 {
  color: #333333;
  text-align: left;
  margin-bottom: 40px;
  font-size: 26px;
  font-weight: 600;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

select,
input {
  width: 100%;
  padding: 15px;
  font-size: 16px;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  background-color: #ffffff;
  color: #333333;
  transition: all 0.2s ease;
}

select:hover,
input:hover {
  border-color: #0053a6;
  background-color: #f8fbff;
}

select:focus,
input:focus {
  outline: none;
  border-color: #4B89DC;
  box-shadow: 0 0 0 3px rgba(75, 137, 220, 0.1);
}

.submit-button {
  margin-top: 20px;
  padding: 16px;
  border: none;
  border-radius: 12px;
  background-color: #4B89DC;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-button:hover {
  background-color: #357abd;
}

.result-section {
  background-color: #ffffff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 83, 166, 0.08);
  margin-bottom: 30px;
}

.result-section p {
  color: #51b7dc6;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.chart-container {
  margin-top: 40px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 16px;
}


.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}


.chart-title {
  color: #51b7dc;
  font-size: 18px;
  font-weight: 600;
}

.chart-period-selector {
  display: flex;
  gap: 10px;
}

.period-button {
  padding: 8px 16px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  background-color: white;
  color: #666666;
  font-size: 14px;
  cursor: pointer;
}

.period-button:hover {
  background-color: #51b7dc;
  color: #ffffff;
}


.period-button.active {
  background-color: #4B89DC;
  color: white;
  border-color: #4B89DC;
}

.comparison-card {
  display: flex;
  justify-content: space-between;
  background-color: #f8fbff;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

.comparison-item {
  text-align: center;
  flex: 1;
}

.comparison-label {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.comparison-value {
  color: #51b7dc;
  font-size: 20px;
  font-weight: bold;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  color: #666666;
  margin-bottom: 4px;
}

@media (max-width: 768px) {
  .input-section {
    grid-template-columns: 1fr;
  }

  .exchange-rate-calculator {
    margin: 15px;
    padding: 20px;
  }

  .comparison-card {
    flex-direction: column;
    gap: 15px;
  }

  .charts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 20px 0;
  }

  .line-chart,
  .bar-chart {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 83, 166, 0.1);
  }

  .line-chart h3,
  .bar-chart h3 {
    color: #51b7dc;
    font-size: 16px;
    margin-bottom: 15px;
  }

  @media (max-width: 768px) {
    .charts-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 768px) {
    .exchange-rate-calculator {
      padding: 20px;
      margin: 16px;
    }
  }



}
</style>