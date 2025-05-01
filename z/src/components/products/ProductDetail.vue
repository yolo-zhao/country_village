<template>
  <div class="product-detail">
    <div class="product-gallery">
      <el-image
        :src="product.image || '/default-product.jpg'"
        class="main-image"
        fit="cover"
      />
    </div>

    <div class="product-info">
      <h2 class="product-name">{{ product.name }}</h2>
      
      <div class="product-meta">
        <el-tag>{{ getCategoryLabel(product.category) }}</el-tag>
        <span class="product-sales">销量: {{ product.sales_count }}</span>
      </div>

      <div class="product-price">
        <span class="price-label">价格：</span>
        <span class="price-value">¥{{ product.price.toFixed(2) }}</span>
      </div>

      <div class="product-stock">
        <span class="stock-label">库存：</span>
        <span class="stock-value">{{ product.stock }}</span>
      </div>

      <div class="product-actions">
        <el-input-number
          v-model="quantity"
          :min="1"
          :max="product.stock"
          size="large"
          class="quantity-input"
        />
        <el-button
          type="primary"
          size="large"
          :disabled="product.stock <= 0"
          @click="handleAddToCart"
        >
          加入购物车
        </el-button>
      </div>

      <div class="product-description">
        <h3>产品描述</h3>
        <p>{{ product.description }}</p>
      </div>

      <div class="farmer-info" v-if="product.farmer">
        <h3>农户信息</h3>
        <div class="farmer-card">
          <el-avatar
            :src="product.farmer.avatar || '/default-avatar.jpg'"
            :size="50"
          />
          <div class="farmer-details">
            <div class="farmer-name">{{ product.farmer.name }}</div>
            <div class="farmer-contact">联系电话：{{ product.farmer.phone }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['add-to-cart'])

const quantity = ref(1)

const categories = [
  { label: '水果', value: 'fruits' },
  { label: '蔬菜', value: 'vegetables' },
  { label: '粮食', value: 'grains' },
  { label: '特产', value: 'specialties' },
  { label: '其他', value: 'others' }
]

const getCategoryLabel = (value) => {
  const category = categories.find(c => c.value === value)
  return category ? category.label : value
}

const handleAddToCart = () => {
  if (props.product.stock <= 0) {
    ElMessage.warning('该产品已售罄')
    return
  }
  
  if (quantity.value > props.product.stock) {
    ElMessage.warning('购买数量不能超过库存数量')
    return
  }

  emit('add-to-cart', {
    product_id: props.product.id,
    quantity: quantity.value
  })
}
</script>

<style scoped>
.product-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  padding: 20px;
}

.product-gallery {
  position: relative;
}

.main-image {
  width: 100%;
  height: 400px;
  border-radius: 8px;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-name {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.product-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.product-sales {
  color: #666;
}

.product-price {
  margin: 20px 0;
}

.price-label {
  font-size: 16px;
  color: #666;
}

.price-value {
  font-size: 28px;
  color: #ff6b6b;
  font-weight: bold;
  margin-left: 8px;
}

.product-stock {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stock-label {
  color: #666;
}

.product-actions {
  display: flex;
  gap: 16px;
  margin: 20px 0;
}

.quantity-input {
  width: 150px;
}

.product-description {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.product-description h3 {
  margin: 0 0 16px;
  font-size: 18px;
}

.product-description p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.farmer-info {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.farmer-info h3 {
  margin: 0 0 16px;
  font-size: 18px;
}

.farmer-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.farmer-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.farmer-name {
  font-weight: bold;
}

.farmer-contact {
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .product-detail {
    grid-template-columns: 1fr;
  }

  .main-image {
    height: 300px;
  }
}
</style> 