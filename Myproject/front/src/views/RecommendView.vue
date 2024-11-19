<template>
  <v-container justify="center" align="center">
    <v-form @submit.prevent>
      <v-card justify="flex-wrap">
        <v-container fluid>
          <v-row>
            <v-col cols="2"
            v-for="find in findCondition"
            :key="find.id">
              <v-combobox
                v-model="value"
                :items="find.content"
                :label="find.title"
              ></v-combobox>
            </v-col>
          </v-row>
        </v-container>
        <v-btn
          class="mt-4"
          color="blue"
          block
        >
          나에게 맞는 상품 찾기 CLICK 💨
        </v-btn>
      </v-card>
    </v-form>


    <img src="@/assets/images/whatsInMyWeb.jpg" alt="" width="600px">

    <!--SEARCH 자체로 필터링을 하게 : 옆에 화면을 띄우려고 했는데 시행착오 多-->
    <div>
      <v-card
        title="예금 상품 추천"
        flat
      >
        <template v-slot:text>
          <v-text-field
            v-model="search"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
          ></v-text-field>
        </template>
  
        <!--dummy data받아옴-->
        <!--items가 항목 관련 된 내용을 받는 것-->
        <!--전체 데이터 -->
        <v-data-table
          :headers="headers"
          :items="dummyData"
          :search="search"
        ></v-data-table>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
  //더미 데이터를 생성해서 대략적인 틀을 잡아갈 수 있음
  //일단은 메인 data만 다뤄보자 => 3개만 만들어보자
  //순위, 6개월, 12개월, 세전이자, 세후이자, 24개월, 36개월, 금융기관, 상품, update
  const dummyData = [
    {'순위': 1,
    '6개월': 1.30,
    '12개월': 3.90,
    '세전이자': 390000,
    '세후이자': 329940,
    '24개월': 1.50,
    '36개월': 1.50,
    '금융기관': 'MG 보은',
    '상품': 'Block예금',
    'update': '11.18'
    },

    {'순위': 2,
    '6개월': '-',
    '12개월': 3.90,
    '세전이자': 390000,
    '세후이자': 329940,
    '24개월': '-',
    '36개월': '-',
    '금융기관': 'MG 보은',
    '상품': 'MG 더뱅킹 정기예금',
    'update': '10.28'
    },
    
    {'순위': 3,
    '6개월': '-',
    '12개월': 3.90,
    '세전이자': 380000,
    '세후이자': 321480,
    '24개월': '-',
    '36개월': '-',
    '금융기관': '봉화 신협',
    '상품': '파워정기예탁금',
    'update': '11.18'
    },
  ]

  //정기 예금 검색 조건들
  let id = 1
  const findCondition = [
    //option에 사용될 데이터들..
    {id: id++, title: '세율', content: ['일반과세', '세금우대', '비과세']},
    {id: id++, title: '이자지급방식', content: ['전체', '만기지급', '월지급']},
    {id: id++, title: '가입방식', content: ['전체', '온라인', '방문']},
    //예치금액은 input받는 값 => v-model로 input받고 또 던져줘야 함
    //편의를 위해 이것도 동일하게 생성
    {id: id++, title: '예치금액', content: [1000, 5000, 10000, 15000, 20000, 30000, 100000]},
    {id: id++, title: '예치기간', content: ['6개월', '12개월', '24개월', '36개월']},
    //추후 데이터 넣을 것 현재는 더미데이터
    {id: id++, title: '지역', content: ['서울', '부산', '경기', '인천', '포항']},
  ]

</script>

<style scoped>
  img {
    margin-top:30px;
  }
</style>