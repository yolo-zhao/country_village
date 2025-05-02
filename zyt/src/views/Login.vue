<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const router = useRouter()

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ]
}

// 表单引用
const loginFormRef = ref(null)

// 加载状态
const loading = ref(false)

// 错误信息
const errorMessage = ref('')

// 处理登录
const handleLogin = async () => {
  // 清除之前的错误信息
  errorMessage.value = ''
  
  // 表单验证
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      
      try {
        // 调用登录操作
        const loginSuccess = await userStore.login(loginForm)
        
        if (loginSuccess) {
          // 登录成功，重定向到首页或之前的页面
          const redirect = router.currentRoute.value.query.redirect || '/'
          router.push(redirect)
        } else {
          errorMessage.value = '登录失败，请检查用户名和密码'
        }
      } catch (error) {
        console.error('登录出错:', error)
        errorMessage.value = '登录时发生错误，请稍后再试'
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <h2 class="login-title">欢迎登录</h2>
      
      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        class="mb-20"
      />
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            class="login-button" 
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-options">
        <router-link to="/forgot-password">忘记密码?</router-link>
        <span class="divider">|</span>
        <router-link to="/register">注册新账号</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: var(--primary-color);
  font-size: 1.8rem;
}

.login-button {
  width: 100%;
}

.login-options {
  margin-top: 20px;
  text-align: center;
}

.divider {
  margin: 0 10px;
  color: #ddd;
}

@media (max-width: 480px) {
  .login-container {
    padding: 20px;
  }
}
</style> 