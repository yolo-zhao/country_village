<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { productApi } from '../../api/products'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 购物车数据
const cart = ref(null)

// 加载状态
const loading = ref(true)

// 更新数量加载状态
const updateLoading = ref({})

// 选中的商品ID
const selectedItems = ref([])

// 是否全选
const isAllSelected = computed(() => {
  if (!cart.value || !cart.value.items || cart.value.items.length === 0) return false
  return cart.value.items.every(item => selectedItems.value.includes(item.id))
})

// 总价
const totalPrice = computed(() => {
  if (!cart.value || !cart.value.items) return 0;
  return cart.value.items
    .filter(item => selectedItems.value.includes(item.id))
    .reduce((sum, item) => {
      const itemPrice = typeof item.product.price === 'number' ? item.product.price : parseFloat(item.product.price) || 0;
      const itemTotal = item.total_price ? 
                        (typeof item.total_price === 'number' ? item.total_price : parseFloat(item.total_price) || 0) : 
                        (item.quantity * itemPrice);
      return sum + itemTotal;
    }, 0);
})

// 获取购物车
const fetchCart = async () => {
  loading.value = true
  try {
    const response = await productApi.getCart()
    
    // 处理后端返回的数据格式
    // 后端可能返回数组(包含用户的所有购物车)或单个购物车对象
    if (Array.isArray(response.data) && response.data.length > 0) {
      // 使用第一个购物车
      cart.value = response.data[0]
    } else if (response.data && !Array.isArray(response.data)) {
      // 单个购物车对象
      cart.value = response.data
    } else {
      // 没有购物车，创建空对象
      cart.value = { items: [] }
    }
    
    // 处理价格数据，确保是数字类型
    if (cart.value && cart.value.items) {
      cart.value.items.forEach(item => {
        // 确保产品价格是数字类型
        if (item.product && typeof item.product.price !== 'number') {
          item.product.price = typeof item.product.price === 'string' ? 
                                parseFloat(item.product.price) || 0 : 0;
        }
        
        // 确保产品总价是数字类型
        if (item.total_price && typeof item.total_price !== 'number') {
          item.total_price = typeof item.total_price === 'string' ? 
                              parseFloat(item.total_price) || 0 : 0;
        }
      });
    }
    
    console.log('购物车数据:', cart.value)
    
    // 默认选中所有可购买的商品
    selectedItems.value = (cart.value.items || [])
      .filter(item => 
        (item.product.status === 'available' || item.product.status === 'published') && 
        item.product.stock > 0
      )
      .map(item => item.id)
  } catch (error) {
    console.error('获取购物车失败:', error)
    ElMessage.error('获取购物车失败')
  } finally {
    loading.value = false
  }
}

// 更新商品数量
const updateQuantity = async (item, newQuantity) => {
  if (newQuantity < 1) {
    ElMessage.warning('购买数量不能小于1')
    return
  }
  
  if (newQuantity > item.product.stock) {
    ElMessage.warning('购买数量不能超过库存')
    return
  }
  
  updateLoading.value[item.id] = true
  try {
    await productApi.updateCartItem(item.id, newQuantity)
    // 刷新购物车
    fetchCart()
  } catch (error) {
    console.error('更新数量失败:', error)
    ElMessage.error('更新数量失败')
  } finally {
    updateLoading.value[item.id] = false
  }
}

// 移除商品
const removeItem = async (itemId) => {
  try {
    await productApi.removeFromCart(itemId)
    // 从选中列表中移除
    selectedItems.value = selectedItems.value.filter(id => id !== itemId)
    // 刷新购物车
    fetchCart()
    ElMessage.success('商品已从购物车移除')
  } catch (error) {
    console.error('移除商品失败:', error)
    ElMessage.error('移除商品失败')
  }
}

// 清空购物车
const clearCart = async () => {
  ElMessageBox.confirm(
    '确定要清空购物车吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await productApi.clearCart()
      selectedItems.value = []
      fetchCart()
      ElMessage.success('购物车已清空')
    } catch (error) {
      console.error('清空购物车失败:', error)
      ElMessage.error('清空购物车失败')
    }
  }).catch(() => {})
}

// 全选/取消全选
const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selectedItems.value = []
  } else {
    selectedItems.value = cart.value.items.map(item => item.id)
  }
}

// 跳转到产品详情
const goToProductDetail = (productId) => {
  router.push(`/products/${productId}`)
}

// 页面加载时获取数据
onMounted(() => {
  fetchCart()
})

// 格式化价格显示
const formatPrice = (price) => {
  const numPrice = typeof price === 'number' ? price : parseFloat(price) || 0;
  return numPrice.toFixed(2);
}
</script>

<template>
  <div class="cart-page">
    <h1 class="page-title">我的购物车</h1>
    
    <el-skeleton :rows="5" animated v-if="loading" />
    
    <div v-else-if="!cart || !cart.items || cart.items.length === 0" class="empty-cart">
      <el-empty description="购物车空空如也" :image-size="200">
        <template #description>
          <p>您的购物车还没有商品，快去选购吧！</p>
        </template>
        <router-link to="/products">
          <el-button type="primary">去购物</el-button>
        </router-link>
      </el-empty>
    </div>
    
    <template v-else>
      <div class="cart-header">
        <div class="cart-actions">
          <el-checkbox
            v-model="isAllSelected"
            @change="toggleSelectAll"
            label="全选"
          />
          <el-button link @click="clearCart">清空购物车</el-button>
        </div>
      </div>
      
      <div class="cart-list">
        <el-card v-for="item in cart.items" :key="item.id" class="cart-item">
          <div class="cart-item-content">
            <el-checkbox
              v-model="selectedItems"
              :label="item.id"
              :disabled="item.product.status !== 'available' && item.product.status !== 'published' || item.product.stock <= 0"
            />
            
            <div class="product-image" @click="goToProductDetail(item.product.id)">
              <img 
                :src="item.product.images && item.product.images.length > 0 ? item.product.images[0].image : 'https://via.placeholder.com/100x100?text=产品'"
                alt="产品图片"
              />
            </div>
            
            <div class="product-info" @click="goToProductDetail(item.product.id)">
              <h3 class="product-title">{{ item.product.name }}</h3>
              <div class="product-meta">
                <span class="product-price">¥{{ formatPrice(item.product.price) }}</span>
                <span 
                  class="product-stock" 
                  :class="{'stock-warning': item.product.stock < 10}"
                >
                  库存: {{ item.product.stock }}
                </span>
                <span 
                  v-if="item.product.status !== 'available' && item.product.status !== 'published'" 
                  class="product-status"
                >
                  {{ item.product.status === 'sold_out' ? '已售罄' : '已下架' }}
                </span>
              </div>
            </div>
            
            <div class="quantity-control">
              <el-button 
                circle 
                size="small" 
                @click="updateQuantity(item, item.quantity - 1)"
                :disabled="item.quantity <= 1 || updateLoading[item.id]"
              >
                -
              </el-button>
              <el-input-number 
                v-model="item.quantity" 
                :min="1" 
                :max="item.product.stock"
                size="small"
                :disabled="updateLoading[item.id]"
                @change="newValue => updateQuantity(item, newValue)"
              />
              <el-button 
                circle 
                size="small" 
                @click="updateQuantity(item, item.quantity + 1)"
                :disabled="item.quantity >= item.product.stock || updateLoading[item.id]"
              >
                +
              </el-button>
            </div>
            
            <div class="item-total">
              <span class="total-price">¥{{ formatPrice(item.total_price || (item.quantity * item.product.price)) }}</span>
            </div>
            
            <div class="item-actions">
              <el-button 
                type="danger" 
                size="small" 
                @click="removeItem(item.id)"
                :icon="Delete"
                circle
                title="删除"
              />
            </div>
          </div>
        </el-card>
      </div>
      
      <div class="cart-footer">
        <div class="cart-summary">
          <div class="summary-row">
            <span>已选商品:</span>
            <span>{{ selectedItems.length }} 件</span>
          </div>
          <div class="summary-row">
            <span>合计:</span>
            <span class="total-amount">¥{{ formatPrice(totalPrice) }}</span>
          </div>
        </div>
        
        <div class="checkout-actions">
          <el-button 
            type="primary" 
            size="large"
            :disabled="selectedItems.length === 0"
          >
            去结算
          </el-button>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.cart-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-align: center;
}

.empty-cart {
  margin: 50px 0;
  text-align: center;
}

.cart-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.cart-list {
  margin-bottom: 20px;
}

.cart-item {
  margin-bottom: 15px;
}

.cart-item-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.product-image {
  width: 80px;
  height: 80px;
  overflow: hidden;
  border-radius: 4px;
  cursor: pointer;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  flex: 1;
  cursor: pointer;
}

.product-title {
  font-size: 1.1rem;
  margin-bottom: 8px;
}

.product-meta {
  display: flex;
  gap: 15px;
  font-size: 0.9rem;
}

.product-price {
  color: #f56c6c;
  font-weight: bold;
}

.stock-warning {
  color: #E6A23C;
}

.product-status {
  color: #F56C6C;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.item-total {
  min-width: 100px;
  text-align: right;
}

.total-price {
  font-size: 1.2rem;
  color: #f56c6c;
  font-weight: bold;
}

.cart-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.cart-summary {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.summary-row {
  display: flex;
  gap: 10px;
}

.total-amount {
  font-size: 1.5rem;
  color: #f56c6c;
  font-weight: bold;
}

@media (max-width: 768px) {
  .cart-item-content {
    flex-wrap: wrap;
  }
  
  .product-info {
    width: 100%;
    margin: 10px 0;
  }
  
  .cart-footer {
    flex-direction: column;
    gap: 15px;
  }
  
  .cart-summary {
    width: 100%;
  }
  
  .checkout-actions {
    width: 100%;
  }
  
  .checkout-actions button {
    width: 100%;
  }
}
</style> 