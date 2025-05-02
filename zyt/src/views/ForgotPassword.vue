<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const resetPassword = async () => {
  if (!email.value) {
    message.value = '请输入您的注册邮箱'
    messageType.value = 'error'
    return
  }
  
  loading.value = true
  message.value = ''
  
  try {
    // 这里可以添加实际的密码重置API调用
    // const response = await userApi.forgotPassword(email.value)
    
    // 模拟API请求成功
    setTimeout(() => {
      message.value = '密码重置链接已发送到您的邮箱，请查收'
      messageType.value = 'success'
      loading.value = false
    }, 1000)
  } catch (error) {
    console.error('重置密码失败:', error)
    message.value = '重置密码失败，请稍后再试'
    messageType.value = 'error'
    loading.value = false
  }
}
</script>

<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
      <h1>找回密码</h1>
      
      <el-alert
        v-if="message"
        :title="message"
        :type="messageType"
        show-icon
        class="alert-message"
      />
      
      <el-form class="forgot-form">
        <el-form-item>
          <el-input 
            v-model="email" 
            placeholder="请输入您的注册邮箱"
            type="email"
            prefix-icon="el-icon-message"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="loading" 
            @click="resetPassword" 
            class="submit-btn"
          >
            发送重置链接
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="links">
        <router-link to="/login">返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.forgot-password-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.forgot-password-container {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.alert-message {
  margin-bottom: 20px;
}

.submit-btn {
  width: 100%;
}

.links {
  margin-top: 20px;
  text-align: center;
}

.links a {
  color: #409EFF;
  text-decoration: none;
  font-size: 14px;
}

.links a:hover {
  text-decoration: underline;
}
</style> 