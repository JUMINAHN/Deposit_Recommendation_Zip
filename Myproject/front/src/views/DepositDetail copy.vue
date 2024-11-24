<template>
  <div class="detailPage">
    <v-container>
      <v-row>
        <!-- 왼쪽 이미지 섹션 -->
        <v-col cols="5">
          <v-img
            :src="recommend"
            alt="Bank Illustration"
            class="bank-image"
            contain
          ></v-img>
        </v-col>

        <!-- 오른쪽 상세 정보 섹션 -->
        <v-col cols="7">
          <div class="detail-content">
            <h3 class="bank-title">{{ bankName }}</h3>
            
            <div class="product-name">{{ productName }}</div>
            
            <v-divider class="divider"></v-divider>
            
            <div class="info-section">

              <div class="info-item">
                <div class="info-label">상세 정보</div>
                <div class="info-content">
                  우대 금리 : {{ maxRate }} <br>
                  최고 금리 : {{ maxRate2 ? maxRate2 : '해당 값이 없음'}} <br>
                  개월 수 : {{ month }} 개월
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-label">가입 방법</div>
                <div class="info-content">
                  {{ joinWay }}
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-label">특이 사항</div>
                <div class="info-content">
                  {{ special || '특이사항이 없습니다.' }}
                </div>
              </div>
            </div>

            <!--true이면 바꿔줌 -->
            <v-btn
              class="cart-button"
              elevation="2"
              @click="toggleProduct"
            >
              {{ productResult ? '관심상품 제거' : '관심상품 등록' }}
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import recommend from '@/assets/images/detailbank.jpg'
import { useBankStore } from '@/stores/bank'
import { useRoute } from "vue-router"
import { ref, onMounted, computed } from 'vue'

const route = useRoute()
const bankName = ref('')
const productName = ref('')
const store = useBankStore()
const detailInfo = ref('')
const joinWay = ref('')
const special = ref('')
const maxRate = ref('')
const maxRate2 = ref('')
const month = ref('')

// onMounted 수정
onMounted(async () => {
  try {
    bankName.value = route.params.bankName
    productName.value = route.params.productName
    
    // 순차적으로 처리
    await store.fetchUserInfo()
    await store.getOptionDeposit()
    await checkProductStatus()
    
    const resultData = store.findDepositDetail(bankName.value, productName.value)
    if (resultData && resultData[0]) {
      special.value = resultData[0].special || '관련 데이터가 없습니다.'
      joinWay.value = resultData[0].joinWay || '관련 데이터가 없습니다.'
      maxRate.value = resultData[0].maxRate
      maxRate2.value = resultData[0].maxRate2 
      month.value = resultData[0].month
    }
  } catch (error) {
    console.error('데이터 로딩 중 오류 발생:', error)
  }
})

// 상품 상태 확인 함수
const checkProductStatus = async () => {
  try {
    if (!store.userInfo?.username) {
      await store.fetchUserInfo()
    }
    const preferences = await store.getPreferences()
    if (preferences && Array.isArray(preferences)) {
      const isProductInPreferences = preferences.some(
        pref => 
          pref.bankname?.trim() === bankName.value?.trim() && 
          pref.products?.trim() === productName.value?.trim()
      )
      if (productResult.value !== isProductInPreferences) {
        productResult.value = isProductInPreferences
      }
    }
  } catch (error) {
    console.error('상품 상태 확인 중 오류 발생:', error)
    productResult.value = false
  }
}

const productResult = ref(false)
// toggleProduct 함수 개선
const toggleProduct = async () => {
  try {
    if (productResult.value) {
      await store.removeFromPreference(bankName.value, productName.value)
      productResult.value = false  // 즉시 UI 업데이트
    } else {
      await store.addToPreference(bankName.value, productName.value)
      productResult.value = true   // 즉시 UI 업데이트
    }
    
    // 서버와 상태 동기화
    setTimeout(async () => {
      await checkProductStatus()
    }, 500)
    
  } catch (error) {
    console.error('상품 토글 중 오류 발생:', error)
    // 에러 발생 시 상태 복원
    await checkProductStatus()
  }
}
</script>

<style scoped>
/* 문제 원인:고정된(fixed) 네비게이션 바가 페이지 컨텐츠와 겹침
해결 방법: */

.detailPage {
  /* margin: 40px auto; 기존 코드 수정 */
  margin-top: 100px;
  margin-bottom: 40px;
  margin-left: auto;
  margin-right: auto;
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
}

.bank-image {
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.detail-content {
  padding: 0 20px;
}

.bank-title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 15px;
  font-weight: 600;
}

.product-name {
  font-size: 20px;
  color: #3498db;
  margin-bottom: 20px;
}

.divider {
  border-color: rgba(44, 62, 80, 0.2);
  margin: 20px 0;
}

.info-section {
  margin: 25px 0;
}

.info-item {
  margin-bottom: 20px;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.info-label {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
  margin-bottom: 8px;
}

.info-content {
  color: #34495e;
  line-height: 1.6;
}

.info-content ul {
  list-style-type: none;
  padding-left: 0;
}

.info-content ul li {
  margin-bottom: 5px;
}

.cart-button {
  background-color: #3498db !important;
  color: white !important;
  padding: 0 30px !important;
  height: 45px;
  font-size: 16px;
  text-transform: none;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.cart-button:hover {
  background-color: #2980b9 !important;
  transform: translateY(-2px);
}
</style>