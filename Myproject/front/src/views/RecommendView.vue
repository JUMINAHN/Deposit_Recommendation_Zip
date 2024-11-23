<template>
  <v-container class="main-content">
    <!-- 상단 예금상품 찾기 섹션 -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row align="center">
          <!-- 입력 필드 영역 -->
          <v-col cols="12" md="8">
            <v-row>
              <v-col v-for="(find, index) in findCondition" :key="find.id" cols="6">
                <v-combobox
                  v-model="find.selectedValue"
                  :items="find.content || []"
                  :label="find.title"
                  height="56"
                ></v-combobox>
              </v-col>
            </v-row>
          </v-col>
          <!-- 버튼 영역 - 높이와 너비 조정 -->
          <v-col cols="12" md="4" class="d-flex align-center">
            <v-btn 
              color="blue" 
              block 
              height="56"
              class="search-button"
              @click="findProducts"
            >
              나에게 맞는 상품 찾기 CLICK 💨
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- 메인 콘텐츠 영역 -->
    <v-row>
      <!-- 이미지 영역 -->
      <v-col cols="12" md="5">
        <v-img 
          :src="bankservice" 
          max-height="800" 
          contain
          class="rounded-lg"
        ></v-img>
      </v-col>

      <!-- 테이블 영역 -->
      <v-col cols="12" md="7">
        <v-card>
          <v-card-title>예금 상품 추천</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="search"
              label="원하는 검색어를 입력하세요 : (예시) 수협은행 or 정기예금"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              hide-details
              single-line
            ></v-text-field>
          </v-card-text>
          
          <div v-if="isLoading" class="pa-4">데이터 로딩 중...</div>
          <v-data-table
            v-else
            :headers="headers"
            :items="depositData"
            :search="search"
            @click:row="handleRowClick"
            class="cursor-pointer"
          >
          <template v-slot:item="props">
            <tr @click="handleRowClick(props.item)">
              <td v-for="header in headers" :key="header.key"
                  :class="{ 'highlighted-amount': header.key === '예상금액' && props.item[header.key] !== '-' }"
              >
                {{ props.item[header.key] }}
              </td>
            </tr>
          </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useBankStore } from '@/stores/bank'
import { computed, onMounted, onUpdated, ref, watch } from 'vue'
import { storeToRefs } from 'pinia' //이거 뭐임?
import Swal from 'sweetalert2'
import { useRoute, useRouter } from 'vue-router'
import bankservice from '@/assets/images/bankservice.jpg'


const store = useBankStore()
// 주석: storeToRefs를 사용하여 반응형으로 store의 상태를 가져온다. => 기존에 풀려서 옴
const { depositData, findCondition } = storeToRefs(store)
//별도 구현하던거 진행
const displayItems = computed(() => depositData.value) //기존 items 역할
const search = ref('')
const router = useRouter()
//data table 만들기
const dummyKey = ['금융기관', '상품', '6개월', '12개월', '24개월', '36개월', '예상금액']
const headers = dummyKey.map(item => ({
  title: item,
  key: item
}))

const isLoading = ref(true)

onMounted(async () => {
  try {
    await store.getDepositData()
    isLoading.value = false
  } catch (error) {
    console.error('데이터 로딩 실패:', error)
    isLoading.value = false
  }
})

// 새로 추가된 코드 시작
const topResult = ref(null)
const isHighlighted = ref(false)
// 새로 추가된 코드 끝



const findProducts = async function() {
  const selectedValues = findCondition.value.map((condition) => condition.selectedValue.trim());
  // 입력값 확인
  if (!selectedValues[0] || !selectedValues[1]) {
    alert('값을 입력해주세요.')
    return
  }
  try {
    const updatedData = await store.getUserInput(selectedValues);
    depositData.value = [...updatedData];
    console.log('최신 데이터:', depositData.value);

   // 새로 추가된 코드 시작
   if (depositData.value.length > 0) {
  topResult.value = depositData.value[0]
  Swal.fire({
    title: '추천 상품',
    html: `
      <div style="text-align: left; margin: 10px 0;">
        <p>금융기관: ${topResult.value['금융기관']}</p>
        <p>상품: ${topResult.value['상품']}</p>
        <p>예상금액: ${topResult.value['예상금액']}</p>
      </div>
    `,
    icon: 'success',
    confirmButtonText: '확인'
  })
}

    isHighlighted.value = true // 클릭 시 하이라이트 활성화
  }
    // 새로 추가된 코드 끝
   catch (error) {
    console.error('데이터 처리 중 오류 발생:', error);
  }
}

// 클릭된 행을 추적하기 위한 상태 추가
const clickedRow = ref(null)

// 행이 클릭되었는지 확인하는 함수
const isClickedRow = (item) => {
  return clickedRow.value && 
         item['금융기관'] === clickedRow.value['금융기관'] && 
         item['상품'] === clickedRow.value['상품']
}

const handleRowClick = function(item) {
  // 클릭된 행 저장
  clickedRow.value = item
  
  try {
    const bankName = item['금융기관']
    const productName = item['상품']
    
    console.log('추출된 데이터:', { bankName, productName })

    if (!bankName || !productName) {
      console.error('데이터 누락:', item)
      return
    }

    // 라우팅 시도
    router.push({
      name: 'compared',
      params: {
        bankName: bankName,
        productName: productName
      }
    })
  } catch (error) {
    console.error('클릭 처리 중 오류:', error)
    console.error('문제의 데이터:', item)
  }
}

//   //상세 페이지 => 내용 가져오기 => router로
//   //deposit데이터로 호출을 한다 How? 
//   import { useBankStore } from '@/stores/bank'
//   import { useRoute } from "vue-router"
//   import { ref, onMounted } from 'vue'

//   const route = useRoute()
//   const bankName = ref('')
//   const productName = ref('')
//   const store = useBankStore()
//   const detailInfo = ref('')
//   const joinWay = ref('')
//   const special = ref('')

//   //그리고 거기 일치하는 데이터 다시 받아와야함
//   //store에 있는 내용들 담을 건데 => router로 
//   onMounted(() => {
//   // 라우트 파라미터 접근
//   bankName.value = route.params.bankName //parameter로 router 받아옴
//   productName.value = route.params.productName //productname로 router 받아옴
//   console.log('Bank Name:', bankName.value)
//   console.log('Product Name:', productName.value)
//     store.getOptionDeposit() 

//   const resultData = store.findDepositDetail(bankName.value, productName.value) //여기에 파라미터로 받아서 일치하는 값을 찾아서 전달
//   // console.log(resultData[0].special)    
//   if (resultData[0].special) {
//     special.value = resultData[0].special
//   } else {
//     special.value = '관련 데이터가 없습니다.'
//   }
  
//   if (resultData[0].joinWay) {
//     joinWay.value = resultData[0].joinWay
//   } else {
//     joinWay.value ='관련 데이터가 없습니다.'
//   }
  
//   if (resultData[0].detailInfo) {
//     detailInfo.value = resultData[0].detailInfo
//   } else {
//     detailInfo.value = '관련 데이터가 없습니다.'
//   }
  


// })




</script>

<style scoped>
.main-content {
  padding-top: 80px; /* 네비게이션 바 높이만큼 상단 패딩 추가 */
}

.v-img {
  max-width: 100%;
  height: auto;
}

.cursor-pointer {
  cursor: pointer;
}

.search-button {
  margin-top: 0;
}

/* 버튼과 입력 필드의 높이를 맞추기 위한 스타일 */
.v-btn {
  height: 56px !important;
}

.highlighted-row td {
  color: red !important;
  font-weight: bold;
}

/* 선택된 행에 호버 효과 추가 */
.v-data-table tr:hover td {
  background-color: rgba(0, 0, 0, 0.1);
}

.highlighted-amount {
  color: red !important;
  font-weight: bold;
}

</style>