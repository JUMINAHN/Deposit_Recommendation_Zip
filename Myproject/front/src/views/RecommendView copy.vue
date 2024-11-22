<template>
  <v-container>
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
                ></v-combobox>
              </v-col>
            </v-row>
          </v-col>
          <!-- 버튼 영역 -->
          <v-col cols="12" md="4">
            <v-btn color="primary" block @click="findProducts">
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
          src="@/assets/images/whatsInMyWeb.jpg" 
          max-height="600" 
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
            <template v-slot:item="{ item }">
              <tr>
                <td v-for="header in headers" :key="header.key">
                  {{ item[header.key] }}
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
const handleRowClick = function(clickRow) {
  console.log('클릭된 행의 데이터', clickRow)
  if (clickRow['금융기관'] && clickRow['상품']) {
    router.push({
      name: 'compared',  // 'detail'에서 'compared'로 변경
      params: {
        bankName: clickRow['금융기관'],
        productName: clickRow['상품']
      }
    }).catch((err) => {
      console.log('라우팅 오류:', err)
    })
  } else {
    console.error('필요한 데이터가 누락되었습니다:', clickRow)
  }
}





</script>

<style scoped>
g {
  max-width: 100%;
  height: auto;
}

.cursor-pointer {
  cursor: pointer;
}

.v-card {
  height: 100%;
}
</style>