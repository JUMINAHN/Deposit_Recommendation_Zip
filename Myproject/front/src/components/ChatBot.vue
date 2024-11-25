<template>
  <div class="chatbot-container" :class="{ 'chatbot-open': isOpen }">
    <!-- 챗봇 토글 버튼 -->
    <button class="chatbot-toggle" @click="toggleChat">
      <span v-if="!isOpen">💬 나만의 금융 상담사와 대화하기</span>
      <span v-else>✕</span>
    </button>

    <!-- 챗봇 채팅창 -->
    <div v-if="isOpen" class="chatbot-window">
      <div class="chat-header">
        <h3>금융 상담 챗봇</h3>
      </div>
      
      <div class="chat-messages" ref="messageContainer">
        <div v-for="(message, index) in messages" 
             :key="index" 
             :class="['message', message.type]">
          <div class="message-content">{{ message.content }}</div>
        </div>
      </div>

      <div class="chat-input">
        <input 
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="질문을 입력하세요..."
          :disabled="loading"
        />
        <button @click="sendMessage" :disabled="loading">
          전송
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useBankStore } from '@/stores/bank'

const store = useBankStore()
const isOpen = ref(false)
const messages = ref([])
const userInput = ref('')
const loading = ref(false)
const messageContainer = ref(null)

// 초기 메시지
onMounted(() => {
  messages.value.push({
    type: 'bot',
    content: '안녕하세요! 금융 상품에 대해 어떤 것이 궁금하신가요? 먼저 당신의 연령대, 재무 정보, 선호하는 상품 등 기본 데이터를 입력해주세요!'
  })
})

// 메시지 자동 스크롤
watch(messages, () => {
  setTimeout(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  }, 100)
}, { deep: true })

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return

  const userMessage = userInput.value
  messages.value.push({
    type: 'user',
    content: userMessage
  })
  
  userInput.value = ''
  loading.value = true

  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/api/v1/chatbot/',
      { message: userMessage },
      {
        headers: {
          'Authorization': `Token ${store.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    
    if (response.data.error) {
      console.error('Chatbot error:', response.data.error)
      messages.value.push({
        type: 'bot',
        content: '죄송합니다. 오류가 발생했습니다: ' + response.data.error
      })
    } else {
      messages.value.push({
        type: 'bot',
        content: response.data.reply
      })
    }
  } catch (error) {
    console.error('Request error:', error)
    messages.value.push({
      type: 'bot',
      content: '죄송합니다. 서버 오류가 발생했습니다.'
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chatbot-toggle {
  background-color: rgb(63, 156, 232);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.chatbot-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.chatbot-window {
  position: absolute;
  bottom: 70px;
  right: 0;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 16px;
  background: rgb(63, 156, 232);
  color: white;
  border-radius: 16px 16px 0 0;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 12px;
  border-radius: 12px;
  margin-bottom: 8px;
}

.message.user {
  background: #e3f2fd;
  align-self: flex-end;
}

.message.bot {
  background: #f5f5f5;
  align-self: flex-start;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 8px;
}

.chat-input input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
}

.chat-input button {
  background: rgb(63, 156, 232);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.chat-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>