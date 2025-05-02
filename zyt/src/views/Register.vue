<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const router = useRouter()

// 注册表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  firstName: '',
  lastName: '',
  role: 'tourist' // 默认为游客
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
  ],
  confirmPassword: [
    { 
      required: true, 
      message: '请再次输入密码', 
      trigger: 'blur' 
    },
    { 
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  firstName: [
    { required: true, message: '请输入名字', trigger: 'blur' }
  ],
  lastName: [
    { required: true, message: '请输入姓氏', trigger: 'blur' }
  ]
}

// 表单引用
const registerFormRef = ref(null)

// 加载状态
const loading = ref(false)

// 错误信息
const errorMessage = ref('')

// 处理注册
const handleRegister = async () => {
  // 清除之前的错误信息
  errorMessage.value = ''
  
  // 表单验证
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      
      try {
        // 准备注册数据（移除确认密码字段）
        const userData = {...registerForm}
        delete userData.confirmPassword
        
        // 调用注册操作
        const result = await userStore.register(userData)
        
        if (result.success) {
          // 注册成功，跳转到登录页
          router.push('/login')
        } else {
          errorMessage.value = result.error || '注册失败，请稍后再试'
        }
      } catch (error) {
        console.error('注册出错:', error)
        errorMessage.value = '注册时发生错误，请稍后再试'
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <div class="register-page">
    <div class="register-container">
      <h2 class="register-title">创建新账号</h2>
      
      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        class="mb-20"
      />
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="电子邮箱" prop="email">
          <el-input 
            v-model="registerForm.email"
            placeholder="请输入电子邮箱"
            prefix-icon="Message"
          />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="名字" prop="firstName">
              <el-input 
                v-model="registerForm.firstName"
                placeholder="请输入名字"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="姓氏" prop="lastName">
              <el-input 
                v-model="registerForm.lastName"
                placeholder="请输入姓氏"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="账号类型">
          <el-radio-group v-model="registerForm.role">
            <el-radio label="tourist">游客</el-radio>
            <el-radio label="farmer">农场主</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            class="register-button" 
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-options">
        已有账号? <router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30px 20px;
}

.register-container {
  width: 100%;
  max-width: 500px;
  padding: 30px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.register-title {
  text-align: center;
  margin-bottom: 30px;
  color: var(--primary-color);
  font-size: 1.8rem;
}

.register-button {
  width: 100%;
}

.register-options {
  margin-top: 20px;
  text-align: center;
}

@media (max-width: 480px) {
  .register-container {
    padding: 20px;
  }
}
</style> 