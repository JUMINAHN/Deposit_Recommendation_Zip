<template>
  <v-container justify="center" align="center">
    <v-form @submit.prevent>
      <v-card justify="flex-wrap">
        <v-container fluid>
          <v-row>
            <v-col cols="2"
            v-for="(find, index) in findCondition"
            :key="find.id">
              <v-combobox
                v-model="find.selectedValue"
                :items="find.content || []"
                :label="find.title"
              ></v-combobox>
              <!--                 :items="Array.isArray(find.content) ? find.content : []" -->
            </v-col>
          </v-row>
        </v-container>
        <v-btn
          class="mt-4"
          color="blue"
          block
        >
          나에게 맞는 상품 찾기 CLICK 💨
        </v-btn>
      </v-card>
    </v-form>


    <img src="@/assets/images/whatsInMyWeb.jpg" alt="" width="600px">

    <!--SEARCH 자체로 필터링을 하게 : 옆에 화면을 띄우려고 했는데 시행착오 多-->
    <div>
      <v-card
        title="예금 상품 추천"
        flat
      >
        <template v-slot:text>
          <v-text-field
            v-model="search"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
          ></v-text-field>
        </template>
  
        <!--dummy data받아옴-->
        <!--items가 항목 관련 된 내용을 받는 것-->
        <!--전체 데이터 -->
        <v-data-table
          :headers="headers"
          :items="items"
          :search="search"
        ></v-data-table>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { useBankStore } from '@/stores/bank'
import { computed, ref } from 'vue'
const store = useBankStore()

//selectValue를 ..? 흠
const findCondition = store.findCondition


//data table관련해서 
const dummyKey = ['순위', '6개월', '12개월', '세전이자', '세후이자', '금융기관', '상품', 'update']
const headers = dummyKey.map(item => ({
  title: item,
  key: item
}))
const items = computed(() => store.dummyData)
const search = ref('')


</script>

<style scoped>
  img {
    margin-top:30px;
  }
</style>