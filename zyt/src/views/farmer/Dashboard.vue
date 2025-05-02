<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { activityApi } from '../../api/activities'
import { productApi } from '../../api/products'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 当前活动标签
const activeTab = ref('activities')

// 活动列表
const activities = ref([])

// 产品列表
const products = ref([])

// 加载状态
const activitiesLoading = ref(true)
const productsLoading = ref(true)

// 格式化价格的辅助函数
const formatPrice = (price) => {
  // 确保价格是数字类型
  const numPrice = typeof price === 'number' ? price : 
                  (typeof price === 'string' ? parseFloat(price) || 0 : 0);
  return numPrice.toFixed(2);
}

// 获取农场主发布的活动
const fetchFarmerActivities = async () => {
  activitiesLoading.value = true
  try {
    const response = await activityApi.getFarmerActivities()
    activities.value = response.data || []
  } catch (error) {
    console.error('获取活动列表失败:', error)
    ElMessage.error('获取活动列表失败')
  } finally {
    activitiesLoading.value = false
  }
}

// 获取农场主发布的产品
const fetchFarmerProducts = async () => {
  productsLoading.value = true
  try {
    const response = await productApi.getFarmerProducts()
    products.value = response.data || []
  } catch (error) {
    console.error('获取产品列表失败:', error)
    ElMessage.error('获取产品列表失败')
  } finally {
    productsLoading.value = false
  }
}

// 切换到创建活动页面
const createActivity = () => {
  router.push('/farmer/activities/create')
}

// 编辑活动
const editActivity = (activityId) => {
  router.push(`/farmer/activities/edit/${activityId}`)
}

// 查看活动详情
const viewActivity = (activityId) => {
  router.push(`/activities/${activityId}`)
}

// 删除活动
const deleteActivity = async (activityId) => {
  ElMessageBox.confirm(
    '确定要删除此活动吗？删除后无法恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await activityApi.deleteActivity(activityId)
      ElMessage.success('活动已删除')
      // 刷新活动列表
      fetchFarmerActivities()
    } catch (error) {
      console.error('删除活动失败:', error)
      ElMessage.error('删除活动失败')
    }
  }).catch(() => {})
}

// 切换到创建产品页面
const createProduct = () => {
  router.push('/farmer/products/create')
}

// 编辑产品
const editProduct = (productId) => {
  router.push(`/farmer/products/edit/${productId}`)
}

// 查看产品详情
const viewProduct = (productId) => {
  router.push(`/products/${productId}`)
}

// 删除产品
const deleteProduct = async (productId) => {
  ElMessageBox.confirm(
    '确定要删除此产品吗？删除后无法恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await productApi.deleteProduct(productId)
      ElMessage.success('产品已删除')
      // 刷新产品列表
      fetchFarmerProducts()
    } catch (error) {
      console.error('删除产品失败:', error)
      ElMessage.error('删除产品失败')
    }
  }).catch(() => {})
}

// 页面加载时获取数据
onMounted(() => {
  fetchFarmerActivities()
  fetchFarmerProducts()
})
</script>

<template>
  <div class="farmer-dashboard">
    <h1 class="page-title">农户管理中心 - 农产品与活动发布平台</h1>
    
    <div class="dashboard-intro">
      <el-alert type="info" show-icon :closable="false">
        <strong>欢迎，农户用户！</strong> 这是您专属的管理平台，在这里您可以管理您发布的乡村活动和农产品。
      </el-alert>
    </div>
    
    <el-tabs v-model="activeTab" class="dashboard-tabs">
      <!-- 活动管理标签页 -->
      <el-tab-pane label="活动管理" name="activities">
        <div class="tab-header">
          <h2 class="tab-title">我发布的活动</h2>
          <el-button type="primary" @click="createActivity">
            <el-icon><Plus /></el-icon>
            创建新活动
          </el-button>
        </div>
        
        <el-skeleton :rows="5" animated v-if="activitiesLoading" />
        
        <div v-else-if="!activities.length" class="empty-data">
          <el-empty description="暂无发布的活动">
            <el-button type="primary" @click="createActivity">创建第一个活动</el-button>
          </el-empty>
        </div>
        
        <el-table v-else :data="activities" style="width: 100%" border>
          <el-table-column prop="title" label="活动名称" min-width="150">
            <template #default="{ row }">
              <el-link type="primary" @click="viewActivity(row.id)">
                {{ row.title }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column prop="start_time" label="开始时间" width="180">
            <template #default="{ row }">
              {{ new Date(row.start_time).toLocaleString() }}
            </template>
          </el-table-column>
          
          <el-table-column prop="end_time" label="结束时间" width="180">
            <template #default="{ row }">
              {{ new Date(row.end_time).toLocaleString() }}
            </template>
          </el-table-column>
          
          <el-table-column prop="location" label="地点" min-width="120" />
          
          <el-table-column prop="max_participants" label="人数上限" width="100" />
          
          <el-table-column prop="reservation_count" label="已预约" width="100" />
          
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag 
                :type="new Date(row.end_time) < new Date() ? 'info' : 
                      (row.reservation_count >= row.max_participants ? 'danger' : 'success')"
              >
                {{ new Date(row.end_time) < new Date() ? '已结束' : 
                   (row.reservation_count >= row.max_participants ? '已满' : '可预约') }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="180">
            <template #default="{ row }">
              <el-button 
                size="small" 
                @click="viewActivity(row.id)"
              >
                查看
              </el-button>
              <el-button 
                type="primary" 
                size="small" 
                @click="editActivity(row.id)"
              >
                编辑
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="deleteActivity(row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <!-- 产品管理标签页 -->
      <el-tab-pane label="产品管理" name="products">
        <div class="tab-header">
          <h2 class="tab-title">我的农产品</h2>
          <el-button type="primary" @click="createProduct">
            <el-icon><Plus /></el-icon>
            添加新产品
          </el-button>
        </div>
        
        <el-skeleton :rows="5" animated v-if="productsLoading" />
        
        <div v-else-if="!products.length" class="empty-data">
          <el-empty description="暂无发布的产品">
            <el-button type="primary" @click="createProduct">添加第一个产品</el-button>
          </el-empty>
        </div>
        
        <el-table v-else :data="products" style="width: 100%" border>
          <el-table-column label="产品图片" width="100">
            <template #default="{ row }">
              <el-image 
                :src="row.images && row.images.length > 0 ? row.images[0].image : 'https://via.placeholder.com/50x50'"
                style="width: 50px; height: 50px"
                fit="cover"
              />
            </template>
          </el-table-column>
          
          <el-table-column prop="name" label="产品名称" min-width="150">
            <template #default="{ row }">
              <el-link type="primary" @click="viewProduct(row.id)">
                {{ row.name }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column prop="price" label="价格" width="100">
            <template #default="{ row }">
              ¥{{ formatPrice(row.price) }}
            </template>
          </el-table-column>
          
          <el-table-column prop="stock" label="库存" width="100" />
          
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag 
                :type="row.status === 'available' ? 'success' : 
                      (row.status === 'sold_out' ? 'danger' : 'info')"
              >
                {{ row.status === 'available' ? '在售' : 
                   (row.status === 'sold_out' ? '售罄' : '已下架') }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="销量" width="100">
            <template #default="{ row }">
              {{ row.sales_count || 0 }}
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="180">
            <template #default="{ row }">
              <el-button 
                size="small" 
                @click="viewProduct(row.id)"
              >
                查看
              </el-button>
              <el-button 
                type="primary" 
                size="small" 
                @click="editProduct(row.id)"
              >
                编辑
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="deleteProduct(row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.farmer-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-align: center;
}

.dashboard-tabs {
  margin-top: 20px;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tab-title {
  font-size: 1.3rem;
  margin: 0;
}

.empty-data {
  margin: 50px 0;
  text-align: center;
}
</style> 