<template>
  <div class="titleInfo">
    <h1 class="font-weight-medium">
      예적금 상품 비교 및 환율 정보 찾기가 어려운
    </h1>
    <h2 class="font-weight-medium">
      여러분을 위한 맞춤 서비스 예적금 <span class="font-weight-bold appName">"맛ZIP👩‍🍳"</span>
    </h2>
  </div>

  <v-container> 
    <v-row justify="center" align="center"> <!--justify, align : centner-->
    <v-col
      v-for="(card, index) in imgData"
      :key="card.id"
        cols="12" 
        sm="6"     
        md="4"  
        class="pa-4">
        <!--pa는 padding -->
        <!-- 모바일에서는 한 줄에 하나 cols -->
        <!-- 태블릿에서는 한 줄에 둘 sm -->
        <!-- 데스크탑에서는 한 줄에 셋 md -->
        <v-card
        class="mx-auto"
        max-width="400"
        elevation="2"
        hover
      >
      <!--elevation == 그림자 효과 추가-->
      
      
        <v-img 
          class="align-end text-white" 
          height="200"
          :src="card.src"
          cover
        >
        <!--카드 제목 배경 추가-->
          <v-card-title class="text-white bg-black bg-opacity-50">{{ card.title }}</v-card-title>
        </v-img>
    
        <v-card-subtitle class="pt-4">
          {{ card.number }}
        </v-card-subtitle>
    
        <v-card-text>
          <div>{{ card.content }}</div>
    
        </v-card-text>
    
        <v-card-actions>
          <v-btn variant="text" color="primary" text="EXPLORE" @click.stop="handleCardClick(card)"></v-btn>
        </v-card-actions>
      </v-card> 
    </v-col>
    </v-row>
  </v-container>
</template>


<script setup >
// asset 이미지 호출
import compare from '@/assets/images/compare.jpg'
import recommend from '@/assets/images/recommend.jpg'
import exchange from '@/assets/images/exchange.jpg'
import findBank from '@/assets/images/findBank.jpg'
import moneyFace from '@/assets/images/moneyFace.jpg'
import { RouterLink, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useBankStore } from '@/stores/bank'
onMounted
const router = useRouter()
const store = useBankStore()
const isLoggedIn = ref(false)
onMounted(() => {
  isLoggedIn.value = !!store.token
})

//데이터 정보 입력
let id = 1
//loginrequried 데이터 추가
const imgData = [
  {id: id++, src: recommend, title: '예적금 추천', number: 'Number1', content: '나에게 맞는 상품을 찾아봐요 🫡', link: 'recommend', requiresLogin: false},
  {id: id++, src: compare, title: '예적금 상품 비교', number: 'Number2', content: '다양한 상품을 비교해봐요 😊', link: 'compared', requiresLogin: true},
  {id: id++, src: exchange, title: '환율 검색', number: 'Number3', content: '지금 우리나라 돈으로는 얼마일까? 💱', requiresLogin: false},
  {id: id++, src: findBank, title: '주변 은행 검색', number: 'Number4', content: '근처에 있는 은행을 찾아봐요 🏛️', requiresLogin: false},
  {id: id++, src: moneyFace, title:'내가 지폐가 될 상인가', number: 'Number5', content: '나와 닮은 지폐를 찾아보고, 돈을 획득해요💲', requiresLogin: false},
]

const handleCardClick = (card) => {
  if (card.requiresLogin && !isLoggedIn.value) {
    alert('로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
  } else {
    if (card.link) {
      router.push({ name: card.link })
    } else {
      console.log(`${card.title} 기능은 아직 구현되지 않았습니다.`)
    }
  }
}
</script>


<style scoped>
.titleInfo {
  margin-top: 30px;
  margin-bottom : 20px;
  text-align: center;
}

h1, h2 {
  font-family: 'Noto Sans KR', sans-serif !important;
  font-weight: 700;
  font-size: 2rem;
  color: #1f1f21;
  letter-spacing: -0.02em; 
}

.appName {
  color:red
}

/* 추가할 스타일 */
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-5px); /* 호버 시 약간 위로 올라가는 효과 */
}

/* 이미지 밝기 조절 */
.v-img {
  filter: brightness(0.9);
}

/* 카드 간격 조절 */
.v-col {
  display: flex;
  justify-content: center;
}
</style>