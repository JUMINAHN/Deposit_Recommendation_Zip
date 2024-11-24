<template>
  <div class="profile-container">
    <!-- 왼쪽 섹션 -->
    <div class="left-section">
      <div class="profile-info">
        <h2>{{ userInfo.nickname || userInfo.username }}</h2>
        <div class="follow-stats">
          <span>팔로워 {{ followers.length }}</span>
          <span>팔로잉 {{ followings.length }}</span>
        </div>
        <button 
        v-if="store.userInfo?.username !== route.params.username"
          @click="toggleFollow" 
          :class="['follow-button', { 'following': isFollowing }]"
        >
          {{ isFollowing ? '팔로잉' : '팔로우' }}
        </button>
      </div>
    </div>

    <!-- 오른쪽 섹션 -->
    <div class="right-section">
      <h3>작성한 게시글</h3>
      <div class="user-articles">
        <div v-for="article in userArticles" 
             :key="article.id" 
             class="article-item"
             @click="goToArticle(article.id)">
          <h4>{{ article.title }}</h4>
          <span class="article-date">{{ formatDate(article.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBankStore } from '@/stores/bank'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useBankStore()
const username = ref(route.params.username)
const userInfo = ref({})
const userArticles = ref([])
const followers = ref([])
const followings = ref([])
const isFollowing = ref(false)

// formatDate 함수 추가
const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit' 
  }
  return new Date(dateString).toLocaleDateString('ko-KR', options)
}

// UserProfile.vue의 script 부분에 추가
const fetchUserProfile = async () => {
  try {
    // route.params.username을 사용하여 클릭한 사용자의 정보를 가져옴
    const response = await axios.get(`http://127.0.0.1:8000/app/accounts/profile/${route.params.username}/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
    userInfo.value = response.data
    
    // 팔로워/팔로잉 정보도 해당 사용자의 것을 가져옴
    followers.value = response.data.followers || []
    followings.value = response.data.followings || []
    
    // 현재 로그인한 사용자가 이 프로필의 사용자를 팔로우하고 있는지 확인
    isFollowing.value = followers.value.includes(store.userInfo?.username)
  } catch (error) {
    console.error('프로필 로드 실패:', error)
  }
}


// watch를 추가하여 라우트 파라미터 변경 감지
watch(() => route.params.username, (newUsername) => {
  if (newUsername) {
    fetchUserProfile()
    fetchUserArticles()
  }
})

const fetchUserArticles = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/articles/', {
      headers: { Authorization: `Token ${store.token}` }
    })
    // route.params.username을 사용하여 해당 사용자의 게시글만 필터링
    userArticles.value = response.data.filter(article => article.user === route.params.username)
  } catch (error) {
    console.error('게시글 로드 실패:', error)
  }
}

const toggleFollow = async () => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/app/accounts/accounts/${route.params.username}/follow/`,
      {},
      { headers: { Authorization: `Token ${store.token}` } }
    )
    
    if (response.data) {
      isFollowing.value = response.data.is_followed
      followers.value = response.data.followers
      followings.value = response.data.followings
    }
  } catch (error) {
    console.error('팔로우 실패:', error)
    alert(error.response?.data?.message || '팔로우 처리 중 오류가 발생했습니다.')
  }
}

onMounted(() => {
  fetchUserProfile()
  fetchUserArticles()
})

// UserProfile.vue의 script에 추가
const goToArticle = (articleId) => {
  router.push({ 
    name: 'articleDetail', 
    params: { id: articleId } 
  })
}

</script>

<style scoped>
.profile-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 30px;
  max-width: 1200px;
  margin: 120px auto 40px;
  padding: 30px;
}

.left-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.right-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.follow-button {
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  background: #4f46e5;
  color: white;
  cursor: pointer;
}

.follow-button.following {
  background: #e5e7eb;
  color: #374151;
}

.article-item {
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
}

.article-item:hover {
  background: #f9fafb;
}
</style>