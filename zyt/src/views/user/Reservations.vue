<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { activityApi } from '../../api/activities'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 预约列表
const reservations = ref([])

// 加载状态
const loading = ref(true)

// 获取预约列表
const fetchReservations = async () => {
  loading.value = true
  try {
    const response = await activityApi.getUserReservations()
    reservations.value = response.data || []
  } catch (error) {
    console.error('获取预约列表失败:', error)
    ElMessage.error('获取预约列表失败')
  } finally {
    loading.value = false
  }
}

// 取消预约
const cancelReservation = async (reservationId) => {
  ElMessageBox.confirm(
    '确定要取消此预约吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await activityApi.cancelReservation(reservationId)
      ElMessage.success('预约已取消')
      // 刷新预约列表
      fetchReservations()
    } catch (error) {
      console.error('取消预约失败:', error)
      ElMessage.error('取消预约失败')
    }
  }).catch(() => {})
}

// 跳转到活动详情
const goToActivityDetail = (activityId) => {
  router.push(`/activities/${activityId}`)
}

// 获取预约状态标签类型
const getStatusType = (status) => {
  switch (status) {
    case 'pending':
      return 'warning'
    case 'confirmed':
      return 'success'
    case 'cancelled':
      return 'danger'
    case 'completed':
      return 'info'
    default:
      return 'info'
  }
}

// 格式化预约状态
const formatStatus = (status) => {
  switch (status) {
    case 'pending':
      return '待确认'
    case 'confirmed':
      return '已确认'
    case 'cancelled':
      return '已取消'
    case 'completed':
      return '已完成'
    default:
      return '未知'
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchReservations()
})
</script>

<template>
  <div class="reservations-page">
    <h1 class="page-title">我的预约</h1>
    
    <el-skeleton :rows="5" animated v-if="loading" />
    
    <div v-else-if="reservations.length === 0" class="empty-reservations">
      <el-empty description="暂无预约记录">
        <template #description>
          <p>您还没有预约过任何活动，快去参与体验吧！</p>
        </template>
        <router-link to="/activities">
          <el-button type="primary">浏览活动</el-button>
        </router-link>
      </el-empty>
    </div>
    
    <div v-else class="reservations-list">
      <el-timeline>
        <el-timeline-item
          v-for="reservation in reservations"
          :key="reservation.id"
          :timestamp="new Date(reservation.created_at).toLocaleString()"
          :type="getStatusType(reservation.status)"
        >
          <el-card class="reservation-card">
            <div class="reservation-content">
              <div class="reservation-info">
                <h3 
                  class="activity-title"
                  @click="goToActivityDetail(reservation.activity.id)"
                >
                  {{ reservation.activity.title }}
                </h3>
                
                <div class="reservation-meta">
                  <p>
                    <el-icon><Calendar /></el-icon>
                    预约日期: {{ new Date(reservation.reservation_date).toLocaleDateString() }}
                  </p>
                  
                  <p>
                    <el-icon><Location /></el-icon>
                    活动地点: {{ reservation.activity.location }}
                  </p>
                  
                  <p>
                    <el-icon><User /></el-icon>
                    联系人: {{ reservation.contact_name }}
                  </p>
                  
                  <p>
                    <el-icon><Phone /></el-icon>
                    联系电话: {{ reservation.contact_phone }}
                  </p>
                </div>
              </div>
              
              <div class="reservation-actions">
                <el-tag :type="getStatusType(reservation.status)">
                  {{ formatStatus(reservation.status) }}
                </el-tag>
                
                <div class="action-buttons">
                  <el-button 
                    size="small" 
                    @click="goToActivityDetail(reservation.activity.id)"
                  >
                    查看活动
                  </el-button>
                  
                  <el-button 
                    v-if="['pending', 'confirmed'].includes(reservation.status)"
                    type="danger" 
                    size="small" 
                    @click="cancelReservation(reservation.id)"
                  >
                    取消预约
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<style scoped>
.reservations-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-align: center;
}

.empty-reservations {
  margin: 50px 0;
  text-align: center;
}

.reservation-card {
  margin-bottom: 20px;
}

.reservation-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.reservation-info {
  flex: 1;
}

.activity-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  cursor: pointer;
  color: var(--primary-color);
}

.activity-title:hover {
  text-decoration: underline;
}

.reservation-meta {
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.reservation-meta p {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.reservation-meta .el-icon {
  margin-right: 5px;
}

.reservation-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

@media (max-width: 768px) {
  .reservation-content {
    flex-direction: column;
  }
  
  .reservation-actions {
    margin-top: 15px;
    align-items: flex-start;
  }
}
</style> 