<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { activityApi } from '../api/activities'
import { productApi } from '../api/products'
import { ChatDotRound } from '@element-plus/icons-vue'

// 数据加载状态
const loading = ref({
  activities: true,
  products: true
})

// 热门活动列表
const featuredActivities = ref([])

// 推荐产品列表
const featuredProducts = ref([])

// 获取热门活动
const fetchFeaturedActivities = async () => {
  loading.value.activities = true
  try {
    const response = await activityApi.getActivities({ featured: true, limit: 4 })
    const data = Array.isArray(response.data) ? response.data : []
    
    // 格式化每个活动数据
    featuredActivities.value = data.map(activity => ({
      ...activity,
      id: activity.id || 0,
      title: activity.title || '',
      location: activity.location || '',
      start_time: activity.start_time || new Date().toISOString(),
      cover_image: activity.cover_image || ''
    }))
    
    console.log('活动数据:', featuredActivities.value)
  } catch (error) {
    console.error('获取热门活动失败:', error)
    featuredActivities.value = []
  } finally {
    loading.value.activities = false
  }
}

// 获取推荐产品
const fetchFeaturedProducts = async () => {
  loading.value.products = true
  try {
    const response = await productApi.getProducts({ featured: true, limit: 4 })
    const data = Array.isArray(response.data) ? response.data : []
    
    // 格式化每个产品数据
    featuredProducts.value = data.map(product => ({
      ...product,
      id: product.id || 0,
      name: product.name || '',
      price: typeof product.price === 'number' ? product.price : 
             (typeof product.price === 'string' ? parseFloat(product.price) || 0 : 0),
      description: product.description || '',
      images: Array.isArray(product.images) ? product.images : []
    }))
    
    console.log('产品数据:', featuredProducts.value)
  } catch (error) {
    console.error('获取推荐产品失败:', error)
    featuredProducts.value = []
  } finally {
    loading.value.products = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchFeaturedActivities()
  fetchFeaturedProducts()
})
</script>

<template>
  <div class="home-page">
    <!-- 顶部横幅 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">发现乡村之美</h1>
        <p class="hero-subtitle">体验农村生活，品尝新鲜农产品，参与乡村活动</p>
        
        <div class="hero-actions">
          <router-link to="/activities">
            <el-button type="primary" size="large">
              探索乡村活动
            </el-button>
          </router-link>
          <router-link to="/products">
            <el-button type="success" size="large">
              浏览农产品
            </el-button>
          </router-link>
          <router-link to="/ai-assistant">
            <el-button type="info" size="large">
              <el-icon><ChatDotRound /></el-icon> AI乡村助手
            </el-button>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 角色区分提示 -->
    <div class="role-info-section">
      <el-divider>用户角色说明</el-divider>
      
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12">
          <el-card class="role-card">
            <template #header>
              <div class="card-header">
                <h3>游客用户</h3>
              </div>
            </template>
            <div class="role-features">
              <p><el-icon><Check /></el-icon> 浏览所有乡村活动和农产品</p>
              <p><el-icon><Check /></el-icon> 预约参加乡村活动</p>
              <p><el-icon><Check /></el-icon> 购买农产品</p>
              <p><el-icon><Check /></el-icon> 评价活动和产品</p>
              <p><el-icon><Close /></el-icon> 无法发布活动和产品</p>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12">
          <el-card class="role-card">
            <template #header>
              <div class="card-header">
                <h3>农户用户</h3>
              </div>
            </template>
            <div class="role-features">
              <p><el-icon><Check /></el-icon> 发布乡村活动</p>
              <p><el-icon><Check /></el-icon> 发布农产品</p>
              <p><el-icon><Check /></el-icon> 管理活动预约</p>
              <p><el-icon><Check /></el-icon> 管理产品销售</p>
              <p><el-icon><Check /></el-icon> 查看活动和产品统计数据</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <div class="register-cta">
        <p>还没有账号？立即注册选择您的角色！</p>
        <router-link to="/register">
          <el-button type="primary">注册账号</el-button>
        </router-link>
      </div>
    </div>

    <!-- 我们的特色 -->
    <section class="features-section">
      <h2 class="section-title text-center">我们的特色</h2>
      <div class="features-container">
        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><Calendar /></el-icon>
          </div>
          <h3>多样的乡村活动</h3>
          <p>探索丰富多彩的乡村活动，从农作物采摘到传统工艺学习，应有尽有</p>
        </div>
        
        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><ShoppingBag /></el-icon>
          </div>
          <h3>优质农产品</h3>
          <p>直接从农场到餐桌，为您提供新鲜、健康、无污染的优质农产品</p>
        </div>
        
        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><House /></el-icon>
          </div>
          <h3>地道乡村体验</h3>
          <p>体验真实的乡村生活，感受纯朴民风，远离城市喧嚣</p>
        </div>
        
        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <h3>AI乡村助手</h3>
          <p>智能助手为您解答关于乡村旅游、农产品和活动的各类问题，提供个性化建议</p>
        </div>
      </div>
    </section>

    <!-- 热门活动 -->
    <section class="featured-activities">
      <h2 class="section-title">热门活动</h2>
      
      <el-skeleton :rows="3" animated :loading="loading.activities" v-if="loading.activities" />
      
      <div v-else>
        <div v-if="featuredActivities.length === 0" class="empty-data">
          <el-empty description="暂无活动数据" />
        </div>
        
        <el-row :gutter="20" v-else>
          <el-col :xs="24" :sm="12" :md="6" v-for="activity in featuredActivities" :key="activity.id" class="mb-20">
            <RouterLink :to="`/activities/${activity.id}`">
              <el-card class="activity-card" shadow="hover">
                <img 
                  :src="activity.cover_image || 'https://via.placeholder.com/300x200?text=乡村活动'" 
                  class="activity-image responsive-img"
                />
                <div class="activity-info">
                  <h3>{{ activity.title }}</h3>
                  <p class="activity-location">
                    <el-icon><Location /></el-icon>
                    {{ activity.location }}
                  </p>
                  <p class="activity-time">
                    <el-icon><Timer /></el-icon>
                    {{ new Date(activity.start_time).toLocaleDateString() }}
                  </p>
                </div>
              </el-card>
            </RouterLink>
          </el-col>
        </el-row>
        
        <div class="text-center mt-20">
          <RouterLink to="/activities">
            <el-button type="primary">查看全部活动</el-button>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- 推荐产品 -->
    <section class="featured-products">
      <h2 class="section-title">推荐产品</h2>
      
      <el-skeleton :rows="3" animated :loading="loading.products" v-if="loading.products" />
      
      <div v-else>
        <div v-if="featuredProducts.length === 0" class="empty-data">
          <el-empty description="暂无产品数据" />
        </div>
        
        <el-row :gutter="20" v-else>
          <el-col :xs="24" :sm="12" :md="6" v-for="product in featuredProducts" :key="product.id" class="mb-20">
            <RouterLink :to="`/products/${product.id}`">
              <el-card class="product-card" shadow="hover">
                <img 
                  :src="product.images && product.images.length > 0 ? product.images[0].image : 'https://via.placeholder.com/300x200?text=农产品'" 
                  class="product-image responsive-img"
                />
                <div class="product-info">
                  <h3>{{ product.name }}</h3>
                  <p class="product-price">¥{{ typeof product.price === 'number' ? product.price.toFixed(2) : product.price }}</p>
                </div>
              </el-card>
            </RouterLink>
          </el-col>
        </el-row>
        
        <div class="text-center mt-20">
          <RouterLink to="/products">
            <el-button type="success">浏览更多产品</el-button>
          </RouterLink>
        </div>
      </div>
    </section>
    
    <!-- 加入我们 -->
    <section class="join-us-section">
      <div class="join-us-content">
        <h2>加入我们，一起创造美好乡村</h2>
        <p>无论您是游客还是农产品提供者，我们都欢迎您的加入</p>
        <div class="join-buttons">
          <RouterLink to="/register">
            <el-button type="primary" size="large">现在注册</el-button>
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  width: 100%;
}

/* 顶部横幅 */
.hero-section {
  height: 500px;
  background-image: url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1332&q=80');
  background-size: cover;
  background-position: center;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
}

.hero-content {
  z-index: 1;
  max-width: 800px;
  padding: 0 20px;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 30px;
}

.hero-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

/* 特色部分 */
.features-section {
  padding: 60px 20px;
  background-color: #fff;
}

.features-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-item {
  flex: 1;
  min-width: 300px;
  padding: 20px;
  margin: 10px;
  text-align: center;
}

.feature-icon {
  font-size: 3rem;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.feature-item h3 {
  margin-bottom: 15px;
}

/* 活动和产品部分 */
.featured-activities,
.featured-products {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.featured-activities {
  background-color: #f5f5f5;
}

.activity-card,
.product-card {
  height: 100%;
  transition: transform 0.3s;
}

.activity-card:hover,
.product-card:hover {
  transform: translateY(-5px);
}

.activity-image,
.product-image {
  height: 200px;
  object-fit: cover;
  width: 100%;
}

.activity-info,
.product-info {
  padding: 15px 0;
}

.activity-location,
.activity-time,
.product-price {
  display: flex;
  align-items: center;
  color: var(--text-color-secondary);
  margin-top: 8px;
}

.activity-location .el-icon,
.activity-time .el-icon {
  margin-right: 5px;
}

.product-price {
  color: #f56c6c;
  font-weight: bold;
  font-size: 1.2rem;
}

/* 加入我们 */
.join-us-section {
  background-image: url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1332&q=80');
  background-size: cover;
  background-position: center;
  color: white;
  padding: 80px 20px;
  text-align: center;
  position: relative;
}

.join-us-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
}

.join-us-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.join-us-content h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.join-us-content p {
  margin-bottom: 30px;
  font-size: 1.1rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .hero-section {
    height: 400px;
  }
  
  .hero-content h1 {
    font-size: 1.8rem;
  }
  
  .hero-content p {
    font-size: 1rem;
  }
  
  .feature-item {
    min-width: 100%;
  }
}

.role-info-section {
  max-width: 1000px;
  margin: 40px auto;
  padding: 20px;
}

.role-card {
  height: 100%;
  margin-bottom: 20px;
}

.role-features {
  text-align: left;
}

.role-features p {
  margin: 10px 0;
  display: flex;
  align-items: center;
}

.role-features .el-icon {
  margin-right: 10px;
}

.role-features .el-icon.Check {
  color: #67C23A;
}

.role-features .el-icon.Close {
  color: #F56C6C;
}

.register-cta {
  margin-top: 30px;
  text-align: center;
}

.register-cta p {
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.3rem;
}
</style> 