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

  // ============== 회원탈퇴 기능
  const clearUserInfo = async function () {
    userInfo.value = null
    token.value = null
    localStorage.removeItem('token')
  }

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
  
      detailDepositData.value = arrayData.map((item) => {
        const bankname = item.kor_co_nm
        const products = item.fin_prdt_nm
        const joinWay = item.join_way
        const special = item.spcl_cnd
        const options = item.options || [] // options가 없을 경우 빈 배열 할당
  
        let six = 0, twelve = 0, twenty_four = 0, thirty_six = 0
  
        // options가 존재하고 배열인 경우에만 처리
        if (Array.isArray(options) && options.length > 0) {
          options.forEach(option => {
            if (option && option.save_trm) {  // option과 save_trm이 존재하는지 확인
              const rate = option.intr_rate || 0
              switch (option.save_trm) {
                case 6: six = rate; break
                case 12: twelve = rate; break
                case 24: twenty_four = rate; break
                case 36: thirty_six = rate; break
              }
            }
          })
        }
  
        // 최대 금리 계산
        const maxRate = Math.max(six, twelve, twenty_four, thirty_six)
        const resultOption = options.find(option => option?.intr_rate === maxRate) || {}
  
        return {
          'bankname': bankname,
          'products': products,
          'joinWay': joinWay || '정보 없음',
          'special': special || '정보 없음',
          'month': resultOption.save_trm || 0,
          'maxRate': maxRate || 0,
          'maxRate2': resultOption.intr_rate2 || 0
        }
      })
  
      return detailDepositData
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
      if (!userInfo.value || !userInfo.value.username) {
        await fetchUserInfo()
        if (!userInfo.value || !userInfo.value.username) {
          throw new Error('사용자 정보를 불러올 수 없습니다')
        }
      }

      // URL 인코딩 전 공백과 특수문자 처리
      const cleanBankName = bankName.trim().replace(/\//g, '-')
      const cleanProductName = productName.trim().replace(/\//g, '-')
      
      const encodedBankName = encodeURIComponent(bankName.trim())
      const encodedProductName = encodeURIComponent(productName.trim())
  
      // URL 구성 확인을 위한 로그
      const url = `http://127.0.0.1:8000/app/accounts/profile/${userInfo.value.username}/preference/save/${encodedBankName}/${encodedProductName}/`
      console.log('요청 URL:', url)
  
      const response = await axios.post(
        url,
        {},
        {
          headers: {
            Authorization: `Token ${token.value}`,
            'Content-Type': 'application/json'
          }
        }
      )
  
      console.log('서버 응답:', response.data)
      alert('장바구니에 상품을 담았습니다!')
      return true
    } catch (error) {
      console.error('장바구니 추가 실패:', error.response || error)
      alert('장바구니 상품을 담는 과정에서 에러가 발생했습니다.')
      return false
    }
  }

  const removeFromPreference = async (bankName, productName) => {
    try {
      if (!userInfo.value || !userInfo.value.username) {
        await fetchUserInfo();
      }
  
      const encodedBankName = encodeURIComponent(bankName.trim());
      const encodedProductName = encodeURIComponent(productName.trim());
  
      await axios.delete(
`http://127.0.0.1:8000/app/accounts/profile/${userInfo.value.username}/preference/delete/${encodedBankName}/${encodedProductName}/`,        {
          headers: {
            Authorization: `Token ${token.value}`
          }
        }
      );
  
      alert('관심 상품에서 제거되었습니다.');
      return true;
    } catch (error) {
      console.error('장바구니 제거 실패:', error);
      alert(error.response?.data?.message || '장바구니 상품을 삭제하는 과정에서 에러가 발생했습니다.');
      return false;
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


  // 새로운 상태 추가
  const recommendedProducts = computed(() => {
    if (!detailDepositData.value || !userInfo.value) return []
    
    const age = userInfo.value.age
    const asset = userInfo.value.asset
    const income = userInfo.value.income
  
    return detailDepositData.value
      .map(product => ({
        ...product,
        score: calculateRecommendationScore(product, age, asset, income),
        recommendationReason: getRecommendationReason(product, age, asset, income)
      }))
      .filter(product => product.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5)
  })

  // 추천 상품을 가져오는 함수 추가
  const getRecommendedProducts = computed(() => {
    if (!detailDepositData.value || !userInfo.value) return []
    
    const age = userInfo.value.age
    const asset = userInfo.value.asset
    const gender = userInfo.value.gender
  
    return detailDepositData.value
      .map(product => {
        let score = 0
        let reasons = []
  
        // 연령대별 점수
        if (age < 30) {
          score += product.maxRate2 > 3.5 ? 3 : 1
          reasons.push('20대 우대 금리 제공')
        } else if (age < 40) {
          score += product.maxRate2 > 3.0 ? 2 : 1
          reasons.push('30대 맞춤 상품')
        }
  
        // 자산별 점수
        if (asset > 50000000) {
          score += product.maxRate2 > 4.0 ? 3 : 1
          reasons.push('고액자산가 우대')
        }
  
        // 성별별 추천 (예시)
        if (gender === 'F') {
          score += product.special?.includes('여성') ? 2 : 0
          if (product.special?.includes('여성')) reasons.push('여성 우대 상품')
        }
  
        return {
          ...product,
          score,
          recommendationReason: reasons.join('\n'),
          matchRate: Math.min(Math.round((score / 8) * 100), 100) // 매칭률 계산
        }
      })
      .filter(product => product.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5) // 상위 5개 상품만 추천
  })

  const getRecommendationReason = (product, age, asset, income) => {
    const reasons = []
    
    if (age < 30) {
      reasons.push('청년층 우대 금리 혜택')
      if (product.maxRate2 > 3.5) reasons.push(`${product.maxRate2}% 고금리 상품`)
    } else if (age < 40) {
      reasons.push('30대 맞춤 안정적 상품')
    }
    
    if (asset > 100000000) {
      reasons.push('프리미엄 고객 전용 상품')
    } else if (asset > 50000000) {
      reasons.push('우수 고객 우대 혜택')
    }
    
    if (income > 50000000) {
      reasons.push('고소득자 특별 우대')
    }
    
    return reasons.join('\n')
  }
  
const calculateRecommendationScore = (product, age, asset, income) => {
  let score = 0
  
  // 연령별 점수
  if (age < 30 && product.maxRate2 > 3.5) score += 3
  else if (age < 40 && product.maxRate2 > 3.0) score += 2
  else if (age < 50 && product.maxRate2 > 2.5) score += 2
  
  // 자산별 점수
  if (asset > 100000000 && product.maxRate2 > 4.0) score += 4
  else if (asset > 50000000 && product.maxRate2 > 3.5) score += 3
  else if (asset > 10000000 && product.maxRate2 > 3.0) score += 2
  
  // 소득별 점수
  if (income > 50000000 && product.maxRate2 > 3.8) score += 3
  else if (income > 30000000 && product.maxRate2 > 3.3) score += 2
  
  return score
}
  

  return {
    getDepositData, findCondition, getUserInput,
    findUser, signUpComplete, token, logoutUser,
    depositData, detailDepositData, findDepositDetail, getOptionDeposit,
    userProduct, nowUserProduct,userGetProduct, userInfo, getPreferences // loadUserProduct, getUserInfo, userSaveProducts, userDeleteProducts, 
    , addToPreference, removeFromPreference, updateUserProfile,
    recommendedProducts, getRecommendedProducts, clearUserInfo

  }
}, { persist: true }) 
