<template>
  <div class="tourist-orders">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>我的订单</h3>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="订单号">
            <el-input v-model="searchForm.order_no" placeholder="请输入订单号" clearable />
          </el-form-item>
          <el-form-item label="订单状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="待付款" value="pending" />
              <el-option label="已付款" value="paid" />
              <el-option label="已发货" value="shipped" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="下单时间">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 订单列表 -->
      <el-table :data="orders" border style="width: 100%">
        <el-table-column prop="order_no" label="订单号" width="180" />
        <el-table-column prop="total_amount" label="订单金额">
          <template #default="{ row }">
            ¥{{ row.total_amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="订单状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="shipping_address" label="收货地址" show-overflow-tooltip />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleViewDetail(row)">查看详情</el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              link
              @click="handlePay(row)"
            >
              付款
            </el-button>
            <el-button
              v-if="row.status === 'shipped'"
              type="success"
              link
              @click="handleConfirmReceipt(row)"
            >
              确认收货
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              link
              @click="handleCancel(row)"
            >
              取消订单
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="订单详情"
      width="800px"
      destroy-on-close
    >
      <div v-if="currentOrder" class="order-detail">
        <div class="detail-section">
          <h4>订单信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="订单号">{{ currentOrder.order_no }}</el-descriptions-item>
            <el-descriptions-item label="订单状态">
              <el-tag :type="getStatusType(currentOrder.status)">
                {{ getStatusText(currentOrder.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="下单时间">{{ formatDate(currentOrder.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="订单金额">¥{{ currentOrder.total_amount.toFixed(2) }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="detail-section">
          <h4>收货信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="收货人">{{ currentOrder.receiver_name }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ currentOrder.receiver_phone }}</el-descriptions-item>
            <el-descriptions-item label="收货地址" :span="2">{{ currentOrder.shipping_address }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="detail-section">
          <h4>商品信息</h4>
          <el-table :data="currentOrder.items" border>
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="quantity" label="数量" width="100" />
            <el-table-column prop="price" label="单价" width="120">
              <template #default="{ row }">
                ¥{{ row.price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="subtotal" label="小计" width="120">
              <template #default="{ row }">
                ¥{{ (row.price * row.quantity).toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div v-if="currentOrder.status === 'shipped'" class="detail-section">
          <h4>物流信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="物流公司">{{ currentOrder.shipping_company }}</el-descriptions-item>
            <el-descriptions-item label="物流单号">{{ currentOrder.shipping_no }}</el-descriptions-item>
            <el-descriptions-item label="发货时间">{{ formatDate(currentOrder.shipped_at) }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-dialog>

    <!-- 支付对话框 -->
    <el-dialog
      v-model="payDialogVisible"
      title="订单支付"
      width="500px"
      destroy-on-close
    >
      <div v-if="currentOrder" class="pay-content">
        <p>订单号：{{ currentOrder.order_no }}</p>
        <p>支付金额：<span class="price">¥{{ currentOrder.total_amount.toFixed(2) }}</span></p>
        <div class="payment-methods">
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
          <el-button type="primary" @click="handlePaySubmit">确认支付</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useStore()
const loading = ref(false)
const detailDialogVisible = ref(false)
const payDialogVisible = ref(false)
const currentOrder = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const paymentMethod = ref('alipay')

// 搜索表单
const searchForm = ref({
  order_no: '',
  status: '',
  dateRange: []
})

// 从 store 获取订单列表
const orders = computed(() => store.state.order.orders)

// 获取订单状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    paid: 'primary',
    shipped: 'success',
    completed: 'success',
    cancelled: 'info'
  }
  return types[status] || 'info'
}

// 获取订单状态文本
const getStatusText = (status) => {
  const texts = {
    pending: '待付款',
    paid: '已付款',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchOrders()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    order_no: '',
    status: '',
    dateRange: []
  }
  handleSearch()
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchOrders()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchOrders()
}

// 查看订单详情
const handleViewDetail = async (order) => {
  try {
    loading.value = true
    await store.dispatch('order/fetchOrderDetail', order.id)
    currentOrder.value = store.state.order.currentOrder
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取订单详情失败')
  } finally {
    loading.value = false
  }
}

// 支付订单
const handlePay = (order) => {
  currentOrder.value = order
  payDialogVisible.value = true
}

// 提交支付
const handlePaySubmit = async () => {
  try {
    loading.value = true
    await store.dispatch('order/payOrder', {
      id: currentOrder.value.id,
      payment_method: paymentMethod.value
    })
    ElMessage.success('支付成功')
    payDialogVisible.value = false
    fetchOrders()
  } catch (error) {
    ElMessage.error('支付失败')
  } finally {
    loading.value = false
  }
}

// 确认收货
const handleConfirmReceipt = async (order) => {
  try {
    await ElMessageBox.confirm('确认已收到商品？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await store.dispatch('order/confirmReceipt', order.id)
    ElMessage.success('确认收货成功')
    fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('确认收货失败')
    }
  } finally {
    loading.value = false
  }
}

// 取消订单
const handleCancel = async (order) => {
  try {
    await ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await store.dispatch('order/cancelOrder', order.id)
    ElMessage.success('取消订单成功')
    fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消订单失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取订单列表
const fetchOrders = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      ...searchForm.value
    }
    
    if (params.dateRange && params.dateRange.length === 2) {
      params.start_date = params.dateRange[0]
      params.end_date = params.dateRange[1]
      delete params.dateRange
    }
    
    await store.dispatch('order/fetchOrders', params)
    total.value = store.state.order.total
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.tourist-orders {
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #606266;
}

:deep(.el-descriptions) {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 100px;
}

.pay-content {
  text-align: center;
}

.pay-content p {
  margin: 16px 0;
  font-size: 16px;
}

.pay-content .price {
  color: #f56c6c;
  font-size: 24px;
  font-weight: bold;
}

.payment-methods {
  margin-top: 24px;
  text-align: left;
}

.payment-methods h4 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #606266;
}
</style> 