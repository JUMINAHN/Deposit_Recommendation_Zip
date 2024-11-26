<template>
  <div class="main-container">
    <!-- 왼쪽 검색 패널 -->
    <div class="search-panel">
      <h2>은행 찾기</h2>
      <!-- 지역 선택 -->
      <div class="select-group">
        <label>광역시/도</label>
        <select v-model="selectedRegion" @change="updateDistricts" class="select-box">
          <option value="">선택하세요</option>
          <optgroup label="특별시/광역시">
            <option v-for="city in administrativeDistricts.metropolitan" :key="city.id" :value="city.id">
              {{ city.name }}
            </option>
          </optgroup>
          <optgroup label="도">
            <option v-for="province in administrativeDistricts.province" :key="province.id" :value="province.id">
              {{ province.name }}
            </option>
          </optgroup>
        </select>
      </div>
      <!-- 시/군/구 선택 부분 -->
      <div class="select-group">
        <label>시/군/구</label>
        <select v-model="selectedDistrict" class="select-box">
          <option value="">시/군/구 선택</option>
          <option v-for="district in districts" :key="district" :value="district">
            {{ district }}
          </option>
        </select>
      </div>
      <div class="select-group">
        <label>은행</label>
        <select v-model="selectedBank" class="select-box">
          <option value="">은행 선택</option>
          <option v-for="bank in banks" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>
      <button @click="searchNearbyBanks" class="search-button">
        검색하기
      </button>
      <!-- 검색 결과 리스트 -->
      <div class="search-results">
        <h3 class="results-title">검색 결과</h3>
        <ul id="placesList"></ul>
        <div id="pagination"></div>
      </div>
    </div>
    <!-- 오른쪽 지도 영역 -->
    <div class="map-container">
      <div id="map"></div>
    </div>

    <!-- 모달 열림 상태를 관리하는 변수 -->
    <v-dialog v-model="showModal" persistent max-width="400px">
      <!-- 모달 내부 카드 -->
      <v-card>
        <!-- 모달 헤더 -->
        <v-card-title>
          <span class="text-h6">알림</span>
        </v-card-title>
        <!-- 모달 본문 -->
        <v-card-text>
          지도에 대한 정보를 불러오는데 실패했습니다.<br />
          잠시 후 다시 시도해주세요.
        </v-card-text>
        <!-- 모달 푸터 -->
        <v-card-actions>
          <v-btn color="primary" text @click="showModal = false, router.push({ name: 'main' })">
            닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const apiKey = import.meta.env.VITE_KAKAO_API_KEY
// 변수 선언 부분 수정
const selectedRegion = ref('')
const selectedDistrict = ref('') // selectedCity 대신 selectedDistrict로 통일
const selectedBank = ref('')
const districts = ref([]) // cities 대신 districts로 통일
const router = useRouter()
const showModal = ref(false) // 모달 표시 여부


// 11/24-오전 11시 : ps오류
let map, ps, infowindow, markers = []

// 지도 초기화 함수
const initMap = () => {
  const mapContainer = document.getElementById('map')
  const mapOption = {
    center: new kakao.maps.LatLng(37.566826, 126.9786567),
    level: 3
  }

  map = new kakao.maps.Map(mapContainer, mapOption)
  ps = new kakao.maps.services.Places()
  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
}


// 시/군/구 목록 업데이트 함수

const updateDistricts = () => {
  console.log('Selected Region:', selectedRegion.value) // 디버깅용
  if (selectedRegion.value) {
    const regionData = districtData[selectedRegion.value]
    if (regionData) {
      districts.value = regionData.districts
      console.log('Updated Districts:', districts.value) // 디버깅용
    } else {
      districts.value = []
    }
  } else {
    districts.value = []
  }
  // 시/군/구 선택값 초기화
  selectedDistrict.value = ''
}

// 근처 은행 검색 함수
// searchNearbyBanks 함수도 수정
const searchNearbyBanks = () => {
  if (!selectedRegion.value || !selectedDistrict.value) {
    alert('지역을 선택해주세요!')
    return
  }
  if (!selectedBank.value) {
    alert('은행을 선택해주세요!')
    return
  }

  const regionName = districtData[selectedRegion.value].name
  const keyword = `${regionName} ${selectedDistrict.value} ${selectedBank.value}`
  ps.keywordSearch(keyword, placesSearchCB)
}

// 검색 결과 콜백 함수
const placesSearchCB = (data, status, pagination) => {
  if (status === kakao.maps.services.Status.OK) {
    displayPlaces(data);
    displayPagination(pagination);
  } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
    alert('검색 결과가 존재하지 않습니다.');
  } else if (status === kakao.maps.services.Status.ERROR) {
    alert('검색 결과 중 오류가 발생했습니다.');
  }
}

// 검색 결과 표시 함수
const displayPlaces = (places) => {
  const listEl = document.getElementById('placesList')
  const menuEl = document.getElementById('menu_wrap')
  const fragment = document.createDocumentFragment()
  const bounds = new kakao.maps.LatLngBounds()

  removeAllChildNods(listEl)
  removeMarker()

  for (let i = 0; i < places.length; i++) {
    const placePosition = new kakao.maps.LatLng(places[i].y, places[i].x)
    const marker = addMarker(placePosition, i)
    const itemEl = getListItem(i, places[i])

    bounds.extend(placePosition);

    (function (marker, title) {
      kakao.maps.event.addListener(marker, 'mouseover', function () {
        displayInfowindow(marker, title)
      });

      kakao.maps.event.addListener(marker, 'mouseout', function () {
        infowindow.close()
      });

      itemEl.onmouseover = function () {
        displayInfowindow(marker, title)
      };

      itemEl.onmouseout = function () {
        infowindow.close()
      };
    })(marker, places[i].place_name)

    fragment.appendChild(itemEl)
  }

  listEl.appendChild(fragment)

  map.setBounds(bounds)
}

// 검색 결과 항목 생성 함수
// getListItem 함수 수정
const getListItem = (index, place) => {
  const el = document.createElement('li')
  let itemStr = `
    <div class="item-container">
      <div class="item-header">
        <span class="item-number">${index + 1}</span>
        <h5 class="item-title">${place.place_name}</h5>
      </div>
      <div class="item-body">
        <table class="item-table">
          <tbody>
            <tr>
              <td class="label">주소</td>
              <td>${place.road_address_name || place.address_name}</td>
            </tr>
            ${place.phone ? `
            <tr>
              <td class="label">연락처</td>
              <td>${place.phone}</td>
            </tr>
            ` : ''}
          </tbody>
        </table>
      </div>
    </div>
  `.trim(); // 불필요한 공백 제거

  el.innerHTML = itemStr
  el.className = 'item'

  // 클릭 이벤트 추가 및 활성화 스타일 처리
  el.addEventListener('click', () => {
    // 기존 활성화된 항목의 스타일 제거
    const items = document.querySelectorAll('.item')
    items.forEach(item => item.classList.remove('active'))

    // 현재 항목 활성화
    el.classList.add('active')

    // 기존 마커 모두 제거
    removeMarker()

    // 클릭한 장소에 대한 마커 생성
    const marker = addMarker(new kakao.maps.LatLng(place.y, place.x), index)

    // 지도 중심 이동 (부드러운 이동 효과 추가)
    map.panTo(new kakao.maps.LatLng(place.y, place.x))

    // 인포윈도우 표시
    displayInfowindow(marker, place.place_name)
  })

  return el
}

// 마커 생성 함수
const addMarker = (position, idx) => {
  const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png'
  const imageSize = new kakao.maps.Size(36, 37)
  const imgOptions = {
    spriteSize: new kakao.maps.Size(36, 691),
    spriteOrigin: new kakao.maps.Point(0, (idx * 46) + 10),
    offset: new kakao.maps.Point(13, 37)
  };
  const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);
  const marker = new kakao.maps.Marker({
    position: position,
    image: markerImage
  })

  marker.setMap(map)
  markers.push(marker)

  return marker
}

// 마커 제거 함수
const removeMarker = () => {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null)
  }
  markers = []
}

// 페이지네이션 표시 함수
const displayPagination = (pagination) => {
  const paginationEl = document.getElementById('pagination')
  const fragment = document.createDocumentFragment()

  while (paginationEl.hasChildNodes()) {
    paginationEl.removeChild(paginationEl.lastChild)
  }

  for (let i = 1; i <= pagination.last; i++) {
    const el = document.createElement('a')
    el.href = "#"
    el.innerHTML = i

    if (i === pagination.current) {
      el.className = 'on'
    } else {
      el.onclick = (function (i) {
        return function () {
          pagination.gotoPage(i)
        }
      })(i)
    }

    fragment.appendChild(el)
  }
  paginationEl.appendChild(fragment)
}

// 인포윈도우 표시 함수
const displayInfowindow = (marker, title) => {
  const content = `<div style="padding:5px;z-index:1;">${title}</div>`
  infowindow.setContent(content)
  infowindow.open(map, marker)
}

// 요소의 모든 자식 노드 제거 함수
const removeAllChildNods = (el) => {
  while (el.hasChildNodes()) {
    el.removeChild(el.lastChild)
  }
}

// 컴포넌트 마운트 시 실행되는 함수
onMounted(() => {
  const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services&autoload=false`
    script.async = true
    script.onload = () => {
      window.kakao.maps.load(initMap)
    }
    script.onerror = () => {
    console.error('카카오 맵 API 로드 실패')
    showModal.value = true
  }
    document.head.appendChild(script)

})

const administrativeDistricts = {
  metropolitan: [
    { id: 'seoul', name: '서울특별시' },
    { id: 'busan', name: '부산광역시' },
    { id: 'daegu', name: '대구광역시' },
    { id: 'incheon', name: '인천광역시' },
    { id: 'gwangju', name: '광주광역시' },
    { id: 'daejeon', name: '대전광역시' },
    { id: 'ulsan', name: '울산광역시' },
    { id: 'sejong', name: '세종특별자치시' }
  ],
  province: [
    { id: 'gyeonggi', name: '경기도' },
    { id: 'gangwon', name: '강원특별자치도' },
    { id: 'chungbuk', name: '충청북도' },
    { id: 'chungnam', name: '충청남도' },
    { id: 'jeonbuk', name: '전북특별자치도' },
    { id: 'jeonnam', name: '전라남도' },
    { id: 'gyeongbuk', name: '경상북도' },
    { id: 'gyeongnam', name: '경상남도' },
    { id: 'jeju', name: '제주특별자치도' }
  ]
};

// 은행 목록 데이터 추가
const banks = ref([
  'KB국민은행',
  '신한은행',
  '우리은행',
  '하나은행',
  'NH농협은행',
  'IBK기업은행',
  'SC제일은행',
  '씨티은행',
  'KDB산업은행',
  '케이뱅크',
  '카카오뱅크',
  '토스뱅크'
])


const districtData = {
  seoul: {
    name: '서울특별시',
    districts: ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']
  },
  busan: {
    name: '부산광역시',
    districts: ['중구', '서구', '동구', '영도구', '부산진구', '동래구', '남구', '북구', '강서구', '해운대구', '사하구', '금정구', '연제구', '수영구', '사상구', '기장군']
  },
  daegu: {
    name: '대구광역시',
    districts: ['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군', '군위군']
  },
  incheon: {
    name: '인천광역시',
    districts: ['중구', '동구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서구', '강화군', '옹진군']
  },
  gwangju: {
    name: '광주광역시',
    districts: ['동구', '서구', '남구', '북구', '광산구']
  },
  daejeon: {
    name: '대전광역시',
    districts: ['중구', '서구', '동구', '유성구', '대덕구']
  },
  ulsan: {
    name: '울산광역시',
    districts: ['중구', '남구', '동구', '북구', '울주군']
  },
  sejong: {
    name: '세종특별자치시',
    districts: ['조치원읍', '연기면', '연동면', '부강면', '금남면', '장군면', '연서면', '전의면', '전동면', '소정면', '한솔동', '새롬동', '나성동', '다정동', '도담동', '어진동', '해밀동', '아름동', '종촌동', '고운동', '보람동', '대평동', '소담동', '반곡동']
  },
  gyeonggi: {
    name: '경기도',
    districts: ['수원시 장안구', '수원시 권선구', '수원시 팔달구', '수원시 영통구', '성남시 수정구', '성남시 중원구', '성남시 분당구', '의정부시', '안양시 만안구', '안양시 동안구', '부천시 원미구', '부천시 소사구', '부천시 오정구', '광명시', '동두천시', '평택시', '안산시 상록구', '안산시 단원구', '고양시 덕양구', '고양시 일산동구', '고양시 일산서구', '과천시', '구리시', '남양주시', '오산시', '시흥시', '군포시', '의왕시', '하남시', '용인시 처인구', '용인시 기흥구', '용인시 수지구', '파주시', '이천시', '안성시', '김포시', '화성시', '광주시', '양주시', '포천시', '여주시', '연천군', '가평군', '양평군']
  },
  gangwon: {
    name: '강원특별자치도',
    districts: ['춘천시', '원주시', '강릉시', '동해시', '태백시', '속초시', '삼척시', '홍천군', '횡성군', '영월군', '평창군', '정선군', '철원군', '화천군', '양구군', '인제군', '고성군', '양양군']
  },
  chungbuk: {
    name: '충청북도',
    districts: ['청주시 상당구', '청주시 흥덕구', '청주시 서원구', '청주시 청원구', '충주시', '제천시', '보은군', '옥천군', '영동군', '증평군', '진천군', '괴산군', '음성군', '단양군']
  },
  chungnam: {
    name: '충청남도',
    districts: ['천안시 동남구', '천안시 서북구', '공주시', '보령시', '아산시', '서산시', '논산시', '계룡시', '당진시', '금산군', '부여군', '서천군', '청양군', '홍성군', '예산군', '태안군']
  },
  jeonbuk: {
    name: '전북특별자치도',
    districts: ['전주시 완산구', '전주시 덕진구', '군산시', '익산시', '정읍시', '남원시', '김제시', '완주군', '진안군', '무주군', '장수군', '임실군', '순창군', '고창군', '부안군']
  },
  jeonnam: {
    name: '전라남도',
    districts: ['목포시', '여수시', '순천시', '나주시', '광양시', '담양군', '곡성군', '구례군', '고흥군', '보성군', '화순군', '장흥군', '강진군', '해남군', '영암군', '무안군', '함평군', '영광군', '장성군', '완도군', '진도군', '신안군']
  },
  gyeongbuk: {
    name: '경상북도',
    districts: ['포항시 남구', '포항시 북구', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시', '상주시', '문경시', '경산시', '의성군', '청송군', '영양군', '영덕군', '청도군', '고령군', '성주군', '칠곡군', '예천군', '봉화군', '울진군', '울릉군']
  },
  gyeongnam: {
    name: '경상남도',
    districts: ['창원시 의창구', '창원시 성산구', '창원시 진해구', '창원시 마산합포구', '창원시 마산회원구', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시', '양산시', '의령군', '함안군', '창녕군', '고성군', '남해군', '하동군', '산청군', '함양군', '거창군', '합천군']
  },
  jeju: {
    name: '제주특별자치도',
    districts: ['제주시', '서귀포시']
  }
}
</script>


<style scoped>
.main-container {
  padding-top: 80px;
  /* 네비게이션 바 높이 + 여유 공간 */
  display: flex;
  height: 100vh;
  background-color: #f5f7fa;
}

.search-panel {
  width: 400px;
  padding: 20px;
  background-color: white;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.search-panel h2 {
  color: #2c5282;
  margin-bottom: 30px;
  font-size: 24px;
}

.select-group {
  margin-bottom: 20px;
}

.select-group label {
  display: block;
  margin-bottom: 8px;
  color: #4a5568;
  font-weight: 500;
}

.select-box {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
  color: #2d3748;
}

.search-button {
  width: 100%;
  padding: 12px;
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-button:hover {
  background-color: #3182ce;
}

.search-results {
  margin-top: 20px;
  height: calc(100vh - 400px);
  overflow-y: auto;
}

.map-container {
  flex: 1;
  padding: 20px;
}

#map {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 검색 결과 스타일 수정 */
#placesList {
  list-style: none;
  padding: 0;
}

#placesList .item {
  padding: 15px;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
}

#placesList .item:hover {
  background-color: #ebf8ff;
}

#pagination {
  margin-top: 20px;
  text-align: center;
}

#pagination a {
  display: inline-block;
  padding: 8px 12px;
  margin: 0 4px;
  border-radius: 4px;
  color: #4a5568;
  text-decoration: none;
}

#pagination .on {
  background-color: #4299e1;
  color: white;
}

/* 검색 결과 스타일 수정 */
.item-container {
  padding: 15px;
  border-radius: 8px;
  background-color: white;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.item-number {
  width: 24px;
  height: 24px;
  background-color: #4299e1;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  font-size: 12px;
}

.item-title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  color: #2d3748;
}

.item-table {
  width: 100%;
  border-collapse: collapse;
}

.item-table tr {
  border-bottom: 1px solid #e2e8f0;
}

.item-table tr:last-child {
  border-bottom: none;
}

.item-table td {
  padding: 8px 0;
  font-size: 14px;
}

.item-table .label {
  color: #718096;
  width: 80px;
}

.search-results {
  background-color: #f8fafc;
  padding: 15px;
  border-radius: 8px;
}

#placesList .item {
  transition: transform 0.2s;
  cursor: pointer;
}

#placesList .item:hover {
  transform: translateY(-2px);
  background-color: #f7fafc;
}
</style>