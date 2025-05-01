<template>
  <div class="tourist-activities">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>活动列表</h3>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="活动名称">
            <el-input v-model="searchForm.name" placeholder="请输入活动名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="未开始" value="upcoming" />
              <el-option label="进行中" value="ongoing" />
              <el-option label="已结束" value="ended" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 活动列表 -->
      <el-row :gutter="20">
        <el-col :span="8" v-for="activity in activities" :key="activity.id">
          <el-card class="activity-card" :body-style="{ padding: '0px' }">
            <img :src="activity.image" class="activity-image" />
            <div class="activity-info">
              <h3>{{ activity.name }}</h3>
              <p class="description">{{ activity.description }}</p>
              <div class="activity-details">
                <p><el-icon><Calendar /></el-icon> 开始时间：{{ activity.start_time }}</p>
                <p><el-icon><Calendar /></el-icon> 结束时间：{{ activity.end_time }}</p>
                <p><el-icon><User /></el-icon> 参与人数：{{ activity.current_participants }}/{{ activity.max_participants }}</p>
                <p>
                  <el-tag :type="getStatusType(activity.status)">
                    {{ getStatusName(activity.status) }}
                  </el-tag>
                </p>
              </div>
              <div class="activity-actions">
                <el-button 
                  type="primary" 
                  @click="handleViewDetails(activity)"
                >查看详情</el-button>
                <el-button 
                  v-if="activity.status === 'upcoming' && activity.current_participants < activity.max_participants"
                  type="success" 
                  @click="handleRegister(activity)"
                >立即报名</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[6, 12, 18, 24]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 活动详情对话框 -->
    <el-dialog
      title="活动详情"
      v-model="detailsVisible"
      width="800px"
    >
      <div v-if="currentActivity">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="活动名称">{{ currentActivity.name }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentActivity.status)">
              {{ getStatusName(currentActivity.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ currentActivity.start_time }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ currentActivity.end_time }}</el-descriptions-item>
          <el-descriptions-item label="最大参与人数">{{ currentActivity.max_participants }}</el-descriptions-item>
          <el-descriptions-item label="当前参与人数">{{ currentActivity.current_participants }}</el-descriptions-item>
        </el-descriptions>

        <h4>活动描述</h4>
        <p>{{ currentActivity.description }}</p>

        <h4>活动图片</h4>
        <el-image 
          :src="currentActivity.image" 
          :preview-src-list="[currentActivity.image]"
          fit="cover"
          style="width: 100%; max-height: 400px;"
        />

        <div class="dialog-footer">
          <el-button 
            v-if="currentActivity.status === 'upcoming' && currentActivity.current_participants < currentActivity.max_participants"
            type="primary" 
            @click="handleRegister(currentActivity)"
          >立即报名</el-button>
          <el-button @click="detailsVisible = false">关闭</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, User } from '@element-plus/icons-vue'

const store = useStore()
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(6)
const detailsVisible = ref(false)
const currentActivity = ref(null)

// 搜索表单
const searchForm = ref({
  name: '',
  status: ''
})

// 从 store 获取活动列表
const activities = computed(() => store.state.activity.activities)
const total = computed(() => store.state.activity.total)

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    upcoming: 'warning',
    ongoing: 'success',
    ended: 'info'
  }
  return types[status] || 'info'
}

// 获取状态名称
const getStatusName = (status) => {
  const names = {
    upcoming: '未开始',
    ongoing: '进行中',
    ended: '已结束'
  }
  return names[status] || status
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchActivities()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    name: '',
    status: ''
  }
  handleSearch()
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchActivities()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchActivities()
}

// 查看活动详情
const handleViewDetails = (activity) => {
  currentActivity.value = activity
  detailsVisible.value = true
}

// 报名活动
const handleRegister = async (activity) => {
  try {
    await ElMessageBox.confirm('确定要报名参加该活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await store.dispatch('activity/registerActivity', activity.id)
    ElMessage.success('报名成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('报名失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取活动列表
const fetchActivities = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      ...searchForm.value
    }
    
    await store.dispatch('activity/fetchActivities', params)
  } catch (error) {
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
.tourist-activities {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  margin-bottom: 20px;
}

.activity-card {
  margin-bottom: 20px;
}

.activity-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.activity-info {
  padding: 14px;
}

.activity-info h3 {
  margin: 0 0 10px;
  font-size: 16px;
}

.description {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.activity-details {
  margin-bottom: 10px;
}

.activity-details p {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}

.activity-details .el-icon {
  margin-right: 5px;
}

.activity-actions {
  display: flex;
  justify-content: space-between;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

h4 {
  margin: 20px 0 10px;
  font-weight: 500;
}

.dialog-footer {
  margin-top: 20px;
  text-align: right;
}
</style> 