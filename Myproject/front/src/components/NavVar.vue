<template>
<nav class="navbar navbar-expand-lg bg-body-tertiary justify-content-center">
  <div class="container-fluid">
    <img src="@/assets/images/logo.png" alt="Logo" width="40" height="34" class="d-inline-block align-text-top">
    <a class="navbar-brand" href="#">예적금 맛ZIP</a> 
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <RouterLink :to="{name : 'main'}" class="nav-link" >메인 페이지</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink :to="{name : 'recommend'}" class="nav-link" >예적금 추천</RouterLink>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">예적금 상품 비교</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">환율 검색</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">주변 은행 검색</a>
        </li>
        <li class="nav-item">
          <RouterLink :to="{name: 'community'}" class="nav-link">게시판</RouterLink>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">내가 지폐가 될 상인가?</a>
        </li>
        <li class="nav-item">
          <RouterLink :to="{name : 'login'}" class="nav-link" >로그인</RouterLink>
        </li>
      </ul>
    </div>
  </div>
</nav>

</template>

<script setup>
  import { RouterLink } from 'vue-router'


</script>

<style scoped>
  /*  */
  .navbar-nav {
  margin: 0 auto;
  }

.navbar-collapse {
  justify-content: center !important; 
  /* center로 넣는데 먼저 => important로 우선적으로 걸기 */
}
</style>