<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { aiApi } from '../api/ai'
import { useUserStore } from '../stores/user'
import { ChatDotRound, Loading, User, Position } from '@element-plus/icons-vue'

const userStore = useUserStore()

// AI状态
const aiStatus = ref({
  enabled: false,
  available: false,
  loading: true
})

// 聊天消息列表
const messages = ref([
  {
    id: 1,
    role: 'assistant',
    content: '您好！我是乡村旅游AI助手，可以为您解答关于乡村旅游、农产品和活动的各类问题。请问有什么可以帮到您的吗？',
    timestamp: new Date()
  }
])

// 用户输入
const userInput = ref('')

// 输入框引用
const inputRef = ref(null)

// 消息列表引用（用于自动滚动）
const messagesContainerRef = ref(null)

// 发送按钮加载状态
const sendingMessage = ref(false)

// 检查AI助手可用状态
const checkAIStatus = async () => {
  try {
    aiStatus.value.loading = true
    const response = await aiApi.getStatus()
    aiStatus.value = {
      ...response.data,
      loading: false
    }
    console.log('AI助手状态:', aiStatus.value)
  } catch (error) {
    console.error('获取AI助手状态失败:', error)
    aiStatus.value = {
      enabled: false,
      available: false,
      loading: false
    }
  }
}

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || sendingMessage.value) return
  
  const messageText = userInput.value.trim()
  userInput.value = ''
  
  // 添加用户消息到聊天列表
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: messageText,
    timestamp: new Date()
  })
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  // 显示思考状态
  sendingMessage.value = true
  messages.value.push({
    id: Date.now() + 1,
    role: 'assistant',
    content: '正在思考...',
    isThinking: true,
    timestamp: new Date()
  })
  
  try {
    // 调用AI API
    const response = await aiApi.sendMessage(messageText)
    
    // 移除思考消息
    messages.value = messages.value.filter(msg => !msg.isThinking)
    
    // 添加AI回复
    messages.value.push({
      id: Date.now() + 2,
      role: 'assistant',
      content: response.data.message,
      fallback: response.data.fallback,
      timestamp: new Date()
    })
  } catch (error) {
    console.error('发送消息失败:', error)
    
    // 移除思考消息
    messages.value = messages.value.filter(msg => !msg.isThinking)
    
    // 添加错误消息
    messages.value.push({
      id: Date.now() + 2,
      role: 'assistant',
      content: '很抱歉，我暂时无法回应您的问题。请稍后再试。',
      isError: true,
      timestamp: new Date()
    })
  } finally {
    sendingMessage.value = false
    
    // 滚动到底部
    await nextTick()
    scrollToBottom()
    
    // 聚焦输入框
    if (inputRef.value) {
      inputRef.value.focus()
    }
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainerRef.value) {
    messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 页面加载时
onMounted(() => {
  checkAIStatus()
  
  // 聚焦输入框
  if (inputRef.value) {
    inputRef.value.focus()
  }
  
  // 滚动到底部
  scrollToBottom()
})
</script>

<template>
  <div class="ai-assistant-page">
    <div class="ai-container">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <div class="chat-title">
          <el-icon class="header-icon"><ChatDotRound /></el-icon>
          <h1>乡村旅游AI助手</h1>
        </div>
        <div class="ai-status">
          <el-tag 
            :type="aiStatus.available ? 'success' : (aiStatus.loading ? 'info' : 'danger')" 
            size="small"
          >
            {{ aiStatus.loading ? '正在检查AI状态...' : 
               (aiStatus.available ? 'AI助手在线' : 'AI助手离线')
            }}
          </el-tag>
        </div>
      </div>
      
      <!-- 聊天消息区域 -->
      <div class="chat-messages" ref="messagesContainerRef">
        <div 
          v-for="message in messages" 
          :key="message.id" 
          :class="['message', message.role, { 'thinking': message.isThinking, 'error': message.isError, 'fallback': message.fallback }]"
        >
          <div class="message-avatar">
            <el-avatar 
              :size="36"
              :color="message.role === 'assistant' ? '#409EFF' : '#67C23A'"
            >
              <el-icon v-if="message.role === 'assistant'"><ChatDotRound /></el-icon>
              <el-icon v-else><User /></el-icon>
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-header">
              <span class="message-sender">{{ message.role === 'assistant' ? 'AI助手' : '我' }}</span>
              <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            </div>
            <div class="message-text">
              <p v-if="message.isThinking">
                <el-icon class="thinking-icon" :size="24"><Loading /></el-icon>
                {{ message.content }}
              </p>
              <p v-else>{{ message.content }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 聊天输入区域 -->
      <div class="chat-input">
        <el-input
          v-model="userInput"
          ref="inputRef"
          placeholder="输入您的问题..."
          :disabled="!aiStatus.available && !aiStatus.loading"
          @keyup.enter="sendMessage"
        >
          <template #append>
            <el-button
              type="primary"
              :disabled="!userInput.trim() || !aiStatus.available && !aiStatus.loading || sendingMessage"
              @click="sendMessage"
            >
              <el-icon v-if="sendingMessage"><Loading /></el-icon>
              <el-icon v-else><Position /></el-icon>
              {{ sendingMessage ? '发送中...' : '发送' }}
            </el-button>
          </template>
        </el-input>
        
        <div class="input-help">
          <p v-if="!aiStatus.available && !aiStatus.loading">
            AI助手当前不可用，请稍后再试。
          </p>
          <p v-else>
            您可以询问关于乡村旅游、农产品、活动预订、位置天气等问题。
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-assistant-page {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  min-height: calc(100vh - 200px);
}

.ai-container {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: 80vh;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

.chat-title {
  display: flex;
  align-items: center;
}

.header-icon {
  margin-right: 10px;
  font-size: 24px;
  color: #409EFF;
}

.chat-title h1 {
  font-size: 1.2rem;
  margin: 0;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f7fa;
}

.message {
  display: flex;
  margin-bottom: 20px;
}

.message-avatar {
  margin-right: 12px;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.message-sender {
  font-weight: bold;
}

.message-time {
  font-size: 0.8rem;
  color: #909399;
}

.message-text {
  padding: 10px 14px;
  border-radius: 8px;
  overflow-wrap: break-word;
  word-break: break-word;
}

.message.user .message-text {
  background-color: #ecf5ff;
  border: 1px solid #d9ecff;
}

.message.assistant .message-text {
  background-color: #f0f9eb;
  border: 1px solid #e1f3d8;
}

.message.thinking .message-text {
  background-color: #f4f4f5;
  border: 1px solid #e9e9eb;
  opacity: 0.8;
}

.message.error .message-text {
  background-color: #fef0f0;
  border: 1px solid #fbc4c4;
}

.message.fallback .message-text {
  background-color: #fdf6ec;
  border: 1px solid #faecd8;
}

.thinking-icon {
  animation: rotating 2s linear infinite;
  vertical-align: middle;
  margin-right: 5px;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #ebeef5;
}

.input-help {
  margin-top: 8px;
  font-size: 0.8rem;
  color: #909399;
  text-align: center;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .ai-assistant-page {
    padding: 10px;
  }
  
  .ai-container {
    height: calc(100vh - 120px);
  }
  
  .message-content {
    max-width: 90%;
  }
}
</style> 