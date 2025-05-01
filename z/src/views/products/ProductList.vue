<template>
  <div class="product-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>农特产品</h3>
          <el-button 
            v-if="userRole === 'farmer' || userRole === 'admin'"
            type="primary" 
            @click="handleAddProduct"
          >
            发布产品
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="关键词">
            <el-input
              v-model="searchForm.keyword"
              placeholder="产品名称/描述"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="searchForm.category" placeholder="全部分类" clearable>
              <el-option
                v-for="item in categories"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="价格区间">
            <el-input-number
              v-model="searchForm.minPrice"
              :min="0"
              placeholder="最低价"
              style="width: 130px"
            />
            <span class="mx-2">-</span>
            <el-input-number
              v-model="searchForm.maxPrice"
              :min="0"
              placeholder="最高价"
              style="width: 130px"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 产品列表 -->
      <div class="product-grid" v-loading="loading">
        <el-row :gutter="20">
          <el-col 
            v-for="product in products" 
            :key="product.id" 
            :xs="24" 
            :sm="12" 
            :md="8" 
            :lg="6"
            class="mb-4"
          >
            <el-card :body-style="{ padding: '0px' }" class="product-card">
              <el-image
                :src="product.image || '/default-product.jpg'"
                class="product-image"
                fit="cover"
                @click="handleViewProduct(product)"
              />
              <div class="product-info">
                <h4 class="product-title" @click="handleViewProduct(product)">
                  {{ product.name }}
                </h4>
                <div class="product-price">
                  ¥{{ product.price.toFixed(2) }}
                </div>
                <div class="product-meta">
                  <el-tag size="small">{{ product.category }}</el-tag>
                  <span class="product-sales">销量: {{ product.sales_count }}</span>
                </div>
                <div class="product-actions">
                  <el-button 
                    type="primary" 
                    size="small"
                    @click="handleAddToCart(product)"
                  >
                    加入购物车
                  </el-button>
                  <el-button
                    v-if="canManageProduct(product)"
                    type="warning"
                    size="small"
                    @click="handleEditProduct(product)"
                  >
                    编辑
                  </el-button>
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

      <!-- 产品详情对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'view' ? '产品详情' : (dialogType === 'add' ? '发布产品' : '编辑产品')"
        width="60%"
        destroy-on-close
      >
        <product-form
          v-if="dialogType !== 'view'"
          :product="currentProduct"
          @submit="handleProductSubmit"
          @cancel="dialogVisible = false"
        />
        <product-detail
          v-else
          :product="currentProduct"
          @add-to-cart="handleAddToCart"
        />
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import ProductForm from '@/components/products/ProductForm.vue'
import ProductDetail from '@/components/products/ProductDetail.vue'

const store = useStore()
const userRole = computed(() => store.state.user.role)

// 数据
const loading = ref(false)
const products = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const dialogVisible = ref(false)
const dialogType = ref('view') // 'view', 'add', 'edit'
const currentProduct = ref(null)

const searchForm = ref({
  keyword: '',
  category: '',
  minPrice: null,
  maxPrice: null
})

const categories = [
  { label: '水果', value: 'fruits' },
  { label: '蔬菜', value: 'vegetables' },
  { label: '粮食', value: 'grains' },
  { label: '特产', value: 'specialties' },
  { label: '其他', value: 'others' }
]

// 获取产品列表
const fetchProducts = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/products/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        keyword: searchForm.value.keyword,
        category: searchForm.value.category,
        min_price: searchForm.value.minPrice,
        max_price: searchForm.value.maxPrice
      }
    })
    products.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('Fetch products error:', error)
    ElMessage.error('获取产品列表失败')
  } finally {
    loading.value = false
  }
}

// 事件处理
const handleSearch = () => {
  currentPage.value = 1
  fetchProducts()
}

const handleReset = () => {
  searchForm.value = {
    keyword: '',
    category: '',
    minPrice: null,
    maxPrice: null
  }
  handleSearch()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchProducts()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchProducts()
}

const handleViewProduct = (product) => {
  currentProduct.value = product
  dialogType.value = 'view'
  dialogVisible.value = true
}

const handleAddProduct = () => {
  currentProduct.value = null
  dialogType.value = 'add'
  dialogVisible.value = true
}

const handleEditProduct = (product) => {
  currentProduct.value = product
  dialogType.value = 'edit'
  dialogVisible.value = true
}

const handleProductSubmit = async (formData) => {
  try {
    if (dialogType.value === 'add') {
      await axios.post('/api/products/', formData)
      ElMessage.success('发布产品成功')
    } else {
      await axios.put(`/api/products/${currentProduct.value.id}/`, formData)
      ElMessage.success('更新产品成功')
    }
    dialogVisible.value = false
    fetchProducts()
  } catch (error) {
    console.error('Submit product error:', error)
    ElMessage.error(dialogType.value === 'add' ? '发布产品失败' : '更新产品失败')
  }
}

const handleAddToCart = async (product) => {
  try {
    await store.dispatch('cart/addToCart', {
      product_id: product.id,
      quantity: 1
    })
    ElMessage.success('已添加到购物车')
  } catch (error) {
    console.error('Add to cart error:', error)
    ElMessage.error('添加到购物车失败')
  }
}

const canManageProduct = (product) => {
  if (userRole.value === 'admin') return true
  if (userRole.value === 'farmer' && product.farmer_id === store.state.user.id) return true
  return false
}

// 生命周期
onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.product-list {
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

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.product-grid {
  margin-bottom: 20px;
}

.product-card {
  height: 100%;
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  cursor: pointer;
}

.product-info {
  padding: 14px;
}

.product-title {
  margin: 0;
  font-size: 16px;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-title:hover {
  color: var(--el-color-primary);
}

.product-price {
  margin: 8px 0;
  color: #ff6b6b;
  font-size: 18px;
  font-weight: bold;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.product-sales {
  color: #999;
  font-size: 14px;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.mx-2 {
  margin: 0 8px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style> 