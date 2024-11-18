<template>
  <div class="row container">
    <div 
    v-for="(data, index) in imgData"
    :key="data.id" class="cardHead col-sm-6 col-md-4">
      <div class="card" style="width: 18rem;">
        <img :src="data.src" class="card-img-top" alt="...">
        <div class="card-body">
          <h2 class="card-text">{{ data.text }}</h2>
        </div>
      </div>
  </div>
  </div>
</template>

<script setup>
// 다양한 방식으로 이름 지정 가능
import compare from '@/assets/images/compare.png'
import find from '@/assets/images/find.png'
import findBank from '@/assets/images/findBank.png'
import recommend from '@/assets/images/recommend.png'
import searchPeople from '@/assets/images/searchPeople.png'
 
let id = 1
  const imgData = [
    {id: id++, src: compare, text: '예적금 상품 비교'},
    {id: id++, src: find, text: '예적금 추천'},
    {id: id++, src: recommend, text: '환율 검색'},
    {id: id++, src: findBank, text: '주변 은행 검색'},
    {id: id++, src: searchPeople, text:'내가 지폐가 될 상인가'},
  ]

</script>

<style>
  h2 {
    text-align: center;
  }

  .container{
    margin-top : 40px !important; /*!important로 bootstrap보다 우선순위 부여 */
  }
</style>