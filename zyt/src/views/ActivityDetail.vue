<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { activityApi } from '../api/activities'
import { ElMessage, ElMessageBox } from 'element-plus'
import http from '../api/http'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 活动ID
const activityId = computed(() => route.params.id)

// 活动详情
const activity = ref(null)

// 加载状态
const loading = ref(true)

// 图片预览
const previewVisible = ref(false)
const previewIndex = ref(0)

// 预约表单
const reservationForm = reactive({
  activity: computed(() => activityId.value),
  contact_name: '',
  contact_phone: '',
  reservation_date: '',
  status: 'pending' // 默认状态
})

// 表单规则
const rules = {
  contact_name: [
    { required: true, message: '请输入联系人姓名', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  reservation_date: [
    { required: true, message: '请选择预约日期', trigger: 'change' }
  ]
}

// 预约表单引用
const reservationFormRef = ref(null)

// 预约对话框
const reservationDialogVisible = ref(false)

// 预约加载状态
const reservationLoading = ref(false)

// 是否已登录
const isLoggedIn = computed(() => userStore.isLoggedIn)

// 是否已满
const isFull = computed(() => {
  if (!activity.value) return false
  return activity.value.reservation_count >= activity.value.max_participants
})

// 是否已经过期
const isExpired = computed(() => {
  if (!activity.value) return false
  return new Date(activity.value.end_time) < new Date()
})

// 是否可预约
const canReserve = computed(() => {
  return isLoggedIn.value && !isFull.value && !isExpired.value
})

// 获取活动详情
const fetchActivityDetail = async () => {
  loading.value = true
  try {
    const response = await activityApi.getActivityDetail(activityId.value)
    
    // 标准化活动数据
    const activityData = response.data;
    activity.value = {
      ...activityData,
      id: activityData.id || 0,
      title: activityData.title || '',
      description: activityData.description || '',
      location: activityData.location || '',
      start_time: activityData.start_time || new Date().toISOString(),
      end_time: activityData.end_time || new Date().toISOString(),
      cover_image: getFullImageUrl(activityData.cover_image),
      max_participants: activityData.max_participants || 0,
      reservation_count: activityData.reservation_count || 0,
      category: activityData.category || { id: 0, name: '' },
      tags: Array.isArray(activityData.tags) ? activityData.tags : [],
      farmer: activityData.farmer || { username: '' },
      images: Array.isArray(activityData.images) ? activityData.images.map(img => ({
        ...img,
        image: getFullImageUrl(img.image)
      })) : []
    }
    
    console.log('活动详情数据:', activity.value)
  } catch (error) {
    console.error('获取活动详情失败:', error)
    ElMessage.error('获取活动详情失败')
  } finally {
    loading.value = false
  }
}

// 添加图片URL处理函数
const getFullImageUrl = (imageUrl) => {
  if (!imageUrl) return 'https://via.placeholder.com/800x450?text=乡村活动';
  
  // 如果是完整URL，直接返回
  if (imageUrl.startsWith('http')) return imageUrl;
  
  // 如果是相对路径但没有以/开头，添加/
  if (!imageUrl.startsWith('/')) {
    imageUrl = '/' + imageUrl;
  }
  
  // 如果URL不包含域名，添加服务器地址
  return `http://localhost:8000${imageUrl}`;
};

// 打开预约对话框
const openReservationDialog = () => {
  if (!isLoggedIn.value) {
    ElMessageBox.confirm(
      '请先登录后再进行预约',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      router.push({ 
        path: '/login', 
        query: { redirect: route.fullPath }
      })
    }).catch(() => {})
    return
  }
  
  // 重置表单数据
  reservationForm.contact_name = ''
  reservationForm.contact_phone = ''
  reservationForm.reservation_date = ''
  
  // 显示预约对话框
  reservationDialogVisible.value = true
}

// 提交预约
const submitReservation = async () => {
  if (!reservationFormRef.value) return
  
  // 先检查是否登录
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录后再提交预约')
    router.push({ 
      path: '/login', 
      query: { redirect: route.fullPath }
    })
    return
  }
  
  await reservationFormRef.value.validate(async (valid) => {
    if (valid) {
      reservationLoading.value = true
      try {
        // 方法1: 使用活动API服务的预约方法
        console.log('提交预约数据:', {
          activityId: activityId.value,
          contact_name: reservationForm.contact_name,
          contact_phone: reservationForm.contact_phone,
          reservation_date: reservationForm.reservation_date
        })
        
        await activityApi.reserveActivity(activityId.value, {
          contact_name: reservationForm.contact_name,
          contact_phone: reservationForm.contact_phone,
          reservation_date: reservationForm.reservation_date
        })
        
        ElMessage.success('预约成功！')
        reservationDialogVisible.value = false
        
        // 刷新活动详情
        fetchActivityDetail()
        
      } catch (error) {
        console.error('预约失败，详细错误:', error)
        console.error('错误响应数据:', error.response?.data)
        
        // 如果是401错误，提示登录
        if (error.response?.status === 401) {
          ElMessageBox.confirm(
            '登录已过期或未登录，请重新登录',
            '提示',
            {
              confirmButtonText: '去登录',
              cancelButtonText: '取消',
              type: 'warning'
            }
          ).then(() => {
            router.push({ 
              path: '/login', 
              query: { redirect: route.fullPath }
            })
          }).catch(() => {})
          return
        }
        
        // 显示更具体的错误信息
        let errorMsg = '预约失败，请稍后再试'
        if (error.response?.data) {
          // 尝试提取Django REST框架错误信息
          const errorData = error.response.data
          if (typeof errorData === 'object') {
            const errorDetails = Object.entries(errorData)
              .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
              .join('; ')
            errorMsg = `预约失败: ${errorDetails}`
          } else if (typeof errorData === 'string') {
            errorMsg = `预约失败: ${errorData}`
          }
        }
        
        ElMessage.error(errorMsg)
      } finally {
        reservationLoading.value = false
      }
    }
  })
}

// 图片预览
const previewImage = (index) => {
  previewIndex.value = index
  previewVisible.value = true
}

// 页面加载时获取数据
onMounted(() => {
  fetchActivityDetail()
})
</script>

<template>
  <div class="activity-detail-page">
    <el-skeleton :rows="15" animated v-if="loading" />
    
    <div v-else-if="!activity" class="empty-data">
      <el-empty description="活动不存在或已被删除" />
      <router-link to="/activities">
        <el-button>返回活动列表</el-button>
      </router-link>
    </div>
    
    <template v-else>
      <div class="activity-header">
        <div class="activity-title-container">
          <h1 class="activity-title">{{ activity.title }}</h1>
          
          <div class="activity-tags" v-if="activity.tags && activity.tags.length">
            <el-tag
              v-for="tag in activity.tags"
              :key="tag.id"
              size="small"
              effect="light"
              class="mr-5"
            >
              {{ tag.name }}
            </el-tag>
          </div>
        </div>
        
        <div class="activity-action">
          <el-button 
            type="primary" 
            size="large"
            @click="openReservationDialog"
            :disabled="!canReserve"
          >
            {{ isFull ? '名额已满' : isExpired ? '活动已结束' : '立即预约' }}
          </el-button>
        </div>
      </div>
      
      <el-divider />
      
      <div class="activity-content">
        <div class="activity-details">
          <div class="activity-info-item">
            <el-icon><Clock /></el-icon>
            <span>开始时间：{{ new Date(activity.start_time).toLocaleString() }}</span>
          </div>
          
          <div class="activity-info-item">
            <el-icon><Clock /></el-icon>
            <span>结束时间：{{ new Date(activity.end_time).toLocaleString() }}</span>
          </div>
          
          <div class="activity-info-item">
            <el-icon><Location /></el-icon>
            <span>活动地点：{{ activity.location }}</span>
          </div>
          
          <div class="activity-info-item">
            <el-icon><User /></el-icon>
            <span>
              已报名：{{ activity.reservation_count || 0 }}/{{ activity.max_participants }}
              <el-progress 
                :percentage="(activity.reservation_count / activity.max_participants) * 100" 
                :stroke-width="8"
                :show-text="false"
                style="width: 100px; margin-left: 10px;"
              />
            </span>
          </div>
          
          <div class="activity-info-item">
            <el-icon><UserFilled /></el-icon>
            <span>组织者：{{ activity.farmer?.username || '未知' }}</span>
          </div>
          
          <div class="activity-info-item" v-if="activity.category">
            <el-icon><Collection /></el-icon>
            <span>活动分类：{{ activity.category.name }}</span>
          </div>
        </div>
        
        <el-divider />
        
        <div class="activity-gallery" v-if="activity.images && activity.images.length">
          <h2 class="section-title">活动图片</h2>
          
          <div class="activity-images">
            <div 
              v-for="(image, index) in activity.images" 
              :key="index"
              class="activity-image-item"
              @click="previewImage(index)"
            >
              <el-image 
                :src="image.image" 
                fit="cover"
                loading="lazy"
                :alt="image.caption || '活动图片'"
              >
                <template #placeholder>
                  <div class="image-placeholder">
                    <el-icon><PictureFilled /></el-icon>
                  </div>
                </template>
              </el-image>
              <div class="image-caption" v-if="image.caption">
                {{ image.caption }}
              </div>
            </div>
          </div>
          
          <el-image-viewer
            v-if="previewVisible"
            :url-list="activity.images.map(img => img.image)"
            :initial-index="previewIndex"
            @close="previewVisible = false"
          />
        </div>
        
        <el-divider />
        
        <div class="activity-description-section">
          <h2 class="section-title">活动详情</h2>
          
          <div class="activity-description">
            <p>{{ activity.description }}</p>
          </div>
        </div>
      </div>
      
      <!-- 预约对话框 -->
      <el-dialog
        v-model="reservationDialogVisible"
        title="活动预约"
        width="500px"
        :close-on-click-modal="false"
      >
        <el-form
          ref="reservationFormRef"
          :model="reservationForm"
          :rules="rules"
          label-width="100px"
        >
          <el-form-item label="联系人" prop="contact_name">
            <el-input v-model="reservationForm.contact_name" placeholder="请输入联系人姓名" />
          </el-form-item>
          
          <el-form-item label="联系电话" prop="contact_phone">
            <el-input v-model="reservationForm.contact_phone" placeholder="请输入联系电话" />
          </el-form-item>
          
          <el-form-item label="预约日期" prop="reservation_date">
            <el-date-picker
              v-model="reservationForm.reservation_date"
              type="date"
              placeholder="选择预约日期"
              value-format="YYYY-MM-DD"
              :disabled-date="date => date.getTime() < Date.now() - 8.64e7 || date.getTime() > new Date(activity.end_time).getTime()"
            />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <el-button @click="reservationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReservation" :loading="reservationLoading">
            确认预约
          </el-button>
        </template>
      </el-dialog>
    </template>
  </div>
</template>

<style scoped>
.activity-detail-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activity-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.activity-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.mr-5 {
  margin-right: 5px;
}

.activity-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin: 20px 0;
}

.activity-info-item {
  display: flex;
  align-items: center;
  color: var(--text-color-secondary);
}

.activity-info-item .el-icon {
  margin-right: 10px;
  color: var(--primary-color);
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: var(--text-color);
  border-left: 4px solid var(--primary-color);
  padding-left: 10px;
}

.activity-gallery {
  margin: 30px 0;
}

.activity-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.activity-image-item {
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.activity-image-item:hover {
  transform: scale(1.03);
}

.activity-image-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-caption {
  padding: 10px;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
  background-color: #f5f5f5;
}

.image-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 150px;
  background-color: #f5f5f5;
}

.activity-description-section {
  margin: 30px 0;
}

.activity-description {
  line-height: 1.8;
  color: var(--text-color);
  white-space: pre-line;
}

@media (max-width: 768px) {
  .activity-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .activity-action {
    margin-top: 20px;
    width: 100%;
  }
  
  .activity-action button {
    width: 100%;
  }
}
</style> 