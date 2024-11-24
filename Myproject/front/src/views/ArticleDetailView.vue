<template>
  <div class="board-container">
    <div class="back-button-container">
      <button @click="goBack" class="back-button">
        ← 목록으로 돌아가기
      </button>
    </div>

    <div v-if="article" class="article-detail">
      <!-- 게시글 헤더 -->
      <div class="article-header">
        <h2 class="article-title">{{ article.title }}</h2>
        <div class="article-meta">
          <div class="meta-left">
            <span class="author" @click.stop="goToUserProfile(article.user)">{{ article.user }}</span>
            <span class="date">{{ formatDate(article.created_at) }}</span>
          </div>
          <button 
            class="like-button" 
            @click.stop="toggleLike"
            :class="{ 'liked': isLiked }"
          >
            <span class="heart-emoji">{{ isLiked ? '❤️' : '🤍' }}</span>
            <span class="like-count">{{ likeCount }}</span>
          </button>
        </div>
      </div>
      <!-- 게시글 내용 -->
      <div class="article-content">
        <p>{{ article.content }}</p>
        <div class="like-section">
          <button 
            class="like-button" 
            @click="toggleLike"
            :class="{ 'liked': isLiked }"
          >
            <!-- <span class="heart-emoji">{{ isLiked ? '좋아요 ❤️' : '좋아요 취소 🤍' }}</span> -->
            <!-- <span class="like-count">{{ likeCount }}</span> -->
          </button>
        </div>
        </div>
      <!-- 게시글 수정/삭제 버튼 -->
      <div v-if="article.user === currentUser.username" class="action-buttons">
        <button @click="editArticle" class="edit-button">수정</button>
        <button @click="deleteArticle" class="delete-button">삭제</button>
      </div>

      <!-- 게시글 수정 폼 -->
      <div v-if="isEditing" class="edit-form">
        <h3>게시글 수정</h3>
        <form @submit.prevent="updateArticle">
          <div class="form-group">
            <label for="title">제목</label>
            <input type="text" id="title" v-model="updatedTitle" required />
          </div>
          <div class="form-group">
            <label for="content">내용</label>
            <textarea id="content" v-model="updatedContent" rows="5" required></textarea>
          </div>
          <div class="form-buttons">
          <button type="submit" class="action-button submit">저장</button>
          <button @click="cancelEdit" class="action-button cancel">취소</button>
        </div>
        </form>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h3>댓글</h3>
        
        <!-- 댓글 작성 폼 -->
        <div class="comment-form">
          <form @submit.prevent="addComment">
            <textarea 
              v-model="newComment" 
              rows="3" 
              placeholder="댓글을 입력하세요."
              required>
            </textarea>
            <button type="submit" class="submit-button">댓글 작성</button>
          </form>
        </div>

        <!-- 댓글 목록 -->
        <div v-if="comments.length > 0" class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-content">
              <p>{{ comment.content }}</p>
              <div class="comment-meta">
                <span class="author" @click="goToUserProfile(comment.user)">
                  👤 {{ comment.user }}
                </span>
                <span class="date">
                  📅 {{ formatDate(comment.created_at) }}
                </span>
              </div>
            </div>

            <!-- 댓글 수정/삭제 버튼 -->
            <div v-if="comment.user === currentUser.username" class="comment-actions">
              <button @click="editComment(comment)" class="edit-button-sm">수정</button>
              <button @click="deleteComment(comment.id)" class="delete-button-sm">삭제</button>
            </div>

            <!-- 댓글 수정 폼 -->
            <div v-if="isEditingComment && editingCommentId === comment.id" class="comment-edit-form">
              <form @submit.prevent="updateComment(comment.id)">
                <textarea v-model="updatedCommentContent" rows="3" required></textarea>
                <div class="form-buttons">
                  <button type="submit" class="submit-button-sm">저장</button>
                  <button @click="cancelEditComment" class="cancel-button-sm">취소</button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div v-else class="no-comments">
          <p>첫 댓글을 작성해보세요!</p>
        </div>
      </div>
    </div>

    <div v-else class="loading">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useBankStore } from '@/stores/bank'
const store = useBankStore()  // 이미 import된 useBankStore 사용



const isLiked = ref(false)
const likeCount = ref(0)
const toggleLike = async () => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/articles/${article.value.id}/like/`,
      {},
      { headers: { Authorization: `Token ${store.token}` } }
    )
    
    if (response.data) {
      isLiked.value = response.data.is_liked
      likeCount.value = response.data.likes_count
    }
  } catch (error) {
    console.error('좋아요 처리 실패:', error)
  }
}

const route = useRoute()
const router = useRouter()
const article = ref(null) // 무슨 게시글인지
const currentUser = ref(null) // 현재 사용자 정보 (로그인된 사용자)

const comments = ref([]) // 댓글들 조회하기 위한 변수
const newComment = ref('')

const bankStore = useBankStore()

const updatedTitle = ref('')
const updatedContent = ref('')

const isEditing = ref(false) // 게시글 수정하기위한 변수

const updatedCommentContent = ref('') // 댓글 수정 시 내용
const editingCommentId = ref(null) // 현재 수정 중인 댓글 ID
const isEditingComment = ref(false) // 댓글 수정 모드 여부

// ================================================
// 댓글 삭제
const deleteComment = async (commentId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/articles/comments/${commentId}/`, {
      headers: { Authorization: `Token ${bankStore.token}` },
    })
    comments.value = comments.value.filter((comment) => comment.id !== commentId)
    alert('댓글이 삭제되었습니다.')
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
  }
}

// 댓글 수정 시작
const editComment = (comment) => {
  isEditingComment.value = true
  editingCommentId.value = comment.id
  updatedCommentContent.value = comment.content
}

// 댓글 수정 취소
const cancelEditComment = () => {
  isEditingComment.value = false
  editingCommentId.value = null
  updatedCommentContent.value = ''
}

// 댓글 업데이트
const updateComment = async (commentId) => {
  try {
    const response = await axios.put(
      `http://127.0.0.1:8000/articles/comments/${commentId}/`,
      { content: updatedCommentContent.value },
      { headers: { Authorization: `Token ${bankStore.token}` } }
    )
    const updatedComment = response.data
    const commentIndex = comments.value.findIndex((comment) => comment.id === commentId)
    if (commentIndex !== -1) {
      comments.value[commentIndex] = updatedComment
    }
    isEditingComment.value = false
    editingCommentId.value = null
    updatedCommentContent.value = ''
    alert('댓글이 수정되었습니다.')
  } catch (error) {
    console.error('댓글 수정 실패:', error)
  }
}


// 댓글조회
const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/${route.params.id}/comments/`, {
      headers : {
        'Authorization' : `Token ${bankStore.token}`
      }
    })
    comments.value = response.data
  } catch (error) {
    console.error('댓글 로드 실패:', error)
  }
}

// 댓글 추가하기
const addComment = async () => {
  try {
    const response = await axios.post(`http://127.0.0.1:8000/articles/${route.params.id}/comments/create/`, 
    { content: newComment.value },
    { headers: { 'Authorization' : `Token ${bankStore.token}`} })
    comments.value.push(response.data)
    newComment.value = ''
    alert('댓글이 작성되었습니다.')
  } catch (error) {
    console.error('댓글 작성 실패:', error)
  }
}

// 게시글 조회
const fetchArticle = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/${route.params.id}/`, {
      headers: {
        'Authorization': `Token ${store.token}`
      }
    })
    article.value = response.data
    // 수정 폼을 위한 초기값 설정
    updatedTitle.value = article.value.title
    updatedContent.value = article.value.content
    // 좋아요 상태 초기화
    isLiked.value = response.data.is_liked
    likeCount.value = response.data.likes_count
  } catch (error) {
    console.error('게시글 로드 실패:', error)
  }
}

// 게시글 수정
const updateArticle = async () => {
  try {
    const response = await axios.put(`http://127.0.0.1:8000/articles/${route.params.id}/`, 
      { title: updatedTitle.value, content: updatedContent.value },
      { headers: { 'Authorization' : `Token ${bankStore.token}`} })
    article.value.title = updatedTitle.value
    article.value.content = updatedContent.value
    isEditing.value = false
    alert('게시글이 수정되었습니다.')
  } catch (error) {
    console.error('게시글 수정 실패:', error)
  }
}

// 게시글 삭제
const deleteArticle = async () => {
  try {
    await axios.delete(`http://127.0.0.1:8000/articles/${route.params.id}/`, {
      headers: { 'Authorization' : `Token ${bankStore.token}` }
    })
    alert('게시글이 삭제되었습니다.')
    router.push({ name: 'community'} ) // 게시글 삭제 후 목록 페이지로 리다이렉트
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
  }
}

// 게시글 수정 모드 활성화
const editArticle = () => {
  isEditing.value = true
}

// 게시글 수정 취소
const cancelEdit = () => {
  isEditing.value = false
}

// 댓글 작성일 포맷팅 함수
const formatDate = (dateString) => {
  const date = new Date(dateString)

  // 날짜 값이 유효한지 체크
  if (isNaN(date)) {
    console.warn('Invalid date:', dateString) // 디버깅을 위한 콘솔 로그
    return '유효하지 않은 날짜'
  }

  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 현재 사용자 정보 불러오기
const fetchCurrentUser = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/accounts/user/', {
      headers: {
        Authorization: `Token ${bankStore.token}`,
      },
    })
    currentUser.value = response.data
  } catch (error) {
    console.error('사용자 정보 불러오기 실패:', error)
  }
}

onMounted(async () => {
  if (route.params.id) {
    await fetchCurrentUser() // 사용자 정보 로드
    await fetchArticle() // 게시글 정보 로드
    await fetchComments() // 댓글 정보 로드
  }
})

const goBack = () => {
  router.go(-1)
}

const goToUserProfile = (username) => {
  router.push({ 
    name: 'userProfile', 
    params: { username } 
  })
}

</script>

<style scoped>
.board-container {
  max-width: 1200px;
  margin: 120px auto 40px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* 뒤로가기 버튼 */
.back-button {
  background-color: transparent;
  color: rgb(63, 156, 232);
  border: 2px solid rgb(63, 156, 232);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: rgb(63, 156, 232);
  color: white;
  transform: translateX(-5px);
}

/* 게시글 헤더 */
.article-header {
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.article-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 12px;
}

/* 메타 정보 (작성자, 날짜) */
.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  font-size: 14px;
  color: #94a3b8;
}

/* 게시글 내용 */
.article-content {
  margin: 20px 0;
  line-height: 1.6;
  font-size: 16px;
  color: #444;
}

/* 버튼 공통 스타일 */
.edit-button,
.delete-button,
.submit-button,
.cancel-button {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  margin: 0 6px;
}

/* 각 버튼별 스타일 */
.edit-button,
.submit-button {
  background-color: rgb(63, 156, 232);
  color: white;
}

.delete-button {
  background-color: #ef4444;
  color: white;
}

.cancel-button {
  background-color: #e5e7eb;
  color: #4b5563;
}

/* 버튼 호버 효과 */
.edit-button:hover,
.delete-button:hover,
.submit-button:hover,
.cancel-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 수정 폼 */
.edit-form {
  background-color: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  margin: 20px 0;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: rgb(63, 156, 232);
  box-shadow: 0 0 0 3px rgba(63, 156, 232, 0.1);
}

/* 댓글 섹션 */
.comments-section {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
}

.comments-section h3 {
  font-size: 18px;
  color: #374151;
  margin-bottom: 20px;
}

/* 댓글 작성 폼 */
.comment-form {
  margin-bottom: 30px;
}

.comment-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.comment-form textarea:focus {
  outline: none;
  border-color: rgb(63, 156, 232);
  box-shadow: 0 0 0 3px rgba(63, 156, 232, 0.1);
}

/* 댓글 목록 */
.comment-item {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.comment-content {
  font-size: 14px;
  color: #4b5563;
  margin-bottom: 8px;
}

.comment-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #6b7280;
}

/* 댓글 수정/삭제 버튼 */
.comment-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.edit-button-sm,
.delete-button-sm {
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 4px;
}

/* 로딩 스피너 */
.loading {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid rgb(63, 156, 232);
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 버튼 그룹 정렬 */
.action-buttons,
.form-buttons {
  display: flex;
  gap: 12px;
  margin: 16px 0;
}

/* 댓글 없음 메시지 */
.no-comments {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-size: 14px;
}

.article-meta .author,
.comment-meta .author {
  cursor: pointer;
  color: #6e97f6;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.article-meta .author:hover,
.comment-meta .author:hover {
  color: #4f46e5;
  transform: translateX(2px);
}

.comment-meta {
  display: flex;
  gap: 16px;
  align-items: center;
}

.like-section {
  margin: 20px 0;
  display: flex;
  align-items: center;
}

.like-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}


.heart-emoji {
  font-size: 16px;
  transition: transform 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
}

.like-button:hover .heart-emoji {
  transform: scale(1.3);
}

.like-count {
  font-size: 14px;
  color: #666;
}

.liked .heart-emoji {
  animation: heartBeat 0.3s ease;
}
.meta-left {
  display: flex;
  gap: 24px;
  align-items: center;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.4); }
  100% { transform: scale(1); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

</style>