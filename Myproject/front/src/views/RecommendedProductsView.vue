<template>
  <div class="recommendation-dashboard">
    <!-- 사용자 프로필 요약 -->
    <v-card class="profile-summary mb-4">
      <v-card-title>{{ userInfo.username }}님의 맞춤 금융 추천</v-card-title>
      <v-card-subtitle class="white--text">
        나이: {{ userInfo.age }}세 | 자산: {{ formatCurrency(userInfo.asset) }} | 연봉: {{ formatCurrency(userInfo.income) }}
      </v-card-subtitle>
    </v-card>

    <v-row>
      <!-- 연령대별 선호 상품 차트 -->
      <v-col cols="12" md="6">
        <v-card class="chart-card">
          <v-card-title class="blue-grey--text">추천된 상품의 연령대별 선호도</v-card-title>
          <v-chart class="chart" :option="ageChartOption" autoresize />
        </v-card>
      </v-col>

      <!-- 자산 규모별 선호 상품 차트 -->
      <v-col cols="12" md="6">
        <v-card class="chart-card">
          <v-card-title class="blue-grey--text">비슷한 자산 규모 금리</v-card-title>
          <v-chart class="chart" :option="assetChartOption" autoresize />
        </v-card>
      </v-col>

      <!-- 추천 상품 목록 -->
      <v-col cols="12">
        <v-card class="product-card">
          <v-card-title class="blue-grey--text">
            <v-icon color="primary" class="mr-2">mdi-star</v-icon>
            맞춤 추천 상품
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col v-for="product in recommendedProducts" 
                     :key="product.bankname + product.products" 
                     cols="12" md="4">
                <v-card elevation="2" class="product-item">
                  <!-- 매칭률 표시 -->
                  <div class="match-rate">
                    <v-progress-circular
                      :rotate="-90"
                      :size="50"
                      :width="7"
                      :model-value="calculateMatchRate(product.score)"
                      color="primary"
                    >
                      {{ calculateMatchRate(product.score) }}%
                    </v-progress-circular>
                  </div>
                  
                  <!-- 상품 정보 -->
                  <v-card-title class="text-h6">{{ product.bankname }}</v-card-title>
                  <v-card-text>
                    <div class="product-info">
                      <div class="product-name">{{ product.products }}</div>
                      <div class="interest-rate">
                        <span class="rate-label">기본금리</span>
                        <span class="rate-value">{{ product.maxRate }}%</span>
                      </div>
                      <div class="interest-rate">
                        <span class="rate-label">우대금리</span>
                        <span class="rate-value primary--text">{{ product.maxRate2 }}%</span>
                      </div>
                      <!-- 추천 태그들 -->
                      <div class="recommendation-tags">
                        <v-chip
                          v-for="reason in getProductReasons(product)"
                          :key="reason"
                          color="primary"
                          small
                          class="ma-1"
                        >
                          {{ reason }}
                        </v-chip>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
          

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'  // onMounted를 한 번만 import
import { storeToRefs } from 'pinia'
import { useBankStore } from '@/stores/bank'

const store = useBankStore()
const { detailDepositData, userInfo } = storeToRefs(store)


const recommendedProducts = computed(() => {
  if (!detailDepositData.value || !userInfo.value) return []
  
  const age = userInfo.value.age
  const asset = userInfo.value.asset
  const income = userInfo.value.income  // income 추가

  return detailDepositData.value
    .map(product => ({
      ...product,
      score: calculateRecommendationScore(product, age, asset, income),
      recommendationReason: getRecommendationReason(product, age, asset, income)
    }))
    .filter(product => product.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
})
const getRecommendationReason = (product, age, asset, income) => {
  const reasons = []
  
  // 연령대별 추천 이유
  if (age < 30) {
    reasons.push('청년층 우대 금리 혜택')
    if (product.maxRate2 > 3.5) reasons.push(`${product.maxRate2}% 고금리 상품`)
  } else if (age < 40) {
    reasons.push('30대 맞춤 안정적 상품')
  }
  
  // 자산 규모별 추천 이유
  if (asset > 100000000) {
    reasons.push('프리미엄 고객 전용 상품')
  } else if (asset > 50000000) {
    reasons.push('우수 고객 우대 혜택')
  }
  
  return reasons.join('\n')
}

const calculateAgeDistribution = (userAge) => {
  const ageGroup = Math.floor(userAge / 10) * 10;
  return [
    { value: ageGroup === 20 ? 40 : 20, name: '20대', itemStyle: { color: '#64B5F6' } },
    { value: ageGroup === 30 ? 40 : 25, name: '30대', itemStyle: { color: '#81C784' } },
    { value: ageGroup === 40 ? 40 : 20, name: '40대', itemStyle: { color: '#FFB74D' } },
    { value: ageGroup >= 50 ? 40 : 15, name: '50대 이상', itemStyle: { color: '#E57373' } }
  ];
};


const calculateRecommendationScore = (product, age, asset, income) => {
  let score = 0
  
  // 연령별 점수
  if (age < 30 && product.maxRate2 > 3.5) score += 3
  else if (age < 40 && product.maxRate2 > 3.0) score += 2
  else if (age < 50 && product.maxRate2 > 2.5) score += 2
  
  // 자산별 점수
  if (asset > 100000000 && product.maxRate2 > 4.0) score += 4
  else if (asset > 50000000 && product.maxRate2 > 3.5) score += 3
  else if (asset > 10000000 && product.maxRate2 > 3.0) score += 2
  
  // 소득별 점수
  if (income > 50000000 && product.maxRate2 > 3.8) score += 3
  else if (income > 30000000 && product.maxRate2 > 3.3) score += 2
  
  return score
}

// 매칭률 계산 함수
const calculateMatchRate = (score) => {
  return Math.min(Math.round((score / 10) * 100), 100)
}

// 추천 이유 배열로 변환
const getProductReasons = (product) => {
  if (!product.recommendationReason) return []
  return product.recommendationReason.split('\n').filter(reason => reason)
}


// 차트 옵션 설정
const ageChartOption = computed(() => ({
  title: { 
    text: '연령대별 선호도',
    textStyle: { fontSize: 16, fontWeight: 'bold' }
  },
  tooltip: { 
    trigger: 'item',
    formatter: '{b}: {c}%'
  },
  legend: { 
    orient: 'vertical',
    left: 'left',
    padding: 20,
    borderRadius: 10
  },
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],  // 도넛 형태로 변경
    center: ['60%', '50%'],
    avoidLabelOverlap: true,
    itemStyle: {
      borderRadius: 10,
      borderColor: '#fff',
      borderWidth: 2
    },
    label: {
      show: true,
      formatter: '{b}: {c}%'
    },
    data: [
      { value: 35, name: '20대', itemStyle: { color: '#64B5F6' } },
      { value: 30, name: '30대', itemStyle: { color: '#81C784' } },
      { value: 20, name: '40대', itemStyle: { color: '#FFB74D' } },
      { value: 15, name: '50대 이상', itemStyle: { color: '#E57373' } }
    ]
  }]
}))

const assetChartOption = computed(() => ({
  title: { text: '자산 규모별 평균 금리' },
  tooltip: { trigger: 'axis' },
  xAxis: {
    type: 'category',
    data: ['5천만원 미만', '5천만원~1억', '1억원 이상']
  },
  yAxis: {
    type: 'value',
    name: '평균 금리(%)'
  },
  series: [{
    type: 'bar',
    data: [3.2, 3.8, 4.2],
    itemStyle: {
      color: '#4CAF50'
    }
  }]
}))

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW'
  }).format(value)
}

onMounted(async () => {
  await nextTick()

  try {
    await store.getOptionDeposit()
  } catch (error) {
    console.error('Failed to load data:', error)
  }
})
</script>

<style scoped>
.blue-grey--text {
  background-color: rgba(173, 216, 230, 0.25); /* Light sky blue with 75% transparency */
  font-weight: 800; 
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}
.recommendation-dashboard {
  padding: 20px;
  margin-top: 64px; /* 네비게이션 바 높이만큼 여백 추가 */
}

.profile-summary {
  background: linear-gradient(135deg, #1976D2, #64B5F6);
  color: white;
}

.chart-card, .product-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart {
  height: 400px;
  width: 100%;
  padding: 20px;
}

.product-item {
  height: 100%;
  transition: transform 0.2s;
}

.product-item:hover {
  transform: translateY(-5px);
}

.product-info {
  padding: 10px 0;
}

.product-name {
  font-size: 1.1em;
  color: #1976D2;
  margin-bottom: 10px;
}

.interest-rate {
  display: flex;
  justify-content: space-between;
  margin: 5px 0;
}

.rate-label {
  color: #666;
}

.rate-value {
  font-weight: bold;
}

.recommendation-reason {
  margin-top: 15px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 8px;
  font-size: 0.9em;
  color: #555;
}

.product-card {
  border-radius: 20px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.match-rate {
  position: absolute;
  top: 10px;
  right: 10px;
}

.recommendation-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

</style>