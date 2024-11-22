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
                  {{ detailInfo }}
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

            <v-btn
              class="cart-button"
              elevation="2"
            >
              관심상품 등록
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
import { ref, onMounted } from 'vue'

const route = useRoute()
const bankName = ref('')
const productName = ref('')
const store = useBankStore()
const detailInfo = ref('')
const joinWay = ref('')
const special = ref('')


onMounted(async () => {
  try {
    bankName.value = route.params.bankName
    productName.value = route.params.productName
    console.log('Bank Name:', bankName.value)
    console.log('Product Name:', productName.value)
    
    await store.getOptionDeposit()  // 비동기 호출 대기

    const resultData = store.findDepositDetail(bankName.value, productName.value)
    console.log('Result Data:', resultData) // 디버깅용
  // console.log(resultData[0].special)    
    if (resultData[0].special) {
      special.value = resultData[0].special
    } else {
      special.value = '관련 데이터가 없습니다.'
    }
    
    if (resultData[0].joinWay) {
      joinWay.value = resultData[0].joinWay
    } else {
      joinWay.value ='관련 데이터가 없습니다.'
    }
    
    // if (resultData[0].detailInfo) {
    //   detailInfo.value = resultData[0].detailInfo
    // } else {
    //   detailInfo.value = '관련 데이터가 없습니다.'
    // }
  
  } catch (error) {
    console.error('데이터 로딩 중 오류 발생:', error)
  }
})
</script>

<style scoped>
.detailPage {
  margin: 40px auto;
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