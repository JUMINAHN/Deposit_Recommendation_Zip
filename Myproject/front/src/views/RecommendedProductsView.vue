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
          <v-card-title class="blue-grey--text">{{ userInfo.age }}대 연령층의 선호 상품 TOP 5</v-card-title>
          <v-chart class="chart" :option="ageChartOption" autoresize />
        </v-card>
      </v-col>

      <!-- 자산 규모별 선호 상품 차트 -->
      <v-col cols="12" md="6">
        <v-card class="chart-card">
          <v-card-title class="blue-grey--text">비슷한 자산 규모 선호 상품</v-card-title>
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
                      <div class="recommendation-reason">
                        <v-icon small color="primary" class="mr-1">mdi-information</v-icon>
                        {{ getRecommendationReason(product) }}
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
// 차트 옵션 설정
const ageChartOption = computed(() => ({
  title: { text: '연령대별 선호도' },
  tooltip: { trigger: 'item' },
  legend: { orient: 'vertical', left: 'left' },
  series: [{
    type: 'pie',
    radius: '70%',
    data: [
      { value: 35, name: '20대' },
      { value: 30, name: '30대' },
      { value: 20, name: '40대' },
      { value: 15, name: '50대 이상' }
    ],
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      }
    }
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
</style>