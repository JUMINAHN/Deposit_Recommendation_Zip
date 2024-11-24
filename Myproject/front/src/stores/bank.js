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


  //(추후 점검 필요)
  const loadUserProduct = async function() { 
    try {
      console.log('loginUserName:', loginUserName.value); // 디버깅
      const response = await axios({
        method : 'get',
        url: `http://127.0.0.1:8000/app/accounts/profile/${loginUserName.value}/preference/`,
        headers : {
          Authorization: `Token ${token.value}`
        }
      })
      console.log(response)
      console.log(response.data)

      userProduct.value = response.data
      console.log(userProduct, '맞게 들어갔니?')
      console.log('사용자의 상품 로드 완료', userProduct.value)
    } catch (error) {
      console.log(error, 'error메세지')
      userProduct.value = [] //에러시 빈 배열 초기화
    }
  }

  //일단 한번 담아볼까?

 



  //유저가 장바구니에 삭제할 데이터
  const userDeleteProducts = async function(bankName, productName) { //이거 실행
    //동일하게 user에게 접근
    try {
      const response = await axios({
        method : 'delete',
        url : '`http://127.0.0.1:8000/app/accounts/preference/save/${bankName}/${productName}', //user Save관련 url
        headers: {
          Authorization: `Token ${token.value}` //토큰 관련 정보
        },
        data : {
          bankName, //은행명
          productName //은행상품명
        },
      }) 
      //response가 어떤식으로 받아오는지 확인 => 제품이 엇으니까 삭제가 안되겠지... 고로 현재 테스트 불가
      console.log(response, 'res')
      console.log(response.data, 'res.data')
    const index = userProduct.value.findIndex((item) => {
      return (item.bankName === bankName && item.productName === productName) 
    })
    if (index === -1) {//값이 없다면 => 삭제X => 삭제할 내용이 없음
      alert('삭제할 수 없는 상품입니다.')
    } else {
      userProduct.value.splice(index, 1) //상품 두개 묶음
      alert('관심 상품에서 제거되었습니다.')
      console.log('상품 보유 목록', userProduct)
    } 
  } catch (error) {

      console.log(error)
      alert('장바구니 상품을 삭제하는 과정에서 에러가 발생했습니다.')
    }
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




  //사용자에게 input 받은 값을 기반으로 조건 필터링
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

   //유저가 장바구니에 저장할 제품
  //token을 안보내줌 => get ifno쪽으로 위치 옮김
  const userSaveProducts = async function(bankName, productName) {
    try {
      if (!userInfo.value || !userInfo.value.username) {
        await getUserInfo();
      }
      const username = userInfo.value.username;
      const response = await axios({
        method: 'post',
        url: `http://127.0.0.1:8000/app/accounts/profile/${username}/preference/save/${bankName}/${productName}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      userProduct.value.push({
        'bankName': bankName,
        'productName': productName
      })
      alert('장바구니에 상품을 담았습니다!')
    } catch (error) {
      console.error("Error details:", error.response ? error.response.data : error.message);
      alert('장바구니 상품을 담는 과정에서 에러가 발생했습니다.');
    }
  }

  //이름을 클릭했을떄 파라미터
  //근데 로그인한 애들만 보내는거 아니잖아? 그냥 그 사람 정보 누르면 클릭 되어야 하는데 
  //별도 생성? 일단 로그인한 애만 받아와본다면?
  //내정보 받아오는데 401에러?
  const getUserInfo = async function() {
    try {
      if (!loginUserName.value) {
        console.error('loginUserName is not set');
        return null;
      }
      const response = await axios({
        method: 'get',
        url: `http://127.0.0.1:8000/app/accounts/profile/${loginUserName.value}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      userInfo.value = response.data;
      return userInfo.value;
    } catch(error) {
      console.log(error, 'error 발생!');
      throw error;
    }
  }//userInfo 정보 돌려줄 내용
      //store에서 userInfo 자체를 받아오려고 했으나 비동기 문제로 지연 발생
      //loadUserData가 있는데 굳이 nowUserProduct를 사용할 필요가 없을 듯? 데이터만 잘받아오면 문제 없음
      //nowUserProduct.value = userProduct.value //지금 유저가 가진 정보

    //더미
    // const products = ref([
    //   {
    //     id: 1,
    //     name: '마이드림적금',
    //     interestRate: 3.5,
    //     maxInterestRate: 4.5,
    //   },
    //   {
    //     id: 2,
    //     name: '청년희망적금',
    //     interestRate: 4.2,
    //     maxInterestRate: 5.2,
    //   },
    //   {
    //     id: 3,
    //     name: '디지털예금',
    //     interestRate: 3.8,
    //     maxInterestRate: 4.8,
    //   }
    // ])
    // nowUserProduct.value = products.value


  //   } catch(error) {
  //     console.log(error, 'error 발생!')
  //   }
  // }


  return {
    getDepositData, findCondition, getUserInput,
    findUser, signUpComplete, token, logoutUser,
    depositData, detailDepositData, findDepositDetail, getOptionDeposit,
    userSaveProducts, userDeleteProducts, userProduct,
    userGetProduct, loadUserProduct, getUserInfo, userInfo,
    nowUserProduct
  
  }
}, { persist: true }) 
