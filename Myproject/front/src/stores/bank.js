import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBankStore = defineStore('bank', () => {
  const token = ref(null) //token은 null
  
  //더미 데이터 활용 메서드 => 이건 추후 활용할 예정
  // const dummyData = reactive([
  //   axios({
  //     method: 'get',
  //     url: 'http://127.0.0.1:8000/api/v1/save-deposit-products/',
  //     })   
  // ]

    //user가 입력한 예치금 데이터
  const userDepositData = ref(null)
  //v-model로 추가 유저 데이터 입력값 받아오기 (아직 미진행)
  const getUserData = function(data){
    userDepositData.value = data 
  }

  let id = 1
  const findCondition = reactive([
    {id: id++, title: '세율', content: ['일반과세', '세금우대', '비과세']},
    {id: id++, title: '이자지급방식', content: ['전체', '만기지급', '월지급']},
    {id: id++, title: '가입방식', content: ['전체', '온라인', '방문']},
    //예치금액은 input받는 값 => v-model로 input받고 또 던져줘야 함
    {id: id++, title: '예치금액', content: userDepositData},
    {id: id++, title: '예치기간', content: ['6개월', '12개월', '24개월', '36개월']},
    {id: id++, title: '지역', content: ['서울', '부산', '경기', '인천', '포항']},
  ])


  
  //로그인 데이터 : 더미 데이터 테스팅
  const findUser = async function(userLoginData) {
    const {email, password} = userLoginData
    const dummyUser = ({
      'email' : 'zamwa@naver.com',
      'password' : 'sleep123'
    })
    if (dummyUser.email === email && dummyUser.password === password) {
      console.log('로그인이 완료되었습니다.') //서버에 단순 요청함으로써 일치여부 확인
      console.log('응답 확인')
      return true
    }
    return false
  }

  //로그인 관련 데이터 확보 : 로그인 데이터 확보
  //로그인 데이터 토큰 확인 전달이 필요함 
  // const {email, password} = userLoginData
  // const findUser = async function(userLoginData){
  //     try {
  //     const response = axios({
  //       method : 'post',
  //       url : '', //login url
  //       params : {
  //         email,
  //         password
  //       }
  //     })
  //     console.log(response, ': 응답 데이터 확인')
  //     console.log('로그인이 완료되었습니다.') //서버에 단순 요청함으로써 일치여부 확인
  //       return true
  //   } catch{
  //     console.log('에러 발생')
  //     return false
  //   }
  // }


  //회원가입 데이터 : 더미 데이터 테스팅
  //async => 비동기 작업일때 진행
  // const signUpComplete = function(userData) {
  //   const {nickname, name, email, password} = userData //이거로 받는다 => 이것자체가 더미
  //   if (nickname !== null
  //     && name !== null
  //     && email !== null
  //     && password !== null) {
  //     console.log('응답 확인 : true') // '내부 데이터 확인해보기
  //     console.log(nickname, '단순 nickname')
  //     // console.log(nickname.value, '단순 nickname.value')
  //     return true
  //   }
  //   return false
  // }


  // 회원 가입 데이터
  // 토큰 생성이 필요함
  const signUpComplete = async function(userData) {
    const { name, email, password} = userData
    try {
      const response = axios({
        method : 'post',
        url : 'http://127.0.0.1:8000/accounts/signup/', //회원 가입 URL 추가 예정
        // 받아올 애들
        params: { 
          // nickname,
          username : name,
          email : email,
          password : password
        }
      })
      console.log(response, ': 응답 데이터 확인') 
      console.log('회원가입이 완료되었습니다.') //서버에 단순 요청함으로써 일치여부 확인
      return true //회원가입 로직 확인 완료
    } catch {
      console.log('에러가 발생했습니다.')
      return false
    }
  }


  return { findCondition, getUserData, findUser, signUpComplete }
}) //추후 persist => pinia넣을 것
