<template>
  <div class="order-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>订单详情</h3>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <template v-if="order">
        <!-- 订单状态 -->
        <div class="status-section">
          <el-steps :active="getStatusStep(order.status)" finish-status="success">
            <el-step title="提交订单" />
            <el-step title="付款成功" />
            <el-step title="商家发货" />
            <el-step title="交易完成" />
          </el-steps>
        </div>

        <!-- 收货信息 -->
        <div class="section">
          <h4>收货信息</h4>
          <div class="address-info">
            <p>
              <span class="label">收货人：</span>
              {{ order.address.receiver }}
            </p>
            <p>
              <span class="label">联系电话：</span>
              {{ order.address.phone }}
            </p>
            <p>
              <span class="label">收货地址：</span>
              {{ order.address.address }}
            </p>
          </div>
        </div>

        <!-- 商品信息 -->
        <div class="section">
          <h4>商品信息</h4>
          <div class="products-list">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="product-item"
            >
              <el-image
                :src="item.product.image || '/default-product.jpg'"
                class="product-image"
                fit="cover"
              />
              <div class="product-info">
                <div class="product-name">{{ item.product.name }}</div>
                <div class="product-meta">
                  <span class="price">¥{{ item.price.toFixed(2) }}</span>
                  <span class="quantity">× {{ item.quantity }}</span>
                </div>
              </div>
              <div class="product-subtotal">
                ¥{{ (item.price * item.quantity).toFixed(2) }}
              </div>
            </div>
          </div>
        </div>

        <!-- 订单信息 -->
        <div class="section">
          <h4>订单信息</h4>
          <div class="order-info">
            <p>
              <span class="label">订单编号：</span>
              {{ order.order_number }}
            </p>
            <p>
              <span class="label">创建时间：</span>
              {{ formatDate(order.created_at) }}
            </p>
            <p v-if="order.paid_at">
              <span class="label">支付时间：</span>
              {{ formatDate(order.paid_at) }}
            </p>
            <p v-if="order.shipped_at">
              <span class="label">发货时间：</span>
              {{ formatDate(order.shipped_at) }}
            </p>
            <p v-if="order.completed_at">
              <span class="label">完成时间：</span>
              {{ formatDate(order.completed_at) }}
            </p>
            <p v-if="order.cancelled_at">
              <span class="label">取消时间：</span>
              {{ formatDate(order.cancelled_at) }}
            </p>
          </div>
        </div>

        <!-- 物流信息 -->
        <div v-if="order.tracking_number" class="section">
          <h4>物流信息</h4>
          <div class="shipping-info">
            <p>
              <span class="label">物流公司：</span>
              {{ order.carrier }}
            </p>
            <p>
              <span class="label">物流单号：</span>
              {{ order.tracking_number }}
            </p>
          </div>
        </div>

        <!-- 订单金额 -->
        <div class="amount-section">
          <div class="amount-item">
            <span>商品总额：</span>
            <span>¥{{ order.total_amount.toFixed(2) }}</span>
          </div>
          <div class="amount-item">
            <span>运费：</span>
            <span>¥{{ order.shipping_fee.toFixed(2) }}</span>
          </div>
          <div class="amount-item total">
            <span>实付金额：</span>
            <span class="price">¥{{ (order.total_amount + order.shipping_fee).toFixed(2) }}</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="actions-section">
          <el-button
            v-if="order.status === 'pending'"
            type="primary"
            @click="handlePay"
          >
            去支付
          </el-button>
          <el-button
            v-if="order.status === 'pending'"
            type="danger"
            @click="handleCancel"
          >
            取消订单
          </el-button>
          <el-button
            v-if="order.status === 'shipped'"
            type="success"
            @click="handleConfirm"
          >
            确认收货
          </el-button>
        </div>
      </template>
    </el-card>

    <!-- 支付对话框 -->
    <el-dialog
      v-model="payDialogVisible"
      title="订单支付"
      width="400px"
      destroy-on-close
    >
      <div class="pay-dialog">
        <div class="pay-amount">
          支付金额：<span class="price">¥{{ (order?.total_amount + order?.shipping_fee).toFixed(2) }}</span>
        </div>
        <div class="pay-method">
          <h4>选择支付方式</h4>
          <el-radio-group v-model="paymentMethod">
            <el-radio label="alipay">支付宝</el-radio>
            <el-radio label="wechat">微信支付</el-radio>
          </el-radio-group>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="payDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirmPay">
            确认支付
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useStore()
const route = useRoute()
const router = useRouter()

// 数据
const payDialogVisible = ref(false)
const paymentMethod = ref('alipay')

// 从 store 获取数据
const loading = computed(() => store.state.order.loading)
const order = computed(() => store.state.order.currentOrder)

// 获取订单状态对应的步骤
const getStatusStep = (status) => {
  const steps = {
    pending: 0,
    paid: 1,
    shipped: 2,
    completed: 3,
    cancelled: 0
  }
  return steps[status] || 0
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 事件处理
const handlePay = () => {
  payDialogVisible.value = true
}

const handleConfirmPay = async () => {
  if (!order.value || !paymentMethod.value) return

  try {
    await store.dispatch('order/payOrder', {
      orderId: order.value.id,
      paymentMethod: paymentMethod.value
    })
    payDialogVisible.value = false
    ElMessage.success('支付成功')
    fetchOrderDetail()
  } catch (error) {
    ElMessage.error('支付失败')
  }
}

const handleCancel = async () => {
  try {
    await ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await store.dispatch('order/cancelOrder', order.value.id)
    ElMessage.success('订单已取消')
    fetchOrderDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消订单失败')
    }
  }
}

const handleConfirm = async () => {
  try {
    await ElMessageBox.confirm('确认已收到商品？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await store.dispatch('order/confirmReceipt', order.value.id)
    ElMessage.success('确认收货成功')
    fetchOrderDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('确认收货失败')
    }
  }
}

// 获取订单详情
const fetchOrderDetail = () => {
  const orderId = route.params.id
  if (orderId) {
    store.dispatch('order/fetchOrderDetail', orderId)
  }
}

// 生命周期
onMounted(() => {
  fetchOrderDetail()
})
</script>

<style scoped>
.order-detail {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section {
  margin: 24px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
}

.section h4 {
  margin: 0 0 16px;
  font-size: 16px;
}

.status-section {
  margin: 32px 0;
}

.label {
  color: #666;
  margin-right: 8px;
}

.address-info p,
.order-info p {
  margin: 8px 0;
}

.products-list {
  margin-top: 16px;
}

.product-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.product-item:last-child {
  border-bottom: none;
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  margin-right: 16px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 14px;
  margin-bottom: 8px;
}

.product-meta {
  color: #666;
  font-size: 14px;
}

.product-subtotal {
  font-size: 16px;
  font-weight: bold;
  color: #ff6b6b;
}

.amount-section {
  margin-top: 24px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
}

.amount-item {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}

.amount-item.total {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  font-size: 16px;
}

.price {
  color: #ff6b6b;
  font-weight: bold;
}

.actions-section {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  gap: 16px;
}

/* 支付对话框样式 */
.pay-dialog {
  padding: 20px 0;
}

.pay-amount {
  font-size: 16px;
  margin-bottom: 24px;
}

.pay-amount .price {
  font-size: 24px;
  margin-left: 8px;
}

.pay-method h4 {
  margin: 0 0 16px;
}

@media (max-width: 768px) {
  .product-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .product-image {
    margin-bottom: 12px;
  }

  .product-subtotal {
    margin-top: 12px;
  }

  .actions-section {
    flex-direction: column;
  }
}
</style> 