<script setup>
import { ref, reactive, onMounted } from 'vue'
import { activityApi } from '../api/activities'
import { useRouter } from 'vue-router'

const router = useRouter()

// 活动列表
const activities = ref([])

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 8,
  total: 0
})

// 搜索条件
const searchForm = reactive({
  keyword: '',
  category: '',
  tags: [],
  dateRange: []
})

// 加载状态
const loading = ref(false)

// 分类选项
const categories = ref([])

// 标签选项
const tags = ref([])

// 获取活动列表
const fetchActivities = async () => {
  loading.value = true
  try {
    // 构建查询参数
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      search: searchForm.keyword || undefined,
      category: searchForm.category || undefined,
      tags: searchForm.tags.length ? searchForm.tags.join(',') : undefined,
      start_time_min: searchForm.dateRange?.[0] || undefined,
      start_time_max: searchForm.dateRange?.[1] || undefined
    }
    
    const response = await activityApi.getActivities(params)
    
    // 处理返回的数据
    let activityData = [];
    let totalCount = 0;
    
    if (Array.isArray(response.data)) {
      activityData = response.data;
      totalCount = response.data.length;
    } else if (response.data && response.data.results) {
      activityData = response.data.results;
      totalCount = response.data.count || 0;
    }
    
    // 标准化活动数据
    activities.value = activityData.map(activity => ({
      ...activity,
      id: activity.id || 0,
      title: activity.title || '',
      description: activity.description || '',
      location: activity.location || '',
      start_time: activity.start_time || new Date().toISOString(),
      end_time: activity.end_time || new Date().toISOString(),
      cover_image: getFullImageUrl(activity.cover_image),
      max_participants: activity.max_participants || 0,
      reservation_count: activity.reservation_count || 0,
      category: activity.category || { id: 0, name: '' },
      tags: Array.isArray(activity.tags) ? activity.tags : [],
      farmer: activity.farmer || { username: '' }
    }));
    
    pagination.total = totalCount;
    console.log('活动列表数据:', activities.value);
  } catch (error) {
    console.error('获取活动列表失败:', error)
    activities.value = [];
  } finally {
    loading.value = false
  }
}

// 添加图片URL处理函数
const getFullImageUrl = (imageUrl) => {
  if (!imageUrl) return 'https://via.placeholder.com/300x200?text=乡村活动';
  
  // 如果是完整URL，直接返回
  if (imageUrl.startsWith('http')) return imageUrl;
  
  // 如果是相对路径但没有以/开头，添加/
  if (!imageUrl.startsWith('/')) {
    imageUrl = '/' + imageUrl;
  }
  
  // 如果URL不包含域名，添加服务器地址
  return `http://localhost:8000${imageUrl}`;
};

// 获取分类
const fetchCategories = async () => {
  try {
    const response = await activityApi.getCategories()
    const data = Array.isArray(response.data) ? response.data : [];
    categories.value = data.map(category => ({
      id: category.id || 0,
      name: category.name || ''
    }));
    console.log('分类数据:', categories.value)
  } catch (error) {
    console.error('获取活动分类失败:', error)
    categories.value = [];
  }
}

// 获取标签
const fetchTags = async () => {
  try {
    const response = await activityApi.getTags()
    const data = Array.isArray(response.data) ? response.data : [];
    tags.value = data.map(tag => ({
      id: tag.id || 0,
      name: tag.name || ''
    }));
    console.log('标签数据:', tags.value)
  } catch (error) {
    console.error('获取标签失败:', error)
    tags.value = [];
  }
}

// 搜索活动
const handleSearch = () => {
  pagination.currentPage = 1
  fetchActivities()
}

// 重置搜索条件
const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.category = ''
  searchForm.tags = []
  searchForm.dateRange = []
  pagination.currentPage = 1
  fetchActivities()
}

// 处理分页变化
const handlePageChange = (page) => {
  pagination.currentPage = page
  fetchActivities()
}

// 跳转到活动详情
const goToActivityDetail = (activityId) => {
  router.push(`/activities/${activityId}`)
}

// 页面加载时获取数据
onMounted(() => {
  fetchActivities()
  fetchCategories()
  fetchTags()
})
</script>

<template>
  <div class="activities-page">
    <div class="page-header">
      <h1 class="page-title">乡村活动</h1>
      <p class="page-subtitle">探索丰富多彩的乡村体验活动，感受农耕文化的魅力</p>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form :model="searchForm" inline>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索活动名称或描述"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item label="活动分类">
          <el-select v-model="searchForm.category" placeholder="选择分类" clearable>
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="标签">
          <el-select v-model="searchForm.tags" placeholder="选择标签" multiple clearable>
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="loading">
            搜索
          </el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 活动列表 -->
    <div class="activities-container">
      <el-skeleton :rows="5" animated v-if="loading" />

      <div v-else-if="activities.length === 0" class="empty-data">
        <el-empty description="暂无活动数据" />
      </div>

      <el-row :gutter="20" v-else>
        <el-col
          v-for="activity in activities"
          :key="activity.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
          class="mb-20"
        >
          <el-card
            class="activity-card"
            shadow="hover"
            @click="goToActivityDetail(activity.id)"
          >
            <div class="activity-image-container">
              <img
                :src="activity.cover_image"
                class="activity-image"
                alt="活动图片"
              />
              <div class="activity-tags" v-if="activity.tags && activity.tags.length">
                <el-tag
                  v-for="tag in activity.tags"
                  :key="tag.id"
                  size="small"
                  effect="plain"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
            </div>

            <div class="activity-info">
              <h3 class="activity-title">{{ activity.title }}</h3>
              
              <p class="activity-meta">
                <el-icon><Calendar /></el-icon>
                {{ new Date(activity.start_time).toLocaleDateString() }}
              </p>
              
              <p class="activity-meta">
                <el-icon><Location /></el-icon>
                {{ activity.location }}
              </p>
              
              <p class="activity-description">{{ activity.description }}</p>
              
              <div class="activity-footer">
                <span class="activity-participants">
                  <el-icon><User /></el-icon>
                  已报名: {{ activity.reservation_count || 0 }}/{{ activity.max_participants }}
                </span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 分页 -->
      <div class="pagination-container" v-if="pagination.total > 0">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          layout="prev, pager, next"
          background
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.activities-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.page-subtitle {
  font-size: 1.1rem;
  color: var(--text-color-secondary);
}

.search-container {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.activity-card {
  height: 100%;
  cursor: pointer;
  transition: transform 0.3s;
}

.activity-card:hover {
  transform: translateY(-5px);
}

.activity-image-container {
  position: relative;
}

.activity-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
}

.activity-tags {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.activity-info {
  padding: 15px 0 0;
}

.activity-title {
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-weight: 600;
}

.activity-meta {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.activity-meta .el-icon {
  margin-right: 5px;
}

.activity-description {
  margin: 8px 0;
  color: var(--text-color-secondary);
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.activity-footer {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-participants {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: var(--info-color);
}

.activity-participants .el-icon {
  margin-right: 5px;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style> 