<template>
  <v-container justify="center" align="center">
    <v-form @submit.prevent>
      <v-card justify="flex-wrap">
        <v-container fluid>
          <!--해당 내용은 그대로 유지-->
          <v-row>
            <v-col cols="6"
            v-for="(find, index) in findCondition"
            :key="find.id">
            <v-combobox
              v-model="find.selectedValue"
              :items="find.content || []"
              :label="find.title"
            ></v-combobox>
            </v-col>
          </v-row>
        </v-container>
        <v-btn
          class="mt-4"
          color="blue"
          @click.prevent="findProducts()"
          block
        >
          나에게 맞는 상품 찾기 CLICK 💨
        </v-btn>
      </v-card>
    </v-form>


    <img src="@/assets/images/whatsInMyWeb.jpg" alt="" width="600px">
    <div>
      <v-card
        title="예금 상품 추천"
        flat
      >
      <template v-slot:text>
      <v-text-field
        v-model="search"
        label="원하는 검색어를 입력하세요 : (예시) 수협은행 or 정기예금"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        hide-details
        single-line
      ></v-text-field>
    </template>

    <!-- 주석: v-data-table 시작 태그 추가 -->
    <!--depositData 한개씩 : 해당 내용 라우터로 전달해야함-->
    <v-data-table
      :headers="headers"
      :items="depositData"
      :search="search"
      :key="depositData.length"
    >
      <!-- 새로 추가된 코드 시작 -->
      <template v-slot:item="{ item }">
        <tr>
          <td v-for="header in headers" :key="header.key" :class="{ 'red-border': header.key === '예상금액' && isHighlighted }">
            <span :style="{ color: header.key === '예상금액' && isHighlighted ? 'red' : 'inherit' }">
              {{ item[header.key] }}
            </span>
          </td>
        </tr>
      </template>
      <!-- 새로 추가된 코드 끝 -->
    </v-data-table> 
    <!-- 주석: v-data-table 닫는 태그 추가 -->

      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { useBankStore } from '@/stores/bank'
import { computed, onMounted, onUpdated, ref, watch } from 'vue'
import { storeToRefs } from 'pinia' //이거 뭐임?
import Swal from 'sweetalert2'


const store = useBankStore()
// 주석: storeToRefs를 사용하여 반응형으로 store의 상태를 가져온다. => 기존에 풀려서 옴
const { depositData, findCondition } = storeToRefs(store)
//별도 구현하던거 진행
const displayItems = computed(() => depositData.value) //기존 items 역할
const search = ref('')

//data table 만들기
const dummyKey = ['금융기관', '상품', '6개월', '12개월', '24개월', '36개월', '예상금액']
const headers = dummyKey.map(item => ({
  title: item,
  key: item
}))

onMounted(async() => {
  await store.getDepositData() //비동기로 데이터 받아오면 => store에서 실행되고
  //관련 getDepositData가 담긴 store.depositData를 활용한다.
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




</script>

<style scoped>
  img {
    margin-top:30px;
  }

/* 새로 추가된 스타일 시작 */
/* .v-data-table td.red-border {
  border: 2px solid red;
} */
/* 새로 추가된 스타일 끝 */

</style>