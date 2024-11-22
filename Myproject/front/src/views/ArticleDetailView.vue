<template>
  <div class="container mt-5">
    <div v-if="article">
      <h2>{{ article.title }}</h2>
      <p>{{ article.content }}</p>
      <small class="text-muted">작성일: {{ new Date(article.created_at).toLocaleDateString() }}</small>

      <hr />
      <h4>댓글</h4>
      <div v-if="comments.length > 0" class="list-group mb-3">
        <div class="list-group-item" v-for="comment in comments" :key="comment.id">
          <p>{{ comment.content }}</p>
          <small class="text-muted">작성일: {{ new Date(comment.created_at).toLocaleDateString() }}</small>
        </div>
      </div>
      <div v-else>
        <p>댓글이 없습니다.</p>
      </div>

      <h5>댓글 추가</h5>
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
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

const route = useRoute();
const article = ref(null);
const comments = ref([]);
const newComment = ref('');

const fetchArticle = async () => {
  try {
    const response = await axios.get(`/articles/${route.params.id}/`);
    article.value = response.data;
  } catch (error) {
    console.error('게시글 로드 실패:', error);
  }
};

const fetchComments = async () => {
  try {
    const response = await axios.get(`/articles/${route.params.id}/comments/`);
    comments.value = response.data;
  } catch (error) {
    console.error('댓글 로드 실패:', error);
  }
};

const addComment = async () => {
  try {
    const response = await axios.post(`/articles/${route.params.id}/comments/`, {
      content: newComment.value,
    });
    comments.value.push(response.data);
    newComment.value = '';
  } catch (error) {
    console.error('댓글 작성 실패:', error);
  }
};

onMounted(() => {
  fetchArticle();
  fetchComments();
});
</script>
