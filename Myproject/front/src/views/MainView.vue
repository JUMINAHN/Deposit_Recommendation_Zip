<template>
  <div class="main-container">
    <!-- 히어로 섹션 -->
    <div class="hero-section">
      <div class="titleInfo">
        <h1 class="headline">
          예적금 상품 비교 및 환율 정보 찾기가 어려운
        </h1>
        <h2 class="sub-headline">
          여러분을 위한 맞춤 서비스 예적금 
          <span class="highlight">"맛ZIP<span class="emoji">👩‍🍳</span>"</span>
        </h2>
      </div>
    </div>

    <!-- 카드 섹션 -->
    <v-container class="cards-section">
      <v-row justify="center" align="center">
        <v-col
          v-for="(card, index) in imgData"
          :key="card.id"
          cols="12"
          sm="6"
          md="4"
          class="pa-4"
        >
          <v-card
            class="service-card"
            max-width="400"
            elevation="3"
            hover
          >
            <v-img
              :src="card.src"
              height="220"
              cover
              class="align-end"
            >
              <div class="card-overlay">
                <v-card-title class="text-white">{{ card.title }}</v-card-title>
              </div>
            </v-img>

            <v-card-subtitle class="pt-4 text-primary font-weight-bold">
              {{ card.number }}
            </v-card-subtitle>

            <v-card-text class="text-body-1">
              {{ card.content }}
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-btn
                block
                color="blue"
                variant="elevated"
                @click.stop="handleCardClick(card)"
              >
                자세히 보기
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
   <div>
    <ChatBot />
  </div>
</template>

<script setup lang="ts">
import compare from '@/assets/images/compare.jpg'
import recommend from '@/assets/images/recommend.jpg'
import community from '@/assets/images/community.jpg'
import exchange from '@/assets/images/exchange.jpg'
import findBank from '@/assets/images/findBank.jpg'
import moneyFace from '@/assets/images/moneyFace.jpg'
import ChatBot from '@/components/ChatBot.vue'
import { RouterLink, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useBankStore } from '@/stores/bank'
import { Chart } from 'chart.js/auto'

// 인터페이스 정의
interface CardData {
  id: number;
  src: string;
  title: string;
  number: string;
  content: string;
  link?: string;
  requiresLogin: boolean;
}

const router = useRouter()
const store = useBankStore()
const isLoggedIn = ref(false)

onMounted(() => {
  isLoggedIn.value = !!store.token
})

// 데이터 정보 입력
let id = 1
const imgData = ref<CardData[]>([
  {id: id++, src: recommend, title: '예적금 추천', number: 'Number1', content: '나에게 맞는 상품을 찾아봐요 🫡', link: 'recommend', requiresLogin: false},
  {id: id++, src: compare, title: '예적금 상품 비교', number: 'Number2', content: '다양한 상품을 비교해봐요 😊', link: 'compared', requiresLogin: true},
  {id: id++, src: community, title: '게시판', number: 'Number3', content: '다른 사용자들은 무슨 생각을 할까 🧐', link: 'community', requiresLogin: true},
  {id: id++, src: findBank, title: '주변 은행 검색', number: 'Number4', content: '근처에 있는 은행을 찾아봐요 🏛️', link : 'map', requiresLogin: false},
  {id: id++, src: exchange, title: '환율 검색', number: 'Number5', content: '지금 우리나라 돈으로는 얼마일까? 💱', requiresLogin: false},
  {id: id++, src: moneyFace, title:'내가 지폐가 될 상인가', number: 'Number6', content: '나와 닮은 지폐를 찾아보고, 돈을 획득해요💲', requiresLogin: true},
])

const handleCardClick = (card: CardData) => {
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
// 팝업 상태 관리
const isGraphVisible = ref(false)
let chart: Chart | null = null

// 차트 생성 함수
const createChart = () => {
  const ctx = document.getElementById('interestChart') as HTMLCanvasElement
  if (ctx && imgData.length > 0) {
    if (chart) {
      chart.destroy()
    }
    
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: imgData.map(card => card.title),
        datasets: [
          {
            label: '기본금리 (%)',
            data: imgData.map(() => Math.random() * 5 + 1), // 예시 데이터
            backgroundColor: ['#90cdf4', '#63b3ed', '#4299e1', '#3182ce', '#2c5282'],
            borderColor: ['#63b3ed', '#4299e1', '#3182ce', '#2c5282', '#2a4365'],
            borderWidth: 1,
            order: 2
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: '금리 (%)',
              color: '#2d3748',
              font: {
                size: 14,
                weight: 'bold'
              }
            }
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              padding: 20,
              color: '#2d3748',
              font: {
                size: 14,
                weight: 'bold'
              }
            }
          }
        }
      }
    })
  }
}

const showGraph = () => {
  isGraphVisible.value = true
  setTimeout(createChart, 100)
}

const closeGraph = () => {
  isGraphVisible.value = false
  if (chart) {
    chart.destroy()
    chart = null
  }
}
</script>

<style scoped>
.main-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8fafc, #ffffff);
  padding-top: 80px; /* 네비게이션 바 높이만큼 상단 여백 추가 */
}

.hero-section {
  padding: 2rem 2rem; /* 상단 패딩 줄임 */
  text-align: center;
  background: linear-gradient(135deg, #e6f3ff 0%, #ffffff 100%);
  margin-bottom: 1rem;
}

.cards-section {
  padding: 1rem 0; /* 2rem에서 1rem으로 수정 */
}

.titleInfo {
  margin-top: 0; /* 상단 마진 제거 */
  margin-bottom: 20px;
  text-align: center;
}

.headline {
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 500;
  font-size: 2.2rem;
  color: #2d3748;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.sub-headline {
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  font-size: 2.5rem;
  color: #2d3748;
  line-height: 1.4;
}

.highlight {
  color: #4a90e2;
  position: relative;
  padding: 0 0.5rem;
}

.emoji {
  font-size: 2rem;
  vertical-align: middle;
  margin-left: 0.5rem;
}

.service-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1) !important;
}

.card-overlay {
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  padding: 1.5rem;
}

.v-card-subtitle {
  font-size: 1.1rem !important;
}

.v-card-text {
  font-size: 1rem !important;
  min-height: 80px;
}

@media (max-width: 600px) {
  .headline {
    font-size: 1.8rem;
  }
  
  .sub-headline {
    font-size: 2rem;
  }
}
</style>