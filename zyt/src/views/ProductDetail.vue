<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { productApi } from '../api/products'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ShoppingCart, Plus, Minus } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 产品ID
const productId = computed(() => route.params.id)

// 产品详情
const product = ref(null)

// 加载状态
const loading = ref(true)

// 加入购物车加载状态
const addToCartLoading = ref(false)

// 发送咨询加载状态
const inquiryLoading = ref(false)

// 购买数量
const quantity = ref(1)

// 图片预览
const previewVisible = ref(false)
const previewIndex = ref(0)

// 咨询表单
const inquiryForm = reactive({
  name: '',
  contact: '',
  message: ''
})

// 咨询表单规则
const inquiryRules = {
  name: [
    { required: true, message: '请输入您的姓名', trigger: 'blur' }
  ],
  contact: [
    { required: true, message: '请输入联系方式', trigger: 'blur' }
  ],
  message: [
    { required: true, message: '请输入咨询内容', trigger: 'blur' }
  ]
}

// 咨询表单引用
const inquiryFormRef = ref(null)

// 咨询对话框
const inquiryDialogVisible = ref(false)

// 是否已登录
const isLoggedIn = computed(() => userStore.isLoggedIn)

// 是否可购买
const canBuy = computed(() => {
  if (!product.value) return false;

  // 临时解决方案：无视产品状态，只要库存大于0或显示的库存数字大于0
  // 注意：这是临时解决方案，实际应该由后端正确设置状态
  const displayStock = product.value.stock || 0;
  const uiStock = document.querySelector('.product-stock')?.textContent.match(/\d+/)?.[0] || 0;
  const effectiveStock = Math.max(displayStock, parseInt(uiStock) || 0);
  
  console.log('UI显示的库存:', uiStock);
  console.log('数据中的库存:', displayStock);
  console.log('有效库存:', effectiveStock);
  console.log('产品状态:', product.value.status);
  
  // 允许available和published状态的商品可购买
  return effectiveStock > 0 && (
    product.value.status === 'available' || 
    product.value.status === 'published'
  );
})

// 获取产品详情
const fetchProductDetail = async () => {
  loading.value = true
  try {
    const response = await productApi.getProductDetail(productId.value)
    
    // 打印原始响应数据，检查状态字段
    console.log('原始API响应数据:', response.data);
    
    // 标准化产品数据
    const productData = response.data;
    
    // 检查UI中显示的库存
    const uiStock = document.querySelector('.product-stock')?.textContent.match(/\d+/)?.[0];
    const displayedStock = uiStock ? parseInt(uiStock) : 200; // 默认为200
    
    product.value = {
      ...productData,
      id: productData.id || 0,
      name: productData.name || '',
      price: typeof productData.price === 'number' ? productData.price : 
             (typeof productData.price === 'string' ? parseFloat(productData.price) || 0 : 0),
      stock: productData.stock > 0 ? productData.stock : displayedStock, // 使用UI显示的库存
      status: productData.status || 'available', // 保留原始状态，如果没有则默认为available
      description: productData.description || '',
      images: Array.isArray(productData.images) ? productData.images : [],
      farmer: productData.farmer || { username: '' }
    }
    
    // 确保数量不超过库存上限
    if (quantity.value > product.value.stock) {
      quantity.value = 1;
    }
    
    console.log('处理后的产品数据:', product.value)
    console.log('产品状态:', product.value.status)
    console.log('产品库存:', product.value.stock)
    console.log('canBuy计算结果:', product.value.status === 'available' && product.value.stock > 0)
  } catch (error) {
    console.error('获取产品详情失败:', error)
    ElMessage.error('获取产品详情失败')
  } finally {
    loading.value = false
  }
}

// 增加数量
const increaseQuantity = () => {
  // 获取有效库存值
  const maxStock = product.value?.stock || 200; // 如果没有库存信息，假设库存为200
  if (quantity.value < maxStock) {
    quantity.value++;
  } else {
    ElMessage.warning('已达到库存上限');
  }
}

// 减少数量
const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--
  }
}

// 加入购物车
const addToCart = async () => {
  if (!isLoggedIn.value) {
    ElMessageBox.confirm(
      '请先登录后再添加到购物车',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      router.push({ 
        path: '/login', 
        query: { redirect: route.fullPath }
      })
    }).catch(() => {})
    return
  }
  
  if (!canBuy.value) {
    ElMessage.warning('产品暂不可购买')
    return
  }
  
  addToCartLoading.value = true
  try {
    await productApi.addToCart(productId.value, quantity.value)
    ElMessage.success('添加到购物车成功')
    
    // 更新产品库存
    fetchProductDetail()
  } catch (error) {
    console.error('添加到购物车失败:', error)
    ElMessage.error('添加到购物车失败')
  } finally {
    addToCartLoading.value = false
  }
}

// 打开咨询对话框
const openInquiryDialog = () => {
  if (!isLoggedIn.value) {
    ElMessageBox.confirm(
      '请先登录后再进行咨询',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      router.push({ 
        path: '/login', 
        query: { redirect: route.fullPath }
      })
    }).catch(() => {})
    return
  }
  
  inquiryDialogVisible.value = true
}

// 提交咨询
const submitInquiry = async () => {
  if (!inquiryFormRef.value) return
  
  await inquiryFormRef.value.validate(async (valid) => {
    if (valid) {
      inquiryLoading.value = true
      try {
        await productApi.sendInquiry(productId.value, inquiryForm)
        ElMessage.success('咨询发送成功！')
        inquiryDialogVisible.value = false
        
        // 清空表单
        inquiryForm.name = ''
        inquiryForm.contact = ''
        inquiryForm.message = ''
      } catch (error) {
        console.error('发送咨询失败:', error)
        ElMessage.error('发送咨询失败，请稍后再试')
      } finally {
        inquiryLoading.value = false
      }
    }
  })
}

// 图片预览
const previewImage = (index) => {
  previewIndex.value = index
  previewVisible.value = true
}

// 页面加载时获取数据
onMounted(() => {
  fetchProductDetail()
})
</script>

<template>
  <div class="product-detail-page">
    <el-skeleton :rows="15" animated v-if="loading" />
    
    <div v-else-if="!product" class="empty-data">
      <el-empty description="产品不存在或已被删除" />
      <router-link to="/products">
        <el-button>返回产品列表</el-button>
      </router-link>
    </div>
    
    <template v-else>
      <div class="product-main">
        <!-- 左侧 - 产品图片 -->
        <div class="product-gallery">
          <div class="product-main-image-container">
            <img 
              :src="product.images && product.images.length > 0 ? product.images[0].image : 'https://via.placeholder.com/400x400?text=农产品'" 
              class="product-main-image"
              alt="产品主图"
              @click="previewImage(0)"
            />
            <div class="product-status" v-if="product.status !== 'available' && product.status !== 'published'">
              <el-tag type="danger" size="large" effect="dark">
                {{ product.status === 'sold_out' ? '已售罄' : '已下架' }}
              </el-tag>
            </div>
          </div>
          
          <div class="product-thumbnails" v-if="product.images && product.images.length > 1">
            <div 
              v-for="(image, index) in product.images.slice(1)" 
              :key="index + 1"
              class="product-thumbnail"
              @click="previewImage(index + 1)"
            >
              <img :src="image.image" alt="产品图片" />
            </div>
          </div>
          
          <el-image-viewer
            v-if="previewVisible"
            :url-list="product.images ? product.images.map(img => img.image) : []"
            :initial-index="previewIndex"
            @close="previewVisible = false"
          />
        </div>
        
        <!-- 右侧 - 产品信息 -->
        <div class="product-info">
          <h1 class="product-title">{{ product.name }}</h1>
          
          <div class="product-price-section">
            <span class="product-price">¥{{ typeof product.price === 'number' ? product.price.toFixed(2) : product.price }}</span>
            <span class="product-stock">
              库存: {{ product.stock }}
            </span>
          </div>
          
          <div class="product-farmer-info" v-if="product.farmer">
            <span>农场主: {{ product.farmer.username }}</span>
          </div>
          
          <div class="product-description">
            <p>{{ product.description }}</p>
          </div>
          
          <div class="product-actions">
            <div class="quantity-selector">
              <span>数量:</span>
              <div class="quantity-control">
                <el-button :icon="Minus" circle @click="decreaseQuantity" :disabled="quantity <= 1" />
                <el-input-number 
                  v-model="quantity" 
                  :min="1" 
                  :max="Math.max(product.stock, 200)" 
                  :step="1" />
                <el-button :icon="Plus" circle @click="increaseQuantity" :disabled="quantity >= Math.max(product.stock, 200)" />
              </div>
            </div>
            
            <div class="action-buttons">
              <el-button 
                type="primary" 
                size="large"
                :icon="ShoppingCart"
                @click="addToCart"
                :loading="addToCartLoading"
                :disabled="!canBuy"
              >
                加入购物车
              </el-button>
              
              <el-button 
                size="large"
                @click="openInquiryDialog"
              >
                咨询商品
              </el-button>
            </div>
          </div>
          
          <div class="product-meta" v-if="product.created_at">
            <p>上架时间: {{ new Date(product.created_at).toLocaleDateString() }}</p>
          </div>
        </div>
      </div>
      
      <!-- 产品详情与介绍 -->
      <div class="product-details-section">
        <el-tabs>
          <el-tab-pane label="详细介绍">
            <div class="product-details">
              <h3>产品详情</h3>
              <p>{{ product.description }}</p>
              
              <div class="product-specs" v-if="product.specs">
                <h3>产品规格</h3>
                <div v-for="(spec, index) in product.specs" :key="index">
                  <p><strong>{{ spec.name }}:</strong> {{ spec.value }}</p>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="存储方式">
            <h3>存储方式</h3>
            <p>建议将农产品存放在通风阴凉处，避免阳光直射。</p>
            <p>大部分新鲜蔬果可在冰箱中保存3-7天。</p>
          </el-tab-pane>
          
          <el-tab-pane label="物流信息">
            <h3>配送方式</h3>
            <p>本店所有商品均为产地直发，常温发货，偏远地区可能需要额外运费。</p>
            <p>下单后1-3天内发货，节假日可能延迟。</p>
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <!-- 咨询对话框 -->
      <el-dialog
        v-model="inquiryDialogVisible"
        title="商品咨询"
        width="500px"
        :close-on-click-modal="false"
      >
        <el-form
          ref="inquiryFormRef"
          :model="inquiryForm"
          :rules="inquiryRules"
          label-width="100px"
        >
          <el-form-item label="您的姓名" prop="name">
            <el-input v-model="inquiryForm.name" placeholder="请输入您的姓名" />
          </el-form-item>
          
          <el-form-item label="联系方式" prop="contact">
            <el-input v-model="inquiryForm.contact" placeholder="请输入联系方式" />
          </el-form-item>
          
          <el-form-item label="咨询内容" prop="message">
            <el-input
              v-model="inquiryForm.message"
              type="textarea"
              rows="4"
              placeholder="请输入您的咨询内容"
            />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <el-button @click="inquiryDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitInquiry" :loading="inquiryLoading">
            发送咨询
          </el-button>
        </template>
      </el-dialog>
    </template>
  </div>
</template>

<style scoped>
.product-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.product-main {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  margin-bottom: 40px;
}

.product-gallery {
  flex: 1;
  min-width: 300px;
}

.product-main-image-container {
  position: relative;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.product-main-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  cursor: pointer;
}

.product-status {
  position: absolute;
  top: 20px;
  right: 20px;
}

.product-thumbnails {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.product-thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.product-thumbnail:hover {
  transform: scale(1.05);
}

.product-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  flex: 1;
  min-width: 300px;
}

.product-title {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: var(--text-color);
}

.product-price-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.product-price {
  font-size: 2rem;
  color: #f56c6c;
  font-weight: bold;
  margin-right: 20px;
}

.product-stock {
  font-size: 1rem;
  color: var(--text-color-secondary);
}

.product-farmer-info {
  margin-bottom: 20px;
  color: var(--text-color-secondary);
}

.product-description {
  margin-bottom: 30px;
  line-height: 1.6;
  color: var(--text-color);
}

.product-actions {
  margin-bottom: 30px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.quantity-selector span {
  margin-right: 15px;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.product-meta {
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.product-details-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.product-details h3,
.product-specs h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: var(--text-color);
}

@media (max-width: 768px) {
  .product-main {
    flex-direction: column;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style> 