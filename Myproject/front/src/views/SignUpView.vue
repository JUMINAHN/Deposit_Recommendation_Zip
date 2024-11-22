<template>
  <div class="topClass">
    <v-card
      class="mx-auto pa-12 pb-8"
      elevation="8"
      max-width="448"
      rounded="lg"
      title="User Registration 🤗"
    >
      <v-container>
        <v-text-field
          v-model.trim="name"
          color="primary"
          label="Name"
          variant="underlined"
        ></v-text-field>

        <v-text-field
          v-model.trim="email"
          color="primary"
          label="Email"
          variant="underlined"
        ></v-text-field>

        <v-text-field
          v-model.trim="password1"
          color="primary"
          label="Password1"
          placeholder="Enter your password"
          variant="underlined"
          type="password"
        ></v-text-field>

        <v-text-field
          v-model.trim="password2"
          color="primary"
          label="Password2"
          placeholder="Enter your password"
          variant="underlined"
          type="password"
        ></v-text-field>

        <v-checkbox
          v-model="terms"
          color="blue"
          label="I agree to site terms and conditions"
          @click.prevent="showTermsDialog"
        ></v-checkbox>
      </v-container>

      <!-- 약관 동의 다이얼로그 -->
      <v-dialog v-model="dialog" max-width="500">
        <v-card>
          <v-card-title class="text-h5">
            이용약관 동의
          </v-card-title>
          <v-card-text>
            <div class="terms-content">
              <h3>서비스 이용약관</h3>
              <p>1. 본 약관은 당사가 제공하는 모든 서비스의 이용조건 및 절차, 이용자와 당사의 권리, 의무, 책임사항을 규정합니다.</p>
              <p>2. 당사는 이용자의 개인정보를 보호하기 위해 최선을 다하며, 관련 법령을 준수합니다.</p>
              <p>3. 이용자는 관련 법령과 본 약관의 규정을 준수하여야 합니다.</p>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="rejectTerms">거절</v-btn>
            <v-btn color="primary" @click="acceptTerms">동의</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn 
          color="blue"
          @click.prevent="checkLogin(userData)"
          :disabled="!terms"
        >
          Complete Registration
          <v-icon icon="mdi-chevron-right" end></v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import { useBankStore } from '@/stores/bank'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const store = useBankStore()
const router = useRouter()
const dialog = ref(false)
const terms = ref(false)
const name = ref(null)
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const showTermsDialog = () => {
  dialog.value = true
}

const acceptTerms = () => {
  terms.value = true
  dialog.value = false
}

const rejectTerms = () => {
  terms.value = false
  dialog.value = false
}

const userData = {
  'name': name,
  'email': email,
  'password1': password1,
  'password2': password2,
}

// 기존 checkLogin 함수 유지
const checkLogin = function (userData) {

}
</script>

<style scoped>
.topClass {
  margin-top: 40px;
}

.terms-content {
  max-height: 300px;
  overflow-y: auto;
  padding: 16px;
}

.terms-content h3 {
  margin-bottom: 16px;
  font-weight: bold;
}

.terms-content p {
  margin-bottom: 12px;
  line-height: 1.6;
}
</style>