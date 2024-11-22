<template>
  <v-jumbotron class="detailPage">
    <v-container fill-height>
      <v-layout align-center>
        <v-flex>
          <h3 class="display-3">Welcome to the site</h3>

          <span class="subheading">Lorem ipsum dolor sit amet, pri veniam forensibus id. Vis maluisset molestiae id, ad semper lobortis cum. At impetus detraxit incorrupte usu, repudiare assueverit ex eum, ne nam essent vocent admodum.</span>

          <v-divider class="my-3"></v-divider>

          <div class="title mb-3">Check out our newest features!</div>

          <v-btn
            class="mx-0"
            color="blue"
            large
          >
            장바구니 담기
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </v-jumbotron>
</template>

<script setup>
  //상세 페이지 => 내용 가져오기
  //store에 있는 내용들 담을 건데

</script>

<style scoped>
  .detailPage{
    margin-top: 300px !important;
  }
</style>