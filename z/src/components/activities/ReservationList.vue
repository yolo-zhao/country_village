<template>
  <div class="reservation-list" v-loading="loading">
    <el-table :data="reservations" style="width: 100%">
      <el-table-column prop="activity.title" label="活动名称" min-width="200">
        <template #default="{ row }">
          <el-link type="primary" @click="handleView(row.activity)">
            {{ row.activity.title }}
          </el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="activity.location" label="活动地点" />
      
      <el-table-column label="活动时间" min-width="200">
        <template #default="{ row }">
          {{ formatDate(row.activity.start_time) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="预约状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button 
            v-if="row.status === 'pending'"
            type="danger" 
            size="small" 
            @click="handleCancel(row)"
          >
            取消预约
          </el-button>
          <el-button 
            v-if="canCheckIn(row)"
            type="success" 
            size="small" 
            @click="handleCheckIn(row)"
          >
            打卡签到
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 活动详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentActivity?.title"
      width="60%"
      destroy-on-close
    >
      <div class="activity-detail" v-if="currentActivity">
        <el-image
          :src="currentActivity.cover_image || '/default-activity.jpg'"
          class="detail-image"
          fit="cover"
        />
        <div class="detail-info">
          <div class="info-item">
            <label>活动时间：</label>
            <span>{{ formatDate(currentActivity.start_time) }} - {{ formatDate(currentActivity.end_time) }}</span>
          </div>
          <div class="info-item">
            <label>活动地点：</label>
            <span>{{ currentActivity.location }}</span>
          </div>
          <div class="info-item">
            <label>活动状态：</label>
            <el-tag :type="getStatusType(currentActivity.status)">
              {{ getStatusText(currentActivity.status) }}
            </el-tag>
          </div>
          <div class="info-item">
            <label>活动描述：</label>
            <p>{{ currentActivity.description }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

// 数据
const loading = ref(false)
const reservations = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const currentActivity = ref(null)

// 获取预约列表
const fetchReservations = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/activities/reservations/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        status: props.status
      }
    })
    reservations.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('Fetch reservations error:', error)
    ElMessage.error('获取预约列表失败')
  } finally {
    loading.value = false
  }
}

// 状态相关
const getStatusType = (status) => {
  const types = {
    'pending': 'warning',
    'completed': 'success',
    'cancelled': 'info'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'pending': '待参加',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return texts[status] || status
}

// 日期格式化
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 事件处理
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchReservations()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchReservations()
}

const handleView = (activity) => {
  currentActivity.value = activity
  dialogVisible.value = true
}

const handleCancel = async (reservation) => {
  try {
    await ElMessageBox.confirm('确定要取消这个预约吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.post(`/api/activities/reservations/${reservation.id}/cancel/`)
    ElMessage.success('取消预约成功')
    fetchReservations()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Cancel reservation error:', error)
      ElMessage.error('取消预约失败')
    }
  }
}

const handleCheckIn = async (reservation) => {
  try {
    await axios.post(`/api/activities/reservations/${reservation.id}/check-in/`)
    ElMessage.success('打卡签到成功')
    fetchReservations()
  } catch (error) {
    console.error('Check-in error:', error)
    ElMessage.error('打卡签到失败')
  }
}

// 判断是否可以打卡
const canCheckIn = (reservation) => {
  if (reservation.status !== 'pending') return false
  const now = new Date()
  const startTime = new Date(reservation.activity.start_time)
  const endTime = new Date(reservation.activity.end_time)
  return now >= startTime && now <= endTime
}

// 生命周期
onMounted(() => {
  fetchReservations()
})
</script>

<style scoped>
.reservation-list {
  min-height: 100%;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.detail-image {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 20px;
}

.detail-info {
  margin: 20px 0;
}

.info-item {
  margin-bottom: 15px;
}

.info-item label {
  font-weight: bold;
  margin-right: 10px;
}
</style> 