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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
// 나라들 정보 담기
const currencies = ref([])
// 선택된 국가
const selectedCurrency = ref('')
// 내가 입력할 돈정보
const amount = ref(null)
const inputCurrency = ref('KRW')

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
  }
}

onMounted(() => {
  fetchExchangeRates()
})
</script>


<style scoped>
.exchange-rate-calculator {
  max-width: 600px;
  margin: 50px auto;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #1e90ff; /* 파란색 */
  text-align: center;
  margin-bottom: 40px;
  font-size: 32px;
  font-family: 'Arial', sans-serif;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 요소 간격 */
}

select, input {
  padding: 15px;
  font-size: 16px;
  border: none; /* 기본 테두리 제거 */
  border-radius: 10px; /* 둥근 모서리 */
  background-color: #f0f8ff; /* 파스텔 블루 배경 */
  transition: all 0.3s ease-in-out;
}

select:hover, input:hover {
  background-color: #e6f7ff; /* 호버 시 색상 변화 */
}

select:focus, input:focus {
  outline: none; /* 포커스 아웃라인 제거 */
  box-shadow: inset 0 0 5px rgba(30,144,255,0.5); /* 포커스 시 내부 그림자 */
}

.result-section {
  background-color: #e6f3ff; /* 연한 파란색 배경 */
  padding: 25px;
  border-radius: 10px;
  text-align: center;
}

.result-section p {
  font-size: 22px; /* 결과 텍스트 크기 */
  font-weight: bold;
  color: #2980b9; /* 진한 파란색 텍스트 */
}

@media (max-width: 600px) {
  .exchange-rate-calculator {
    padding: 20px; /* 모바일에서 패딩 조정 */
    margin: 20px; /* 모바일에서 마진 조정 */
    box-shadow: none; /* 모바일에서 그림자 제거 */
    border-radius: 10px; /* 모바일에서 둥근 모서리 조정 */
 }
}
</style>