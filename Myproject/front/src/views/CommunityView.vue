<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">게시판</h2>
    <div class="text-end mb-3">
      <RouterLink :to="{ name: 'article-create' }" class="btn btn-primary">
        새 글 작성
      </RouterLink>
    </div>
    <div v-if="loading" class="text-center">
      <p>로딩 중...</p>
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else-if="articles.length > 0" class="list-group">
      <div 
        class="list-group-item list-group-item-action"
        v-for="article in articles" 
        :key="article.id" 
        @click="goToArticle(article.id)">
        <h5>{{ article.title }}</h5>
        <p v-if="article.content">{{ article.content.substring(0, 100) }}...</p>
        <p v-else>내용 없음</p>
        <small class="text-muted">작성일: {{ formatDate(article.created_at) }}</small>
      </div>
    </div>
    <div v-else>
      <p>게시글이 없습니다. 새로 작성해보세요!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const articles = ref([])
const router = useRouter()
const loading = ref(false)
const error = ref(null)

const fetchArticles = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('http://127.0.0.1:8000/articles/')
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