<template>
  <div class="farmer-profile">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>农户信息</h3>
          <el-button type="primary" @click="handleEdit">编辑信息</el-button>
        </div>
      </template>

      <div v-if="farmer" class="profile-content">
        <div class="profile-section">
          <h4>基本信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="姓名">{{ farmer.name }}</el-descriptions-item>
            <el-descriptions-item label="手机号">{{ farmer.phone }}</el-descriptions-item>
            <el-descriptions-item label="身份证号">{{ farmer.id_card }}</el-descriptions-item>
            <el-descriptions-item label="注册时间">{{ formatDate(farmer.created_at) }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="profile-section">
          <h4>农场信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="农场名称">{{ farmer.farm_name }}</el-descriptions-item>
            <el-descriptions-item label="农场地址">{{ farmer.farm_address }}</el-descriptions-item>
            <el-descriptions-item label="农场面积">{{ farmer.farm_area }}亩</el-descriptions-item>
            <el-descriptions-item label="主要产品">{{ farmer.main_products }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="profile-section">
          <h4>认证信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="认证状态">
              <el-tag :type="farmer.is_verified ? 'success' : 'warning'">
                {{ farmer.is_verified ? '已认证' : '未认证' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="认证时间">
              {{ farmer.verified_at ? formatDate(farmer.verified_at) : '-' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑农户信息"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="form.id_card" />
        </el-form-item>
        <el-form-item label="农场名称" prop="farm_name">
          <el-input v-model="form.farm_name" />
        </el-form-item>
        <el-form-item label="农场地址" prop="farm_address">
          <el-input v-model="form.farm_address" />
        </el-form-item>
        <el-form-item label="农场面积" prop="farm_area">
          <el-input-number v-model="form.farm_area" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="主要产品" prop="main_products">
          <el-input
            v-model="form.main_products"
            type="textarea"
            :rows="3"
            placeholder="请输入主要种植的农产品，用逗号分隔"
          />
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

// 表单数据
const form = ref({
  name: '',
  phone: '',
  id_card: '',
  farm_name: '',
  farm_address: '',
  farm_area: 0,
  main_products: ''
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  id_card: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入正确的身份证号', trigger: 'blur' }
  ],
  farm_name: [{ required: true, message: '请输入农场名称', trigger: 'blur' }],
  farm_address: [{ required: true, message: '请输入农场地址', trigger: 'blur' }],
  farm_area: [{ required: true, message: '请输入农场面积', trigger: 'blur' }],
  main_products: [{ required: true, message: '请输入主要产品', trigger: 'blur' }]
}

// 从 store 获取农户信息
const farmer = computed(() => store.state.user.currentUser?.farmer)

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

// 编辑信息
const handleEdit = () => {
  if (farmer.value) {
    form.value = {
      name: farmer.value.name,
      phone: farmer.value.phone,
      id_card: farmer.value.id_card,
      farm_name: farmer.value.farm_name,
      farm_address: farmer.value.farm_address,
      farm_area: farmer.value.farm_area,
      main_products: farmer.value.main_products
    }
    dialogVisible.value = true
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    await store.dispatch('user/updateFarmerProfile', form.value)
    ElMessage.success('更新成功')
    dialogVisible.value = false
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取农户信息
const fetchFarmerProfile = async () => {
  loading.value = true
  try {
    await store.dispatch('user/fetchCurrentUser')
  } catch (error) {
    ElMessage.error('获取农户信息失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFarmerProfile()
})
</script>

<style scoped>
.farmer-profile {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-section {
  margin-bottom: 24px;
}

.profile-section h4 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #606266;
}

:deep(.el-descriptions) {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 100px;
}
</style> 