<template>
  <div class="tourist-profile">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>个人资料</h3>
          <el-button type="primary" @click="handleEdit">编辑资料</el-button>
        </div>
      </template>

      <div class="profile-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户名">{{ userInfo.username }}</el-descriptions-item>
          <el-descriptions-item label="昵称">{{ userInfo.nickname }}</el-descriptions-item>
          <el-descriptions-item label="手机号码">{{ userInfo.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ userInfo.email }}</el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ formatDate(userInfo.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="最后登录">{{ formatDate(userInfo.last_login) }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑资料"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" />
        </el-form-item>
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const store = useStore()
const loading = ref(false)
const dialogVisible = ref(false)
const formRef = ref(null)

// 用户信息
const userInfo = computed(() => store.state.user)

// 表单数据
const form = ref({
  nickname: '',
  phone: '',
  email: ''
})

// 表单验证规则
const rules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 编辑资料
const handleEdit = () => {
  form.value = {
    nickname: userInfo.value.nickname,
    phone: userInfo.value.phone,
    email: userInfo.value.email
  }
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    await store.dispatch('updateUserInfo', form.value)
    ElMessage.success('更新成功')
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  store.dispatch('fetchCurrentUser')
})
</script>

<style scoped>
.tourist-profile {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

:deep(.el-descriptions) {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 100px;
}
</style> 