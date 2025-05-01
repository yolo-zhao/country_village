<template>
  <div class="tourist-favorites">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>我的收藏</h3>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="商品名称">
            <el-input v-model="searchForm.name" placeholder="请输入商品名称" clearable />
          </el-form-item>
          <el-form-item label="商品类别">
            <el-select v-model="searchForm.category" placeholder="请选择类别" clearable>
              <el-option label="水果" value="fruit" />
              <el-option label="蔬菜" value="vegetable" />
              <el-option label="粮食" value="grain" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 收藏列表 -->
      <el-row :gutter="20">
        <el-col v-for="item in favorites" :key="item.id" :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="product-card" shadow="hover">
            <el-image
              :src="item.image"
              fit="cover"
              class="product-image"
              @click="handleViewProduct(item)"
            >
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
            <div class="product-info">
              <h4 class="product-name" @click="handleViewProduct(item)">{{ item.name }}</h4>
              <p class="product-price">¥{{ item.price.toFixed(2) }}</p>
              <p class="product-farmer">农户：{{ item.farmer_name }}</p>
              <div class="product-actions">
                <el-button type="primary" @click="handleAddToCart(item)">加入购物车</el-button>
                <el-button type="danger" @click="handleRemove(item)">取消收藏</el-button>
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
          :page-sizes="[12, 24, 36, 48]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

// 搜索表单
const searchForm = ref({
  name: '',
  category: ''
})

// 从 store 获取收藏列表
const favorites = computed(() => store.state.favorite.favorites)

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchFavorites()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    name: '',
    category: ''
  }
  handleSearch()
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchFavorites()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchFavorites()
}

// 查看商品详情
const handleViewProduct = (product) => {
  router.push(`/products/${product.id}`)
}

// 加入购物车
const handleAddToCart = async (product) => {
  try {
    loading.value = true
    await store.dispatch('cart/addToCart', {
      product_id: product.id,
      quantity: 1
    })
    ElMessage.success('已添加到购物车')
  } catch (error) {
    ElMessage.error('添加失败')
  } finally {
    loading.value = false
  }
}

// 取消收藏
const handleRemove = async (item) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await store.dispatch('favorite/removeFavorite', item.id)
    ElMessage.success('已取消收藏')
    fetchFavorites()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消收藏失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取收藏列表
const fetchFavorites = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      ...searchForm.value
    }
    
    await store.dispatch('favorite/fetchFavorites', params)
    total.value = store.state.favorite.total
  } catch (error) {
    ElMessage.error('获取收藏列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
.tourist-favorites {
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

.product-card {
  margin-bottom: 20px;
  height: 100%;
}

.product-image {
  width: 100%;
  height: 200px;
  cursor: pointer;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  color: #909399;
  font-size: 30px;
}

.product-info {
  padding: 10px 0;
}

.product-name {
  margin: 0 0 10px;
  font-size: 16px;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-name:hover {
  color: #409eff;
}

.product-price {
  margin: 0 0 10px;
  font-size: 18px;
  color: #f56c6c;
  font-weight: bold;
}

.product-farmer {
  margin: 0 0 10px;
  font-size: 14px;
  color: #909399;
}

.product-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 