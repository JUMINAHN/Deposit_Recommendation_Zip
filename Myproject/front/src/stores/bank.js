import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'


export const useBankStore = defineStore('bank', () => {
  const token = ref(null) //token은 null
  const depositData = ref([])

  //save-deposit 자체를 실행하지 않았음을 알 수 있음 이거 진행해야 함
  


  const getDepositData = async function () {
    //응답 자체를 받아오고 활용하던지 해야할 것 같음
    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/deposit-products/'
      })
      const arrayData = response.data

      depositData.value = arrayData.map((item, index) => {
        const bankname = item.kor_co_nm
        const products = item.fin_prdt_nm
        const options = item.options

        // 초기값을 '-'로 설정
        let six = '-'
        let twelve = '-'
        let twenty_four = '-'
        let thirty_six = '-'

        // options가 존재하면 처리
        if (options && Array.isArray(options)) {
          options.forEach(option => {
            const rate = option.intr_rate2

            // save_trm에 따라 해당 기간의 이자율 설정
            switch (option.save_trm) {
              case 6:
                six = rate
                break
              case 12:
                twelve = rate
                break
              case 24:
                twenty_four = rate
                break
              case 36:
                thirty_six = rate
                break
            }
          })
        }
        // // 세전이자 계산 (12개월 기준)
        // const preTaxInterest = twelve !== '-' ? Math.floor(twelve * 10000) : 0
        // // 세후이자 계산 (세금 15.4% 제외)
        // const postTaxInterest = Math.floor(preTaxInterest * 0.846)

        //추후 계산값 반환
        return {
          '금융기관': bankname,
          '상품': products,
          '6개월': six,
          '12개월': twelve,
          '24개월': twenty_four,
          '36개월': thirty_six,
          '예상금액': '-'
        }
      })

      return depositData

    } catch (error) {
      console.error('데이터 변환 중 오류 발생:', error)
      throw error
    }
  }

  let id = 1
  const findCondition = ref([
    { id: id++, title: '예치금액', content: [], selectedValue: '' }, //해당값 v-binding으로 가져와서 입력받아야 함
    { id: id++, title: '예치기간', content: ['6개월', '12개월', '24개월', '36개월'], selectedValue: '' },
  ]) 

  //지피티 도움
  const getUserInput = async function (selectedValues) {
    const [amount, period] = selectedValues
    const numericAmount = parseFloat(amount)

    //원화 생성..!! : 지피티
    const formatter = new Intl.NumberFormat('ko-KR', {
      style: 'decimal',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    });


    // depositData.value를 직접 수정
    depositData.value = depositData.value.map((deposit) => {
      const rate = parseFloat(deposit[period])
      const result = !isNaN(rate) && !isNaN(numericAmount)
        ? (numericAmount * rate / 100)
        : 0
      return {
        ...deposit,
        '예상금액': result === 0 ? '-' : `${formatter.format(Math.round(result))}원`,
        // 정렬을 위한 숫자 값 추가
        '정렬용_예상금액': result
      }
    })
    // 내림차순 정렬 추가 => sort
    depositData.value.sort((a, b) => b['정렬용_예상금액'] - a['정렬용_예상금액'])


    console.log('Updated depositData:', depositData.value)
    return depositData.value
  }

  // 로그아웃 함수 추가
  const logoutUser = async function () {
    try {
      const response = await axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/logout/',
        headers: {
          Authorization: `Token ${token.value}` //토큰 관련 정보
        }
      })
      // 로그아웃 성공 시 토큰 제거
      localStorage.removeItem('token') //해당 정보 삭제
      token.value = null
      return true
    } catch (error) {
      console.error('로그아웃 실패:', error)
      return false
    }
  }


  //로그인 관련 데이터 확보 : 로그인 데이터 확보
  const findUser = async function (userLoginData) {
    const { username, email, password } = userLoginData
    console.log(username, email, password, ' 없어?')
    try {
      // FormData 객체 생성
      const formData = new FormData()
      formData.append('username', username.value)
      formData.append('email', email.value)
      formData.append('password', password.value)
      const response = await axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/login/', //login url
        data: formData,

      })
      console.log(response, ': 응답 데이터 확인')
      token.value = response.data.key  // response.data.key로 수정
      //local에 저장 => local 저장
      localStorage.setItem('token', response.data.key)  // localStorage에 저장 추가
      console.log('로그인이 완료되었습니다.') //서버에 단순 요청함으로써 일치여부 확인
      return true
    } catch {
      console.log('에러 발생')
      return false
    }
  }

  const router = useRouter()
  // 회원 가입 데이터
  // 토큰 생성이 필요함
  const signUpComplete = async function (userData) {
    const { name, email, password1, password2 } = userData
    try {
      const response = axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/signup/', //회원 가입 URL 추가 예정
        // 받아올 애들
        data: { //params는 get으로 받을때 사용
          // nickname,
          username: name.value,
          email: email.value,
          password1: password1.value,
          password2: password2.value,
        }
      })
      console.log(response, ': 응답 데이터 확인')
      console.log('회원가입이 완료되었습니다.') //서버에 단순 요청함으로써 일치여부 확인
      router.push({ name: 'login' }) //로그인 페이지 이동
      return true //회원가입 로직 확인 완료
    } catch {
      console.log('에러가 발생했습니다.')
      return false
    }
  }



  return { getDepositData, findCondition, getUserInput,
           findUser, signUpComplete, token, logoutUser,
           depositData }
}, { persist: true }) 
