<template>
  <div class="board-container">
    <div class="board-header">
      <h2>금융상품 리뷰 게시판</h2>
      <RouterLink :to="{ name: 'article-create' }" class="write-button">
        새글쓰기
      </RouterLink>
    </div>

    <div v-if="loading" class="loading-wrapper">
      <div class="loading-spinner"></div>
    </div>
    
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else class="article-list">
  <div 
    v-for="article in articles" 
    :key="article.id" 
    @click="goToArticle(article.id)"
    class="article-item"
  >
    <div class="article-content">
      <h3 class="article-title">{{ article.title }}</h3>
      <p class="article-preview" v-if="article.content">
        {{ article.content.substring(0, 100) }}...
      </p>
    </div>
    <div class="article-meta">
      <span class="author" @click.stop="goToUserProfile(article.user)">{{ article.user }}</span>
      <span class="date">{{ formatDate(article.created_at) }}</span>
    </div>
  </div>

  <div v-if="articles.length === 0" class="no-articles">
    <p>첫 게시글의 주인공이 되어보세요!</p>
  </div>
  </div>
</div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useBankStore } from '@/stores/bank'

const store = useBankStore()
const articles = ref([])
const router = useRouter()
const loading = ref(false)
const error = ref(null)

//follow
const goToUserProfile = (username) => {
  router.push({ name: 'userProfile', params: { username } })
}

const fetchArticles = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('http://127.0.0.1:8000/articles/', {
      headers : {
        'Authorization' : `Token ${store.token}`
      }
    })
    articles.value = response.data
  } catch (err) {
    console.error('게시글 로드 실패:', err)
    error.value = '게시글을 불러오는 데 실패했습니다. 잠시 후 다시 시도해주세요.'
  } finally {
    loading.value = false
  }
}

const goToArticle = (id) => {
  router.push({ name: 'articleDetail', params: { id } })
}

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleDateString('ko-KR', options)
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.board-container {
  max-width: 1200px;
  margin: 120px auto 40px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.board-header h2 {
  color: #6e97f6;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.write-button {
  background-color: rgb(63, 156, 232);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
}

.write-button:hover {
  background-color: #6facd2;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(79, 70, 229, 0.3);
}

.article-list {
  background-color: #ffffff;
  border-radius: 12px;
}

.article-item {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.article-item:hover {
  background-color: #f8fafc;
  transform: translateX(6px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.article-title {
  font-size: 20px;
  color: #1e293b;
  font-weight: 600;
  margin-bottom: 12px;
  transition: color 0.2s ease;
}

.article-item:hover .article-title {
  color: #4f46e5;
}

.article-preview {
  color: #64748b;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 16px;
}

.article-meta {
  display: flex;
  gap: 24px;
  font-size: 14px;
  color: #94a3b8;
}

.author {
  display: flex;
  align-items: center;
  gap: 6px;
}

.author::before {
  content: '👤';
  font-size: 16px;
}

.date {
  display: flex;
  align-items: center;
  gap: 6px;
}

.date::before {
  content: '📅';
  font-size: 16px;
}

.loading-wrapper {
  text-align: center;
  padding: 60px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4f46e5;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

.error-message {
  background-color: #fef2f2;
  color: #dc2626;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  font-weight: 500;
  border: 1px solid #fee2e2;
}

.no-articles {
  text-align: center;
  padding: 60px;
  color: #64748b;
  font-size: 16px;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>