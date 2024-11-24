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
          v-if="store.userInfo?.username !== username"
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
import { ref, onMounted } from 'vue'
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

const fetchUserProfile = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/app/accounts/profile/${username.value}/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
    userInfo.value = response.data
  } catch (error) {
    console.error('프로필 로드 실패:', error)
  }
}

const fetchUserArticles = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/articles/', {
      headers: { Authorization: `Token ${store.token}` }
    })
    userArticles.value = response.data.filter(article => article.user === username.value)
  } catch (error) {
    console.error('게시글 로드 실패:', error)
  }
}

const toggleFollow = async () => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/app/accounts/${userInfo.value.id}/follow/`,
      {},
      { headers: { Authorization: `Token ${store.token}` } }
    )
    isFollowing.value = response.data.is_followed
    followers.value = response.data.followers
    followings.value = response.data.followings
  } catch (error) {
    console.error('팔로우 실패:', error)
  }
}

onMounted(() => {
  fetchUserProfile()
  fetchUserArticles()
})
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