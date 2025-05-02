<script setup>
import { ref, reactive, onMounted } from 'vue'
import { productApi } from '../api/products'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import { ShoppingCart } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 产品列表
const products = ref([])

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 8,
  total: 0
})

// 搜索条件
const searchForm = reactive({
  keyword: '',
  priceRange: [],
  farmer_id: '',
})

// 加载状态
const loading = ref(false)

// 添加到购物车加载状态
const addToCartLoading = ref({})

// 获取产品列表
const fetchProducts = async () => {
  loading.value = true
  try {
    // 构建查询参数
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      search: searchForm.keyword || undefined,
      min_price: searchForm.priceRange?.[0] || undefined,
      max_price: searchForm.priceRange?.[1] || undefined,
      farmer_id: searchForm.farmer_id || undefined,
    }
    
    const response = await productApi.getProducts(params)
    console.log('产品列表原始响应:', response.data);
    
    // 处理返回的数据
    let productData = [];
    let totalCount = 0;
    
    if (Array.isArray(response.data)) {
      productData = response.data;
      totalCount = response.data.length;
    } else if (response.data && response.data.results) {
      productData = response.data.results;
      totalCount = response.data.count || 0;
    }
    
    // 标准化产品数据
    products.value = productData.map(product => {
      const normalizedProduct = {
        ...product,
        id: product.id || 0,
        name: product.name || '',
        price: typeof product.price === 'number' ? product.price : 
               (typeof product.price === 'string' ? parseFloat(product.price) || 0 : 0),
        stock: product.stock || 0,
        status: product.status || 'available',  // 默认为可用
        description: product.description || '',
        images: Array.isArray(product.images) ? product.images : [],
        farmer: product.farmer || { username: '' }
      };
      return normalizedProduct;
    });
    
    pagination.total = totalCount;
    console.log('处理后的产品列表数据:', products.value);
  } catch (error) {
    console.error('获取产品列表失败:', error)
    ElMessage.error('获取产品列表失败')
    products.value = [];
  } finally {
    loading.value = false
  }
}

// 搜索产品
const handleSearch = () => {
  pagination.currentPage = 1
  fetchProducts()
}

// 重置搜索条件
const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.priceRange = []
  searchForm.farmer_id = ''
  pagination.currentPage = 1
  fetchProducts()
}

// 处理分页变化
const handlePageChange = (page) => {
  pagination.currentPage = page
  fetchProducts()
}

// 跳转到产品详情
const goToProductDetail = (productId) => {
  router.push(`/products/${productId}`)
}

// 判断产品是否可购买
const isProductAvailable = (product) => {
  // 1. 必须有库存大于0
  // 2. 必须状态为available或published
  const displayStock = product.stock || 0;
  
  // 有库存并且状态为可用才能购买
  return displayStock > 0 && 
         (product.status === 'available' || 
          product.status === 'published');
}

// 添加到购物车
const addToCart = async (product, event) => {
  event.stopPropagation()
  
  console.log('尝试添加到购物车:', product);
  console.log('产品状态:', product.status);
  console.log('产品库存:', product.stock);
  console.log('可购买状态:', isProductAvailable(product));
  
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后再添加到购物车')
    router.push({ path: '/login', query: { redirect: '/products' }})
    return
  }
  
  addToCartLoading.value[product.id] = true
  
  try {
    await productApi.addToCart(product.id, 1)
    ElMessage.success('添加到购物车成功')
  } catch (error) {
    console.error('添加到购物车失败:', error)
    ElMessage.error('添加到购物车失败')
  } finally {
    addToCartLoading.value[product.id] = false
  }
}

// 添加价格格式化函数
const formatPrice = (price) => {
  const numPrice = typeof price === 'number' ? price : parseFloat(price) || 0;
  return numPrice.toFixed(2);
}

// 页面加载时获取数据
onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <div class="products-page">
    <div class="page-header">
      <h1 class="page-title">农产品</h1>
      <p class="page-subtitle">精选新鲜农产品，从田间到餐桌的美味享受</p>
      
      <div class="role-notice">
        <el-alert type="info" show-icon :closable="false">
          <template #title>
            <span>注意：农产品由农户用户发布，游客用户可以浏览和购买产品。如果您是农户，可以在<router-link to="/farmer/dashboard" class="alert-link">农户管理中心</router-link>发布产品。</span>
          </template>
        </el-alert>
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form :model="searchForm" inline>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索产品名称或描述"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item label="价格范围">
          <el-slider
            v-model="searchForm.priceRange"
            range
            :min="0"
            :max="1000"
            :step="10"
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

    <!-- 产品列表 -->
    <div class="products-container">
      <el-skeleton :rows="5" animated v-if="loading" />

      <div v-else-if="products.length === 0" class="empty-data">
        <el-empty description="暂无产品数据" />
      </div>

      <el-row :gutter="20" v-else>
        <el-col
          v-for="product in products"
          :key="product.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
          class="mb-20"
        >
          <el-card
            class="product-card"
            shadow="hover"
            @click="goToProductDetail(product.id)"
          >
            <div class="product-image-container">
              <img
                :src="product.images && product.images.length > 0 ? product.images[0].image : 'https://via.placeholder.com/300x200?text=农产品'"
                class="product-image"
                alt="产品图片"
              />
              <div class="product-status" v-if="product.status !== 'available' && product.status !== 'published'">
                <el-tag type="danger" effect="dark">
                  {{ product.status === 'sold_out' ? '已售罄' : '已下架' }}
                </el-tag>
              </div>
            </div>

            <div class="product-info">
              <h3 class="product-title">{{ product.name }}</h3>
              
              <div class="product-price-row">
                <span class="product-price">¥{{ formatPrice(product.price) }}</span>
                <span class="product-stock" v-if="product.stock > 0">
                  库存: {{ product.stock }}
                </span>
              </div>
              
              <p class="product-description">{{ product.description }}</p>
              
              <div class="product-footer">
                <span class="product-farmer" v-if="product.farmer">
                  <el-icon><UserFilled /></el-icon>
                  {{ product.farmer.username }}
                </span>
                
                <el-button
                  type="primary"
                  size="small"
                  :icon="ShoppingCart"
                  circle
                  :loading="addToCartLoading[product.id]"
                  :disabled="!isProductAvailable(product)"
                  @click.stop="addToCart(product, $event)"
                  title="添加到购物车"
                />
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
.products-page {
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
  color: var(--secondary-color);
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

.product-card {
  height: 100%;
  cursor: pointer;
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image-container {
  position: relative;
}

.product-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
}

.product-status {
  position: absolute;
  top: 10px;
  right: 10px;
}

.product-info {
  padding: 15px 0 0;
}

.product-title {
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-weight: 600;
}

.product-price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.product-price {
  color: #f56c6c;
  font-size: 1.3rem;
  font-weight: bold;
}

.product-stock {
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.product-description {
  margin: 8px 0;
  color: var(--text-color-secondary);
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-footer {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-farmer {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: var(--info-color);
}

.product-farmer .el-icon {
  margin-right: 5px;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style> 