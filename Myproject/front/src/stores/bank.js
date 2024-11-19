import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBankStore = defineStore('bank', () => {
  //더미 데이터를 생성해서 대략적인 틀을 잡아갈 수 있음
  //일단은 메인 data만 다뤄보자 => 3개만 만들어보자
  //순위, 6개월, 12개월, 세전이자, 세후이자, 24개월, 36개월, 금융기관, 상품, update

  //더미 데이터 그자체를 ..
  const dummyData = reactive([
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/save-deposit-products/',
      })   
  ])

  // {'순위': 1,
  //   '6개월': 1.30,
  //   '12개월': 3.90,
  //   '세전이자': 390000,
  //   '세후이자': 329940,
  //   '24개월': 1.50,
  //   '36개월': 1.50,
  //   '금융기관': 'MG 보은',
  //   '상품': 'Block예금',
  //   'update': '11.18'
  //   },
  //   {'순위': 2,
  //   '6개월': '-',
  //   '12개월': 3.90,
  //   '세전이자': 390000,
  //   '세후이자': 329940,
  //   '24개월': '-',
  //   '36개월': '-',
  //   '금융기관': 'MG 보은',
  //   '상품': 'MG 더뱅킹 정기예금',
  //   'update': '10.28'
  //   },
  //   {'순위': 3,
  //   '6개월': '-',
  //   '12개월': 3.90,
  //   '세전이자': 380000,
  //   '세후이자': 321480,
  //   '24개월': '-',
  //   '36개월': '-',
  //   '금융기관': '봉화 신협',
  //   '상품': '파워정기예탁금',
  //   'update': '11.18'
  //   },


  //user가 입력한 예치금 데이터
  const userDepositData = ref(null)
  //v-model로 추가 유저 데이터 입력값 받아오기
  const getUserData = function(data){
    userDepositData.value = data //data 자체를 받아오기
  }

  //정기 예금 검색 조건들 => 더미 데이터, 추가적으로 입력하게 될 데이터들
  //title, content부분 받아와서 진행할 필요 있음
  let id = 1
  const findCondition = reactive([
    //option에 사용될 데이터들..
    {id: id++, title: '세율', content: ['일반과세', '세금우대', '비과세']},
    {id: id++, title: '이자지급방식', content: ['전체', '만기지급', '월지급']},
    {id: id++, title: '가입방식', content: ['전체', '온라인', '방문']},
    //예치금액은 input받는 값 => v-model로 input받고 또 던져줘야 함
    //편의를 위해 이것도 동일하게 생성
    {id: id++, title: '예치금액', content: userDepositData},
    {id: id++, title: '예치기간', content: ['6개월', '12개월', '24개월', '36개월']},
    //추후 데이터 넣을 것 현재는 더미데이터
    {id: id++, title: '지역', content: ['서울', '부산', '경기', '인천', '포항']},
  ])


  return {  dummyData, findCondition, getUserData  }
})
