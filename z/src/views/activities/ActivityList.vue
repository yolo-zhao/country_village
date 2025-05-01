<template>
  <div class="activity-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>乡村活动列表</h3>
          <el-button type="primary" @click="handleCreate" v-if="userRole === 'admin'">
            发布活动
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm">
          <el-form-item>
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索活动名称"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item>
            <el-select v-model="searchForm.category" placeholder="活动分类" clearable>
              <el-option
                v-for="item in categories"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-select v-model="searchForm.status" placeholder="活动状态" clearable>
              <el-option label="未开始" value="pending" />
              <el-option label="进行中" value="ongoing" />
              <el-option label="已结束" value="completed" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 活动列表 -->
      <div class="activity-grid" v-loading="loading">
        <el-row :gutter="20">
          <el-col :span="8" v-for="activity in activities" :key="activity.id">
            <el-card class="activity-card" :body-style="{ padding: '0px' }">
              <el-image
                :src="activity.cover_image || '/default-activity.jpg'"
                class="activity-image"
                fit="cover"
              />
              <div class="activity-info">
                <h4>{{ activity.title }}</h4>
                <p class="description">{{ activity.description }}</p>
                <div class="activity-meta">
                  <el-tag :type="getStatusType(activity.status)">
                    {{ getStatusText(activity.status) }}
                  </el-tag>
                  <span class="time">
                    <el-icon><Calendar /></el-icon>
                    {{ formatDate(activity.start_time) }}
                  </span>
                </div>
                <div class="activity-footer">
                  <el-button type="primary" @click="handleView(activity)">查看详情</el-button>
                  <el-button 
                    type="danger" 
                    @click="handleDelete(activity)"
                    v-if="userRole === 'admin'"
                  >删除</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 36, 48]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

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
        <div class="detail-actions">
          <el-button type="primary" @click="handleReserve" v-if="canReserve">
            立即预约
          </el-button>
          <el-button @click="dialogVisible = false">关闭</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar } from '@element-plus/icons-vue'
import axios from 'axios'

const store = useStore()
const userRole = computed(() => store.getters.userRole)

// 数据
const loading = ref(false)
const activities = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const dialogVisible = ref(false)
const currentActivity = ref(null)

// 搜索表单
const searchForm = reactive({
  keyword: '',
  category: '',
  status: ''
})

// 活动分类
const categories = [
  { label: '文化活动', value: 'culture' },
  { label: '农事体验', value: 'farming' },
  { label: '手工艺术', value: 'crafts' },
  { label: '美食品鉴', value: 'food' }
]

// 获取活动列表
const fetchActivities = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/activities/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        keyword: searchForm.keyword,
        category: searchForm.category,
        status: searchForm.status
      }
    })
    activities.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('Fetch activities error:', error)
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

// 状态相关
const getStatusType = (status) => {
  const types = {
    'pending': 'warning',
    'ongoing': 'success',
    'completed': 'info'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'pending': '未开始',
    'ongoing': '进行中',
    'completed': '已结束'
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
const handleSearch = () => {
  currentPage.value = 1
  fetchActivities()
}

const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.category = ''
  searchForm.status = ''
  handleSearch()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchActivities()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchActivities()
}

const handleView = (activity) => {
  currentActivity.value = activity
  dialogVisible.value = true
}

const handleCreate = () => {
  // TODO: 实现创建活动功能
}

const handleDelete = async (activity) => {
  try {
    await ElMessageBox.confirm('确定要删除这个活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/activities/${activity.id}/`)
    ElMessage.success('删除成功')
    fetchActivities()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Delete activity error:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleReserve = async () => {
  if (!currentActivity.value) return
  
  try {
    await axios.post('/api/activities/reservations/', {
      activity_id: currentActivity.value.id
    })
    ElMessage.success('预约成功')
    dialogVisible.value = false
  } catch (error) {
    console.error('Reserve activity error:', error)
    ElMessage.error('预约失败')
  }
}

// 计算属性
const canReserve = computed(() => {
  if (!currentActivity.value) return false
  return currentActivity.value.status === 'pending'
})

// 生命周期
onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
.activity-list {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-area {
  margin-bottom: 20px;
}

.activity-grid {
  margin-bottom: 20px;
}

.activity-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.activity-card:hover {
  transform: translateY(-5px);
}

.activity-image {
  height: 200px;
  width: 100%;
  display: block;
}

.activity-info {
  padding: 14px;
}

.activity-info h4 {
  margin: 0 0 10px;
  font-size: 16px;
}

.description {
  color: #666;
  font-size: 14px;
  margin: 10px 0;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.activity-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
}

.time {
  font-size: 13px;
  color: #999;
  display: flex;
  align-items: center;
  gap: 4px;
}

.activity-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
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

.detail-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style> 