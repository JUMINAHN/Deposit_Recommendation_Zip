<template>
  <v-container justify="center" align="center">
    <div>
      <!--submit form으로 진행해야 할 것 같기도.. -->
      <!--현재 값을 선택하면 그 값으로 고정되지 않는 문제 발견 : v-select에서 combobox로 변경-->
      <!--interface화면 통합시켜야하는데 이 문제 해결을 못하고 있음-->
      <v-row align="center"
      v-for="find in findCondition"
      :key="find.id">
        <v-col
          cols="1"
        >
        <!--binding 형식 사용시 오류 발생 : 단순 find key 추출-->
          <v-subheader v-text="find.title"></v-subheader>
        </v-col>
        <v-col
          cols="2"
        >
        <!--v-states가 각 역할에 대한 내용 > v-text에 대한 내용.. -->
          <v-combobox
            v-model="e6"
            :items="find.content"
            :menu-props="{ maxHeight: '400' }"
            label="Select"
          ></v-combobox>
        </v-col>
      </v-row>
    </div>

    <div>
      <v-card
    class="mx-auto"
    max-width="600"
  >
    <v-toolbar color="secondary">
      <v-btn icon="mdi-menu" variant="text"></v-btn>
      <v-toolbar-title>BANKS</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon="mdi-magnify" variant="text"></v-btn>
      <v-btn icon="mdi-view-module" variant="text"></v-btn>
    </v-toolbar>

    <v-list lines="two">
      <v-list-item
        v-for="bank in BankList"
        :key="bank.name"
      >
        <template v-slot:prepend>
          <v-avatar color="grey-lighten-1">
            <v-icon color="white">mdi-folder</v-icon>
          </v-avatar>
        </template>

        <template v-slot:append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
          ></v-btn>
        </template>
      </v-list-item>
      </v-list>
    </v-card>
    </div>

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

  let bankId = 1
  //은행 리스트
  const bankList = [
    {id: bankId++, name: '신협'},
    {id: bankId++, name: '새마을 금고'},
    {id: bankId++, name: '농/축협은행'},
    {id: bankId++, name: '저축 은행'},
    {id: bankId++, name: '기타'},
  ]

</script>

<style scoped>

</style>