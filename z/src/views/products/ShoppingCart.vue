<template>
  <div class="shopping-cart">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>购物车</h3>
          <el-button 
            type="danger" 
            :disabled="!selectedItems.length"
            @click="handleClearSelected"
          >
            清空选中
          </el-button>
        </div>
      </template>

      <div v-if="cartItems.length" class="cart-content">
        <el-table
          ref="tableRef"
          :data="cartItems"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          
          <el-table-column label="商品信息" min-width="300">
            <template #default="{ row }">
              <div class="product-info">
                <el-image
                  :src="row.product.image || '/default-product.jpg'"
                  class="product-image"
                  fit="cover"
                />
                <div class="product-details">
                  <div class="product-name">{{ row.product.name }}</div>
                  <el-tag size="small">{{ getCategoryLabel(row.product.category) }}</el-tag>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="单价" width="120">
            <template #default="{ row }">
              <span class="price">¥{{ row.product.price.toFixed(2) }}</span>
            </template>
          </el-table-column>

          <el-table-column label="数量" width="200">
            <template #default="{ row }">
              <el-input-number
                v-model="row.quantity"
                :min="1"
                :max="row.product.stock"
                size="small"
                @change="(value) => handleQuantityChange(row, value)"
              />
            </template>
          </el-table-column>

          <el-table-column label="小计" width="120">
            <template #default="{ row }">
              <span class="subtotal">¥{{ (row.product.price * row.quantity).toFixed(2) }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button
                type="danger"
                size="small"
                @click="handleRemove(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="cart-footer">
          <div class="select-all">
            <el-checkbox
              v-model="isAllSelected"
              @change="handleSelectAll"
            >
              全选
            </el-checkbox>
            <span class="selected-count" v-if="selectedItems.length">
              已选择 {{ selectedItems.length }} 件商品
            </span>
          </div>

          <div class="checkout-info">
            <div class="total-price">
              合计：<span class="price">¥{{ totalPrice.toFixed(2) }}</span>
            </div>
            <el-button
              type="primary"
              size="large"
              :disabled="!selectedItems.length"
              @click="handleCheckout"
            >
              结算 ({{ selectedItems.length }})
            </el-button>
          </div>
        </div>
      </div>

      <div v-else class="empty-cart">
        <el-empty description="购物车是空的">
          <el-button type="primary" @click="$router.push('/products')">
            去购物
          </el-button>
        </el-empty>
      </div>
    </el-card>

    <!-- 结算确认对话框 -->
    <el-dialog
      v-model="checkoutDialogVisible"
      title="确认订单"
      width="50%"
    >
      <div class="checkout-dialog">
        <div class="address-section">
          <h4>收货地址</h4>
          <div v-if="selectedAddress" class="selected-address">
            <div class="address-info">
              <p>
                <span class="receiver">{{ selectedAddress.receiver }}</span>
                <span class="phone">{{ selectedAddress.phone }}</span>
              </p>
              <p class="address">{{ selectedAddress.address }}</p>
            </div>
            <el-button link type="primary" @click="showAddressDialog = true">
              更换地址
            </el-button>
          </div>
          <el-button v-else type="primary" @click="showAddressDialog = true">
            添加收货地址
          </el-button>
        </div>

        <div class="order-items">
          <h4>商品清单</h4>
          <div class="item" v-for="item in selectedItems" :key="item.id">
            <div class="item-info">
              <el-image
                :src="item.product.image || '/default-product.jpg'"
                class="item-image"
                fit="cover"
              />
              <div class="item-details">
                <div class="item-name">{{ item.product.name }}</div>
                <div class="item-price">
                  ¥{{ item.product.price.toFixed(2) }} × {{ item.quantity }}
                </div>
              </div>
            </div>
            <div class="item-subtotal">
              ¥{{ (item.product.price * item.quantity).toFixed(2) }}
            </div>
          </div>
        </div>

        <div class="order-total">
          <span>实付金额：</span>
          <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="checkoutDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :disabled="!selectedAddress"
            @click="handleConfirmOrder"
          >
            提交订单
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 地址选择对话框 -->
    <el-dialog
      v-model="showAddressDialog"
      title="选择收货地址"
      width="40%"
    >
      <address-list
        v-if="showAddressDialog"
        :selected-id="selectedAddress?.id"
        @select="handleSelectAddress"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import AddressList from '@/components/address/AddressList.vue'

const store = useStore()
const router = useRouter()

// 数据
const cartItems = computed(() => store.state.cart.items)
const tableRef = ref(null)
const selectedItems = ref([])
const checkoutDialogVisible = ref(false)
const showAddressDialog = ref(false)
const selectedAddress = ref(null)

// 计算属性
const isAllSelected = computed(() => {
  return cartItems.value.length > 0 && selectedItems.value.length === cartItems.value.length
})

const totalPrice = computed(() => {
  return selectedItems.value.reduce((total, item) => {
    return total + item.product.price * item.quantity
  }, 0)
})

// 商品分类
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

// 事件处理
const handleSelectionChange = (items) => {
  selectedItems.value = items
}

const handleSelectAll = (val) => {
  if (val) {
    tableRef.value?.toggleAllSelection()
  } else {
    tableRef.value?.clearSelection()
  }
}

const handleQuantityChange = async (item, value) => {
  try {
    await store.dispatch('cart/updateQuantity', {
      id: item.id,
      quantity: value
    })
  } catch (error) {
    console.error('Update quantity error:', error)
    ElMessage.error('更新数量失败')
  }
}

const handleRemove = async (item) => {
  try {
    await ElMessageBox.confirm('确定要从购物车中删除该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await store.dispatch('cart/removeFromCart', item.id)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Remove from cart error:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleClearSelected = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedItems.value.length} 件商品吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const itemIds = selectedItems.value.map(item => item.id)
    await store.dispatch('cart/removeMultiple', itemIds)
    ElMessage.success('清空成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Clear selected error:', error)
      ElMessage.error('清空失败')
    }
  }
}

const handleCheckout = () => {
  if (!selectedItems.value.length) {
    ElMessage.warning('请选择要结算的商品')
    return
  }
  checkoutDialogVisible.value = true
}

const handleSelectAddress = (address) => {
  selectedAddress.value = address
  showAddressDialog.value = false
}

const handleConfirmOrder = async () => {
  if (!selectedAddress.value) {
    ElMessage.warning('请选择收货地址')
    return
  }

  try {
    const orderData = {
      address_id: selectedAddress.value.id,
      items: selectedItems.value.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity
      }))
    }

    const response = await store.dispatch('order/createOrder', orderData)
    
    // 从购物车中移除已下单的商品
    await store.dispatch('cart/removeMultiple', selectedItems.value.map(item => item.id))
    
    checkoutDialogVisible.value = false
    ElMessage.success('下单成功')
    
    // 跳转到订单详情页
    router.push(`/orders/${response.data.id}`)
  } catch (error) {
    console.error('Create order error:', error)
    ElMessage.error('下单失败')
  }
}
</script>

<style scoped>
.shopping-cart {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-content {
  margin-bottom: 20px;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-name {
  font-size: 14px;
  margin-bottom: 4px;
}

.price, .subtotal {
  color: #ff6b6b;
  font-weight: bold;
}

.cart-footer {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.select-all {
  display: flex;
  align-items: center;
  gap: 16px;
}

.selected-count {
  color: #666;
}

.checkout-info {
  display: flex;
  align-items: center;
  gap: 24px;
}

.total-price {
  font-size: 20px;
  color: #ff6b6b;
  font-weight: bold;
}

.empty-cart {
  padding: 40px 0;
}

/* 结算对话框样式 */
.checkout-dialog {
  padding: 20px 0;
}

.address-section {
  margin-bottom: 30px;
}

.selected-address {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
  margin-top: 16px;
}

.address-info {
  flex: 1;
}

.receiver {
  font-weight: bold;
  margin-right: 16px;
}

.phone {
  color: #666;
}

.address {
  margin: 8px 0 0;
  color: #666;
}

.order-items {
  margin-bottom: 30px;
}

.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.item:last-child {
  border-bottom: none;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.item-image {
  width: 60px;
  height: 60px;
  border-radius: 4px;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-name {
  font-size: 14px;
}

.item-price {
  color: #666;
  font-size: 14px;
}

.item-subtotal {
  color: #ff6b6b;
  font-weight: bold;
}

.order-total {
  text-align: right;
  padding: 20px 0;
  font-size: 16px;
}

.order-total .total-price {
  font-size: 24px;
  margin-left: 8px;
}

@media (max-width: 768px) {
  .product-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .cart-footer {
    flex-direction: column;
    gap: 16px;
  }

  .checkout-info {
    width: 100%;
    justify-content: space-between;
  }
}
</style> 