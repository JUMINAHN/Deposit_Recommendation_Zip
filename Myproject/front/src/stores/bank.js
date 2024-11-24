import { ref, computed, reactive, watch } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'


export const useBankStore = defineStore('bank', () => {
  const token = ref(null) //회원정보
  const loginUserName = ref('') //token과 함께 저장해야 함
  const depositData = ref([]) //예금 정보 받아오기
  const detailDepositData = ref([]) //예금 상세 정보 받아오기
  const userInfo = ref([]) //유저 정보
  const userProduct = ref([]) //user가 담을 product => save 
  const router = useRouter()
  const nowUserProduct = ref([]) //지금 유저가 선택한 배열 리스트
  //사실 userProduct랑 동일함


  //서버에 예적금 API 데이터 요청
  const getDepositData = async function () {
    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/deposit-products/'
      })
      const arrayData = response.data
      //예적금 데이터 저장
      depositData.value = arrayData.map((item, index) => {
        const bankname = item.kor_co_nm
        const products = item.fin_prdt_nm
        const options = item.options

        let six = '-'
        let twelve = '-'
        let twenty_four = '-'
        let thirty_six = '-'

        if (options && Array.isArray(options)) {
          options.forEach(option => {
            const rate = option.intr_rate2

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

  //서버에 예적금 상세 페이지 정보 요청
  //단순 금리 정보 외 => 가입 방법 / 우대 사항
  const getOptionDeposit = async function () {
    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/deposit-products/'
      })
      const arrayData = response.data
      //상세 데이터 저장
      detailDepositData.value = arrayData.map((item, index) => {
        const bankname = item.kor_co_nm
        const products = item.fin_prdt_nm
        const joinWay = item.join_way
        const special = item.spcl_cnd
        const options = item.options
        let six = 0
        let twelve = 0
        let twenty_four = 0
        let thirty_six = 0
        options.forEach(option => { //뽑은 options에서 우대 금리
          const rate = option.intr_rate 
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
        let month = '' 
        let maxRate2 = ''
        const maxRate = Math.max(six, twelve, twenty_four, thirty_six)
        const resultOption = options.filter((option)=> {
          return (option.intr_rate === maxRate) 
        })
        month = resultOption[0].save_trm
        maxRate2 = resultOption[0].intr_rate2

        return {
          'bankname': bankname,
          'products': products,
          'joinWay': joinWay,
          'special': special,
          //추가
          'month' : month, //개월 수
          'maxRate' : maxRate,  //가장 높은 금리1
          'maxRate2' : maxRate2 //금리 1 기준 우대 금리1
        }
      })
      return detailDepositData //저장 값 반환
    } catch (error) {
      console.error('데이터 변환 중 오류 발생:', error)
      throw error
    }
  }

  //예적금 상세 정보 보유 여부 검색
  const findDepositDetail = function (paramsBank, paramsProudct) {
    const resultData = detailDepositData.value.filter((item) => {
      if (item.bankname === paramsBank && item.products === paramsProudct) {
        return item 
      }
    })
    return resultData //상세 정보 보유 여부 true/false반환
  }

  const userGetProduct = async function(bankName, productName) {
    console.log('getProudct 내부 들어와졌고 뱔류갑 업떻게 생겼는지 확인')    
    console.log(userProduct.value, 'value?') 
    const result = ref(true) 
    if (Array.isArray(userProduct.value)) {
      result.value = userProduct.value.some((item) => {
        if (item.bankName === bankName && item.productName === productName) {
          console.log('일치값 발견')
          return result.value = true
        } else {
          console.log('일치값이 없음')
          return result.value = false
        }
      })
    } else {
      if(userProduct.value.bankName === bankName && userProduct.value.productName === productName) {
        return result.value = true
      } else {
        return result.value = false
      }
    }

    return result //some 반환값
  }

  let id = 1
  const findCondition = ref([
    { id: id++, title: '예치금액', content: [], selectedValue: '' }, //해당값 v-binding으로 가져와서 입력받아야 함
    { id: id++, title: '예치기간', content: ['6개월', '12개월', '24개월', '36개월'], selectedValue: '' },
  ])

  //사용자에게 input 받을 값 
  const getUserInput = async function (selectedValues) {
    const [amount, period] = selectedValues
    const numericAmount = parseFloat(amount)

    //원화 데이터 생성
    const formatter = new Intl.NumberFormat('ko-KR', {
      style: 'decimal',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    })

    // 결과값 할당
    depositData.value = depositData.value.map((deposit) => {
      const rate = parseFloat(deposit[period])
      const result = !isNaN(rate) && !isNaN(numericAmount)
        ? (numericAmount * rate / 100)
        : 0
      return {
        ...deposit,
        '예상금액': result === 0 ? '-' : `${formatter.format(Math.round(result))}원`,
        '정렬용_예상금액': result
      }
    })
    depositData.value.sort((a, b) => b['정렬용_예상금액'] - a['정렬용_예상금액'])
    return depositData.value
  }

  // 로그아웃
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

    loginUserName.value = typeof username === 'object' && username.value 
    ? username.value 
    : username; //    loginUserName.value = username.value //값이 제대로 안들어가지는데
    try {
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
      token.value = response.data.key
      localStorage.setItem('token', token.value) 
      await fetchUserInfo() //사용자 정보 가져오기 함수
      // localStorage에 저장 추가
      console.log('로그인이 완료되었습니다.') //서버에 단순 요청함으로써 일치여부 확인
      return true
    } catch {
      console.log('에러 발생')
      return false
    }
  }

  // 회원 가입 데이터
  // 토큰 생성이 필요함
  const signUpComplete = async function (userData) {
    try {
      const response = await axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/signup/',
        data: {
          username: userData.name.value,
          email: userData.email.value,
          password1: userData.password1.value,
          password2: userData.password2.value,
        }
      })
      
      if (response.data) {
        router.push({ name: 'login' })
        return true
      }
      return false
    } catch (error) {
      console.error('회원가입 실패:', error)
      return false
    }
  }

    const addToPreference = async (bankName, productName) => {
      try {
        // 1. userInfo 확인 및 로드
        if (!userInfo.value || !userInfo.value.username) {
          await fetchUserInfo()
          if (!userInfo.value || !userInfo.value.username) {
            throw new Error('사용자 정보를 불러올 수 없습니다')
          }
        }
    
        
        // 2. URL 인코딩
        const encodedBankName = encodeURIComponent(bankName)
        const encodedProductName = encodeURIComponent(productName)
        
        // 3. API 호출
        const response = await axios.post(
          `http://127.0.0.1:8000/app/accounts/profile/${userInfo.value.username}/preference/save/${encodedBankName}/${encodedProductName}/`,
          {},
          {
            headers: { 
              Authorization: `Token ${token.value}`,
              'Content-Type': 'application/json'
            }
          }
        )
    
        // 4. 성공 처리
        alert(response.data.message || '장바구니에 상품을 담았습니다!')
        return true
      } catch (error) {
        console.error('장바구니 추가 실패:', error)
        alert(error.response?.data?.message || '장바구니 상품을 담는 과정에서 에러가 발생했습니다.')
        return false
      }
    }

    const removeFromPreference = async (bankName, productName) => {
      try {
        if (!userInfo.value || !userInfo.value.username) {
          await fetchUserInfo()
        }
        
        const encodedBankName = encodeURIComponent(bankName)
        const encodedProductName = encodeURIComponent(productName)
        
        await axios.delete(
          `http://127.0.0.1:8000/app/accounts/profile/${userInfo.value.username}/preference/delete/${encodedBankName}/${encodedProductName}/`,
          {
            headers: { Authorization: `Token ${token.value}` }
          }
        )
        alert('관심 상품에서 제거되었습니다.')
        return true
      } catch (error) {
        console.error('장바구니 제거 실패:', error)
        alert(error.response?.data?.message || '장바구니 상품을 삭제하는 과정에서 에러가 발생했습니다.')
        return false
      }
    }

    const getPreferences = async () => {
      try {
        if (!userInfo.value || !userInfo.value.username) {
          await fetchUserInfo()
        }
        
        // 예금 상품 데이터 먼저 가져오기
        const depositResponse = await axios.get(
          'http://127.0.0.1:8000/api/v1/deposit-products/',
          {
            headers: { Authorization: `Token ${token.value}` }
          }
        )
        
        // 선호 상품 목록 가져오기
        const prefResponse = await axios.get(
          `http://127.0.0.1:8000/app/accounts/profile/${userInfo.value.username}/preference/`,
          {
            headers: { Authorization: `Token ${token.value}` }
          }
        )
        
        // 두 데이터 매핑
        return prefResponse.data.map(pref => {
          const depositProduct = depositResponse.data.find(
            d => d.kor_co_nm === pref.bankname && d.fin_prdt_nm === pref.products
          )
          
          return {
            bankname: pref.bankname,
            products: pref.products,
            maxRate: depositProduct?.options[0]?.intr_rate || 0,
            maxRate2: depositProduct?.options[0]?.intr_rate2 || 0
          }
        })
      } catch (error) {
        console.error('선호도 목록 조회 실패:', error)
        return []
      }
    }

    const updateUserProfile = async (fieldName, value) => {
      try {
        const response = await axios.put(
          `http://127.0.0.1:8000/app/accounts/profile/${userInfo.value.username}/`,
          { [fieldName]: value },
          {
            headers: { 
              Authorization: `Token ${token.value}`,
              'Content-Type': 'application/json'
            }
          }
        )
        // 성공 시 userInfo 업데이트
        userInfo.value = response.data
        return true
      } catch (error) {
        console.error('프로필 수정 실패:', error)
        throw error
      }
    }

  
  const fetchUserInfo = async () => { //사용자 정보 가져오기
    try {
      const response = await axios.get('http://127.0.0.1:8000/app/accounts/profile/current/', {
        headers: { Authorization: `Token ${token.value}` }
      })
      userInfo.value = response.data
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
    }
  } 


  return {
    getDepositData, findCondition, getUserInput,
    findUser, signUpComplete, token, logoutUser,
    depositData, detailDepositData, findDepositDetail, getOptionDeposit,
    userProduct, nowUserProduct,userGetProduct, userInfo, getPreferences // loadUserProduct, getUserInfo, userSaveProducts, userDeleteProducts, 
    , addToPreference, removeFromPreference, updateUserProfile

  }
}, { persist: true }) 
