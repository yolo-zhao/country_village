<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const userStore = useUserStore()

// 用户信息
const userInfo = ref(null)

// 加载状态
const loading = ref(true)

// 是否编辑模式
const isEditing = ref(false)

// 编辑表单
const profileForm = reactive({
  nickname: '',
  firstName: '',
  lastName: '',
  email: '',
  contactPhone: '',
  address: ''
})

// 表单规则
const rules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ],
  contactPhone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 表单引用
const formRef = ref(null)

// 获取用户信息
const fetchUserProfile = async () => {
  loading.value = true
  try {
    // 从 store 获取用户信息
    const profile = await userStore.fetchUserProfile()
    
    userInfo.value = profile
    
    // 初始化编辑表单
    profileForm.nickname = profile.nickname || ''
    profileForm.firstName = profile.first_name || ''
    profileForm.lastName = profile.last_name || ''
    profileForm.email = profile.email || ''
    profileForm.contactPhone = profile.contact_phone || ''
    profileForm.address = profile.address || ''
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  } finally {
    loading.value = false
  }
}

// 开始编辑
const startEditing = () => {
  isEditing.value = true
}

// 取消编辑
const cancelEditing = () => {
  isEditing.value = false
  
  // 重置表单数据
  if (userInfo.value) {
    profileForm.nickname = userInfo.value.nickname || ''
    profileForm.firstName = userInfo.value.first_name || ''
    profileForm.lastName = userInfo.value.last_name || ''
    profileForm.email = userInfo.value.email || ''
    profileForm.contactPhone = userInfo.value.contact_phone || ''
    profileForm.address = userInfo.value.address || ''
  }
}

// 保存个人信息
const saveProfile = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 构建更新数据
        const updateData = {
          nickname: profileForm.nickname,
          first_name: profileForm.firstName,
          last_name: profileForm.lastName,
          email: profileForm.email,
          contact_phone: profileForm.contactPhone,
          address: profileForm.address
        }
        
        // 发送更新请求
        const response = await axios.put('http://localhost:8000/api/users/profile/', updateData, {
          headers: {
            Authorization: `Token ${userStore.getToken}`
          }
        })
        
        // 更新本地数据
        userInfo.value = response.data
        
        ElMessage.success('个人信息更新成功')
        isEditing.value = false
      } catch (error) {
        console.error('更新个人信息失败:', error)
        ElMessage.error('更新个人信息失败')
      } finally {
        loading.value = false
      }
    }
  })
}

// 页面加载时获取数据
onMounted(() => {
  fetchUserProfile()
})
</script>

<template>
  <div class="profile-page">
    <h1 class="page-title">个人资料</h1>
    
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
          <el-button 
            v-if="!isEditing" 
            type="primary" 
            @click="startEditing"
          >
            编辑资料
          </el-button>
          <div v-else>
            <el-button @click="cancelEditing">取消</el-button>
            <el-button type="primary" @click="saveProfile">保存</el-button>
          </div>
        </div>
      </template>
      
      <el-skeleton :rows="5" animated v-if="loading" />
      
      <div v-else>
        <!-- 查看模式 -->
        <div v-if="!isEditing" class="view-profile">
          <div class="profile-avatar">
            <el-avatar :size="100" icon="UserFilled" />
          </div>
          
          <div class="profile-info">
            <div class="info-item">
              <span class="info-label">用户名</span>
              <span class="info-value">{{ userInfo?.username || '未设置' }}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">昵称</span>
              <span class="info-value">{{ userInfo?.nickname || '未设置' }}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">姓名</span>
              <span class="info-value">
                {{ userInfo?.first_name || '' }} {{ userInfo?.last_name || '' || '未设置' }}
              </span>
            </div>
            
            <div class="info-item">
              <span class="info-label">电子邮箱</span>
              <span class="info-value">{{ userInfo?.email || '未设置' }}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">联系电话</span>
              <span class="info-value">{{ userInfo?.contact_phone || '未设置' }}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">地址</span>
              <span class="info-value">{{ userInfo?.address || '未设置' }}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">用户角色</span>
              <span class="info-value">
                <el-tag>{{ userInfo?.role === 'farmer' ? '农场主' : '游客' }}</el-tag>
              </span>
            </div>
            
            <div class="info-item">
              <span class="info-label">注册时间</span>
              <span class="info-value">
                {{ userInfo?.date_joined ? new Date(userInfo.date_joined).toLocaleString() : '未知' }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- 编辑模式 -->
        <el-form
          v-else
          ref="formRef"
          :model="profileForm"
          :rules="rules"
          label-width="100px"
        >
          <el-form-item label="昵称" prop="nickname">
            <el-input v-model="profileForm.nickname" placeholder="请输入昵称" />
          </el-form-item>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="名字" prop="firstName">
                <el-input v-model="profileForm.firstName" placeholder="请输入名字" />
              </el-form-item>
            </el-col>
            
            <el-col :span="12">
              <el-form-item label="姓氏" prop="lastName">
                <el-input v-model="profileForm.lastName" placeholder="请输入姓氏" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="profileForm.email" placeholder="请输入电子邮箱" />
          </el-form-item>
          
          <el-form-item label="联系电话" prop="contactPhone">
            <el-input v-model="profileForm.contactPhone" placeholder="请输入联系电话" />
          </el-form-item>
          
          <el-form-item label="地址" prop="address">
            <el-input v-model="profileForm.address" placeholder="请输入地址" />
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-align: center;
}

.profile-card {
  margin-bottom: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-avatar {
  margin-bottom: 30px;
}

.profile-info {
  width: 100%;
}

.info-item {
  display: flex;
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  width: 100px;
  color: var(--text-color-secondary);
  font-weight: bold;
}

.info-value {
  flex: 1;
  color: var(--text-color);
}

@media (max-width: 768px) {
  .info-item {
    flex-direction: column;
  }
  
  .info-label {
    margin-bottom: 5px;
  }
}
</style> 