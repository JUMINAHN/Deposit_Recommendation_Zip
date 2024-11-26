<template>
  <div class="page-container">
    <!-- 뒤로가기 버튼을 상단에 배치 -->
    <div class="back-button-container">
      <button class="back-button" @click="router.go(-1)">
        ← 목록으로 돌아가기
      </button>
    </div>

    <div class="profile-container">
      <!-- 왼쪽 섹션 -->
      <div class="left-section">
        <!-- 프로필 이미지 및 기본 정보 -->
        <div class="profile-card">
          <div class="profile-image">
            <img src="@/assets/images/bankchar.jpg" alt="프로필 이미지">
          </div>
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
      </div>

      <!-- 오른쪽 섹션 -->
      <div class="right-section">
        <div class="tabs">
          <button 
            :class="['tab-button', { active: activeTab === 'posts' }]"
            @click="activeTab = 'posts'"
          >
            작성한 게시글
          </button>
          <button 
            :class="['tab-button', { active: activeTab === 'comments' }]"
            @click="activeTab = 'comments'"
          >
            작성한 댓글
          </button>
        </div>

        <!-- 게시글 목록 -->
        <div v-if="activeTab === 'posts'" class="content-section">
          <div v-for="article in userArticles" 
               :key="article.id" 
               class="article-item"
               @click="goToArticle(article.id)">
            <h4>{{ article.title }}</h4>
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
          </div>
        </div>

        <!-- 댓글 목록 -->
        <div v-else class="content-section">
          <div v-for="comment in userComments" 
               :key="comment.id" 
               class="comment-item">
            <p class="comment-content">{{ comment.content }}</p>
            <span class="article-date">{{ formatDate(comment.created_at) }}</span>
          </div>
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
  fetchUserComments()
})

// UserProfile.vue의 script에 추가
const goToArticle = (articleId) => {
  router.push({ 
    name: 'articleDetail', 
    params: { id: articleId } 
  })
}

// 탭 상태 관리
const activeTab = ref('posts')
const userComments = ref([])

// 댓글 목록 가져오기
const fetchUserComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/${route.params.username}/comments/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
    // 해당 사용자의 댓글만 필터링
    userComments.value = response.data.filter(comment => comment.user === route.params.username)
  } catch (error) {
    console.error('댓글 로드 실패:', error)
  }
}



</script>

<style scoped>
.profile-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 30px;
  max-width: 1200px;
  margin: 120px auto 40px; /* 상단 마진을 120px로 증가 */
  padding: 40px;
  background: linear-gradient(to bottom, #ffffff, #e6f0ff);
  position: relative; /* 상대 위치 설정 */
}


.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(110, 151, 246, 0.1);
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin: 0 auto 1.5rem;
  overflow: hidden;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  text-align: center;
}

.profile-info h2 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.follow-stats {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 1rem 0;
}

.follow-button {
  padding: 8px 24px;
  border-radius: 20px;
  border: none;
  background: #6e97f6;  /* 이미지의 파란색과 유사한 톤 */
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.follow-button.following {
  background: #e6f0ff;
  color: #6e97f6;
}

.right-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-bottom: 2px solid #e6f0ff;
}

.right-section h3 {
  color: #2c3e50;
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e6f0ff;
}

.article-item {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s ease;
}

.article-item:hover {
  background: #f0f7ff;
  transform: translateX(5px);
}

.article-item h4 {
  color: #2c3e50;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.article-date {
  color: #64748b;
  font-size: 0.9rem;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e6f0ff;
  padding-bottom: 0.5rem;
}

.tab-button {
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  color: #6e97f6;
  border-bottom: 2px solid #6e97f6;  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-button.active {
  color: #4f46e5;
  font-weight: 600;
  border-bottom: 2px solid #4f46e5;
}

.comment-item {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* .comment-item:hover {
  background: #f0f7ff;
  transform: translateX(5px);
} */

.comment-content {
  color: #2c3e50;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.back-button-container {
  margin-bottom: 20px;
}

.back-button {
  position: fixed; /* 고정 위치로 변경 */
  top: 100px; /* 네비게이션 바 아래로 위치 조정 */
  left: calc((100% - 1200px) / 2); /* 중앙 정렬 */
  padding: 8px 20px;
  background-color: white;
  color: #6e97f6;
  border: 1px solid #6e97f6;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  z-index: 100; /* 다른 요소들보다 위에 표시 */
}


.back-button:hover {
  background-color: rgb(63, 156, 232);
  color: white;
  transform: translateX(-5px);
}

.profile-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 30px;
  max-width: 1200px;
  margin: 120px auto 40px; /* 상단 여백 120px로 증가 */
  padding: 40px;
  background: linear-gradient(to bottom, #ffffff, #e6f0ff);
  position: relative; /* 상대 위치 설정 */
}


@media (max-width: 1200px) {
  .back-button {
    left: 20px; /* 화면이 작아질 때 왼쪽 여백 조정 */
  }
}

@media (max-width: 768px) {
  .profile-container {
    margin-top: 140px; /* 모바일에서 상단 여백 더 증가 */
    grid-template-columns: 1fr;
    padding: 20px;
  }
  
  .back-button {
    position: fixed;
    top: 80px;
    left: 20px;
    width: auto;
  }
}

</style>