<template>
  <div class="board-container">
    <div class="back-button-container">
      <button @click="goBack" class="back-button">
        ← 목록으로 돌아가기
      </button>
    </div>
    <div class="board-header">
      <h2>새 글 작성</h2>
    </div>

    <div class="article-form">
      <form @submit.prevent="createArticle" class="form-content">
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            type="text" 
            id="title" 
            v-model="form.title" 
            placeholder="제목을 입력하세요" 
            required 
          />
        </div>
        
        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content" 
            v-model="form.content" 
            placeholder="내용을 입력하세요" 
            rows="10" 
            required
          ></textarea>
        </div>

        <div class="button-group">
          <button type="submit" class="submit-button">작성완료</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
// 기존 script 코드는 그대로 유지
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useBankStore } from '@/stores/bank'

const form = ref({
  title: '',
  content: '',
});

const router = useRouter()
const bankStore = useBankStore()

const createArticle = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/articles/', form.value, {
      headers : {
        'Authorization' : `Token ${bankStore.token}`
      }
    })
    console.log('게시글 작성 성공:', response.data)
    alert('게시글이 성공적으로 작성되었습니다!')
    console.log('Token:', bankStore.token);
    router.push({ name: 'community' })
  } catch (error) {
    console.error('게시글 작성 실패:', error)
    alert('게시글 작성에 실패했습니다.')
    console.log('Token:', bankStore.token);
  }
};

const goBack = () => {
  router.go(-1)
}

</script>

<style scoped>
.back-button-container {
  margin-bottom: 24px;
}

.back-button {
  background-color: transparent;
  color: rgb(63, 156, 232);
  border: 2px solid rgb(63, 156, 232);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: rgb(63, 156, 232);
  color: white;
  transform: translateX(-5px);
  box-shadow: 0 2px 4px rgba(63, 156, 232, 0.2);
}

.board-container {
  max-width: 1200px;
  margin: 120px auto 40px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.board-header {
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

.article-form {
  background-color: #ffffff;
  border-radius: 12px;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #1e293b;
  font-size: 16px;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #6e97f6;
  box-shadow: 0 0 0 3px rgba(110, 151, 246, 0.1);
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.submit-button {
  background-color: rgb(63, 156, 232);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background-color: #6facd2;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(79, 70, 229, 0.3);
}
</style>