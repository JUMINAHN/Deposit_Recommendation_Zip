<template>
  <div class="container mt-5">
    <div v-if="article">
      <h1>작성자: {{ article.user }}</h1>
      <h2>제목: {{ article.title }}</h2>
      <p>내용: {{ article.content }}</p>
      <small class="text-muted">작성일: {{ formatDate(article.created_at) }}</small>
      <!-- 게시글 수정/삭제 버튼 -->
      <div v-if="article.user === currentUser.username">
        <button @click="editArticle" class="btn btn-warning mt-3">수정</button>
        <button @click="deleteArticle" class="btn btn-danger mt-3 ml-2">삭제</button>
      </div>
      <!-- 게시글 수정 폼 -->
      <div v-if="isEditing" class="mt-4">
        <h5>게시글 수정</h5>
        <form @submit.prevent="updateArticle">
          <div class="form-group">
            <label for="title">제목</label>
            <input type="text" id="title" v-model="updatedTitle" class="form-control" required />
          </div>
          <div class="form-group">
            <label for="content">내용</label>
            <textarea id="content" v-model="updatedContent" class="form-control" rows="5" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary mt-2">저장</button>
        </form>
        <button @click="cancelEdit" class="btn btn-secondary mt-2">취소</button>
      </div>
      <!-- 댓글 -->
      <hr />
      <h5>댓글</h5>
      <div v-if="comments.length > 0" class="list-group mb-3">
        <div class="list-group-item" v-for="comment in comments" :key="comment.id">
          <p>{{ comment.content }}</p>
          <small class="text-muted">
            작성자: {{ comment.user }} | 작성일: {{ formatDate(comment.created_at) }}
          </small>
          <!-- 댓글 수정/삭제 버튼 -->
          <div v-if="comment.user === currentUser.username" class="mt-2">
            <button @click="editComment(comment)" class="btn btn-warning btn-sm">수정</button>
            <button @click="deleteComment(comment.id)" class="btn btn-danger btn-sm ml-2">삭제</button>
          </div>
          <!-- 댓글 수정 폼 -->
          <div v-if="isEditingComment && editingCommentId === comment.id" class="mt-3">
            <form @submit.prevent="updateComment(comment.id)">
              <div class="form-group">
                <textarea v-model="updatedCommentContent" class="form-control" rows="3" required></textarea>
              </div>
              <button type="submit" class="btn btn-primary btn-sm mt-2">저장</button>
              <button @click="cancelEditComment" class="btn btn-secondary btn-sm mt-2 ml-2">취소</button>
            </form>
          </div>
        </div>
      </div>

      <div v-else>
        <p>댓글이 없습니다.</p>
      </div>

      <h5>댓글 쓰기</h5>
      <form @submit.prevent="addComment">
        <div class="form-group">
          <textarea 
            v-model="newComment" 
            class="form-control" 
            rows="3" 
            placeholder="댓글을 입력하세요."
            required>
          </textarea>
        </div>
        <button type="submit" class="btn btn-primary mt-2">댓글 작성</button>
      </form>
    </div>
    <div v-else>
      <p>게시글을 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useBankStore } from '@/stores/bank'

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
      headers : {
        'Authorization' : `Token ${bankStore.token}`
      }
    })
    article.value = response.data
    updatedTitle.value = article.value.title
    updatedContent.value = article.value.content
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
  await fetchCurrentUser() // 사용자 정보 로드
  fetchArticle()
  fetchComments()

})
</script>
