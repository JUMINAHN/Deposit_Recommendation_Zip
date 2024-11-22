<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">새 글 작성</h2>
    <form @submit.prevent="createArticle" class="form-group">
      <div class="mb-3">
        <label for="title" class="form-label">제목</label>
        <input 
          type="text" 
          id="title" 
          v-model="form.title" 
          class="form-control" 
          placeholder="제목을 입력하세요" 
          required 
        />
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">내용</label>
        <textarea 
          id="content" 
          v-model="form.content" 
          class="form-control" 
          placeholder="내용을 입력하세요" 
          rows="5" 
          required
        ></textarea>
      </div>
      <div class="text-end">
        <button type="submit" class="btn btn-success">작성하기</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useBankStore } from '@/stores/bank'



// 폼 데이터
const form = ref({
  title: '',
  content: '',
});

// 라우터
const router = useRouter()

// 스토어 생성
const bankStore = useBankStore()

// 게시글 생성 요청
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


    router.push({ name: 'community' }) // 게시판 목록으로 이동
  } catch (error) {
    console.error('게시글 작성 실패:', error)
    alert('게시글 작성에 실패했습니다.')
    console.log('Token:', bankStore.token);

  }
};
</script>

<style scoped>
/* 추가적인 CSS는 필요에 따라 작성 */
</style>