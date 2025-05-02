<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { activityApi } from '../../api/activities'
import { serializeActivity } from '../../api/serializers'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 获取活动ID（如果是编辑模式）
const activityId = computed(() => route.params.id)

// 判断是否是编辑模式
const isEditMode = computed(() => !!activityId.value)

// 页面标题
const pageTitle = computed(() => isEditMode.value ? '编辑活动' : '创建新活动')

// 活动表单数据
const activityForm = reactive({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  category: '',
  tags: [],
  cover_image: '',
  max_participants: 20,
  status: 'published'
})

// 表单规则
const rules = {
  title: [
    { required: true, message: '请输入活动标题', trigger: 'blur' },
    { min: 3, max: 100, message: '标题长度应在3-100个字符之间', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入活动描述', trigger: 'blur' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入活动地点', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择活动分类', trigger: 'change' },
    { 
      validator: (rule, value, callback) => {
        if (!value || value === '' || isNaN(Number(value))) {
          callback(new Error('请选择有效的活动分类'));
        } else {
          callback();
        }
      }, 
      trigger: 'change' 
    }
  ],
  max_participants: [
    { required: true, type: 'number', message: '请输入人数上限', trigger: 'blur' }
  ]
}

// 表单引用
const formRef = ref(null)

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 分类列表
const categories = ref([])

// 标签列表
const tags = ref([])

// 获取活动分类
const fetchCategories = async () => {
  try {
    const response = await activityApi.getCategories()
    categories.value = response.data || []
    console.log('获取到分类列表:', categories.value);
    
    // 确保分类是有效的数据
    if (categories.value.length === 0) {
      ElMessage.warning('未获取到活动分类数据，请联系管理员');
    }
  } catch (error) {
    console.error('获取活动分类失败:', error)
    ElMessage.error('获取活动分类失败')
  }
}

// 获取标签列表
const fetchTags = async () => {
  try {
    const response = await activityApi.getTags()
    tags.value = response.data || []
  } catch (error) {
    console.error('获取标签列表失败:', error)
    ElMessage.error('获取标签列表失败')
  }
}

// 获取活动详情（编辑模式）
const fetchActivityDetail = async () => {
  if (!isEditMode.value) return
  
  loading.value = true
  try {
    const response = await activityApi.getActivityDetail(activityId.value)
    const activity = response.data
    
    // 填充表单数据
    activityForm.title = activity.title
    activityForm.description = activity.description
    activityForm.start_time = activity.start_time
    activityForm.end_time = activity.end_time
    activityForm.location = activity.location
    activityForm.category = activity.category?.id ? Number(activity.category.id) : ''
    activityForm.tags = activity.tags?.map(tag => tag.id) || []
    activityForm.cover_image = activity.cover_image
    activityForm.max_participants = activity.max_participants
    
    console.log('加载的活动数据:', activityForm);
    console.log('分类ID:', activityForm.category, '类型:', typeof activityForm.category);
  } catch (error) {
    console.error('获取活动详情失败:', error)
    ElMessage.error('获取活动详情失败')
    router.push('/farmer/dashboard')
  } finally {
    loading.value = false
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      // 检查分类是否已选择
      if (!activityForm.category) {
        ElMessage.error('请选择活动分类');
        return;
      }
      
      // 确保分类字段是数字
      const categoryId = Number(activityForm.category);
      if (isNaN(categoryId) || categoryId <= 0) {
        ElMessage.error('请选择有效的活动分类');
        return;
      }
      
      console.log('提交表单数据:', activityForm);
      console.log('分类ID:', activityForm.category, '类型:', typeof activityForm.category);
      
      // 确保category是数字类型
      activityForm.category = categoryId;
      
      submitLoading.value = true
      try {
        // 使用序列化器处理数据
        const submitData = serializeActivity({ ...activityForm });
        
        console.log('序列化后的提交数据:', submitData);
        console.log('处理后分类ID:', submitData.category, '类型:', typeof submitData.category);
        console.log('添加的category_id:', submitData.category_id, '类型:', typeof submitData.category_id);
        
        if (isEditMode.value) {
          // 编辑活动
          await activityApi.updateActivity(activityId.value, submitData)
          ElMessage.success('活动更新成功')
        } else {
          // 创建活动
          await activityApi.createActivity(submitData)
          ElMessage.success('活动创建成功')
        }
        
        // 返回到农场主管理面板
        router.push('/farmer/dashboard')
      } catch (error) {
        console.error('保存活动失败:', error)
        
        // 显示更详细的错误信息
        let errorMessage = '保存活动失败';
        if (error.response && error.response.data) {
          // 后端返回的详细错误信息
          const backendErrors = error.response.data;
          if (typeof backendErrors === 'object') {
            // 处理对象形式的错误
            errorMessage = Object.entries(backendErrors)
              .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
              .join('; ');
          } else if (typeof backendErrors === 'string') {
            // 处理字符串形式的错误
            errorMessage = backendErrors;
          }
        } else if (error.message) {
          // 前端验证捕获的错误
          errorMessage = error.message;
        }
        
        ElMessage.error(errorMessage);
        submitLoading.value = false
      }
    }
  })
}

// 取消操作
const cancelForm = () => {
  ElMessageBox.confirm(
    '确定要取消吗？所有未保存的更改将丢失。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    router.push('/farmer/dashboard')
  }).catch(() => {})
}

// 上传封面图片成功时的处理
const handleCoverSuccess = (res) => {
  console.log('上传图片成功，响应数据:', res);
  if (res.url) {
    activityForm.cover_image = res.url;
    console.log('设置封面图片URL:', res.url);
  } else if (res.data && res.data.url) {
    activityForm.cover_image = res.data.url;
    console.log('从data中设置封面图片URL:', res.data.url);
  } else {
    console.error('上传响应中没有找到图片URL:', res);
    ElMessage.warning('图片上传成功，但无法获取图片URL');
  }
}

// 图片上传前的验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!')
    return false
  }
  
  return true
}

// 页面加载时获取数据
onMounted(() => {
  fetchCategories()
  fetchTags()
  fetchActivityDetail()
})
</script>

<template>
  <div class="activity-form-page">
    <h1 class="page-title">{{ pageTitle }}</h1>
    
    <el-skeleton :rows="10" animated v-if="loading" />
    
    <el-form
      v-else
      ref="formRef"
      :model="activityForm"
      :rules="rules"
      label-width="120px"
      class="activity-form"
    >
      <el-form-item label="活动标题" prop="title">
        <el-input v-model="activityForm.title" placeholder="请输入活动标题" />
      </el-form-item>
      
      <el-form-item label="活动描述" prop="description">
        <el-input
          v-model="activityForm.description"
          type="textarea"
          :rows="5"
          placeholder="请详细描述活动内容、特色和注意事项等"
        />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="开始时间" prop="start_time">
            <el-date-picker
              v-model="activityForm.start_time"
              type="datetime"
              placeholder="选择开始时间"
              value-format="YYYY-MM-DDTHH:mm:ss"
              format="YYYY-MM-DD HH:mm"
              :disabled-date="date => date.getTime() < Date.now() - 8.64e7"
            />
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="结束时间" prop="end_time">
            <el-date-picker
              v-model="activityForm.end_time"
              type="datetime"
              placeholder="选择结束时间"
              value-format="YYYY-MM-DDTHH:mm:ss"
              format="YYYY-MM-DD HH:mm"
              :disabled-date="date => !activityForm.start_time || date.getTime() < new Date(activityForm.start_time).getTime()"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="活动地点" prop="location">
        <el-input v-model="activityForm.location" placeholder="请输入活动地点" />
      </el-form-item>
      
      <el-form-item label="活动分类" prop="category">
        <el-select 
          v-model="activityForm.category" 
          placeholder="选择活动分类"
          value-key="id"
          @change="val => { 
            console.log('分类选择变化:', val, typeof val); 
            activityForm.category = Number(val);
          }"
        >
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
        <div class="form-tip" v-if="categories.length === 0">
          <el-alert type="info" :closable="false" show-icon>
            正在加载分类数据，如果未显示请刷新页面
          </el-alert>
        </div>
      </el-form-item>
      
      <el-form-item label="活动标签">
        <el-select v-model="activityForm.tags" multiple placeholder="选择活动标签">
          <el-option
            v-for="tag in tags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="人数上限" prop="max_participants">
        <el-input-number v-model="activityForm.max_participants" :min="1" :step="1" />
      </el-form-item>
      
      <el-form-item label="活动状态" prop="status">
        <el-select v-model="activityForm.status">
          <el-option label="草稿" value="draft" />
          <el-option label="已发布" value="published" />
          <el-option label="已取消" value="cancelled" />
          <el-option label="已完成" value="completed" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="封面图片">
        <el-upload
          class="cover-uploader"
          action="/api/upload/"
          :headers="{
            Authorization: `Token ${userStore.getToken}`
          }"
          :show-file-list="false"
          :on-success="handleCoverSuccess"
          :before-upload="beforeUpload"
        >
          <img v-if="activityForm.cover_image" :src="activityForm.cover_image" class="cover-image" />
          <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
        </el-upload>
        <div class="upload-tip">请上传活动封面图片，建议尺寸 800x400 像素</div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="submitLoading">
          {{ isEditMode ? '保存修改' : '创建活动' }}
        </el-button>
        <el-button @click="cancelForm">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.activity-form-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 1.8rem;
  margin-bottom: 30px;
  text-align: center;
}

.activity-form {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.cover-uploader {
  width: 300px;
}

.cover-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 300px;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-uploader .el-upload:hover {
  border-color: var(--primary-color);
}

.cover-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-tip {
  margin-top: 10px;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}

.form-tip {
  margin-top: 5px;
  font-size: 0.9rem;
}
</style> 