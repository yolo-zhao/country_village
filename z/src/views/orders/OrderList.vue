<template>
  <div class="order-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>我的订单</h3>
        </div>
      </template>

      <!-- 状态标签栏 -->
      <div class="status-tabs">
        <el-tabs v-model="activeStatus" @tab-change="handleStatusChange">
          <el-tab-pane label="全部" name="">
            <span class="tab-label">全部 ({{ total }})</span>
          </el-tab-pane>
          <el-tab-pane label="待支付" name="pending">
            <span class="tab-label">
              待支付 ({{ orderCountByStatus.pending }})
            </span>
          </el-tab-pane>
          <el-tab-pane label="待发货" name="paid">
            <span class="tab-label">
              待发货 ({{ orderCountByStatus.paid }})
            </span>
          </el-tab-pane>
          <el-tab-pane label="待收货" name="shipped">
            <span class="tab-label">
              待收货 ({{ orderCountByStatus.shipped }})
            </span>
          </el-tab-pane>
          <el-tab-pane label="已完成" name="completed">
            <span class="tab-label">
              已完成 ({{ orderCountByStatus.completed }})
            </span>
          </el-tab-pane>
          <el-tab-pane label="已取消" name="cancelled">
            <span class="tab-label">
              已取消 ({{ orderCountByStatus.cancelled }})
            </span>
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="订单号">
            <el-input
              v-model="searchForm.orderNumber"
              placeholder="请输入订单号"
              clearable
              @keyup.enter="handleSearch"
            />
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
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 订单列表 -->
      <div class="order-table" v-loading="loading">
        <el-table :data="orders" style="width: 100%">
          <el-table-column label="订单信息" min-width="300">
            <template #default="{ row }">
              <div v-for="item in row.items" :key="item.id" class="order-item">
                <el-image
                  :src="item.product.image || '/default-product.jpg'"
                  class="product-image"
                  fit="cover"
                />
                <div class="product-info">
                  <div class="product-name">{{ item.product.name }}</div>
                  <div class="product-price">
                    ¥{{ item.price.toFixed(2) }} × {{ item.quantity }}
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="收货信息" min-width="200">
            <template #default="{ row }">
              <div class="address-info">
                <p>{{ row.address.receiver }}</p>
                <p>{{ row.address.phone }}</p>
                <p>{{ row.address.address }}</p>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="total_amount" label="实付金额" width="120">
            <template #default="{ row }">
              <span class="price">¥{{ row.total_amount.toFixed(2) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="status" label="订单状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button
                  v-if="row.status === 'pending'"
                  type="primary"
                  size="small"
                  @click="handlePay(row)"
                >
                  去支付
                </el-button>
                <el-button
                  v-if="row.status === 'pending'"
                  type="danger"
                  size="small"
                  @click="handleCancel(row)"
                >
                  取消订单
                </el-button>
                <el-button
                  v-if="row.status === 'shipped'"
                  type="success"
                  size="small"
                  @click="handleConfirm(row)"
                >
                  确认收货
                </el-button>
                <el-button
                  link
                  type="primary"
                  @click="handleViewDetail(row)"
                >
                  查看详情
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
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
          支付金额：<span class="price">¥{{ currentOrder?.total_amount.toFixed(2) }}</span>
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useStore()
const router = useRouter()

// 数据
const activeStatus = ref('')
const searchForm = ref({
  orderNumber: '',
  dateRange: []
})
const payDialogVisible = ref(false)
const paymentMethod = ref('alipay')
const currentOrder = ref(null)

// 从 store 获取数据
const loading = computed(() => store.state.order.loading)
const orders = computed(() => store.state.order.orders)
const total = computed(() => store.state.order.total)
const currentPage = computed({
  get: () => store.state.order.currentPage,
  set: (val) => store.commit('order/SET_PAGE', val)
})
const pageSize = computed({
  get: () => store.state.order.pageSize,
  set: (val) => store.commit('order/SET_PAGE_SIZE', val)
})
const orderCountByStatus = computed(() => store.getters['order/orderCountByStatus'])

// 状态相关
const statusMap = {
  pending: { type: 'warning', text: '待支付' },
  paid: { type: 'info', text: '待发货' },
  shipped: { type: 'primary', text: '待收货' },
  completed: { type: 'success', text: '已完成' },
  cancelled: { type: 'danger', text: '已取消' }
}

const getStatusType = (status) => statusMap[status]?.type || 'info'
const getStatusText = (status) => statusMap[status]?.text || status

// 事件处理
const handleStatusChange = () => {
  currentPage.value = 1
  fetchOrders()
}

const handleSearch = () => {
  currentPage.value = 1
  fetchOrders()
}

const handleReset = () => {
  searchForm.value = {
    orderNumber: '',
    dateRange: []
  }
  handleSearch()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchOrders()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchOrders()
}

const handleViewDetail = (order) => {
  router.push(`/orders/${order.id}`)
}

const handlePay = (order) => {
  currentOrder.value = order
  payDialogVisible.value = true
}

const handleConfirmPay = async () => {
  if (!currentOrder.value || !paymentMethod.value) return

  try {
    await store.dispatch('order/payOrder', {
      orderId: currentOrder.value.id,
      paymentMethod: paymentMethod.value
    })
    payDialogVisible.value = false
    ElMessage.success('支付成功')
    fetchOrders()
  } catch (error) {
    ElMessage.error('支付失败')
  }
}

const handleCancel = async (order) => {
  try {
    await ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await store.dispatch('order/cancelOrder', order.id)
    ElMessage.success('订单已取消')
    fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消订单失败')
    }
  }
}

const handleConfirm = async (order) => {
  try {
    await ElMessageBox.confirm('确认已收到商品？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await store.dispatch('order/confirmReceipt', order.id)
    ElMessage.success('确认收货成功')
    fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('确认收货失败')
    }
  }
}

// 获取订单列表
const fetchOrders = () => {
  const params = {
    page: currentPage.value,
    pageSize: pageSize.value,
    status: activeStatus.value,
    order_number: searchForm.value.orderNumber,
    start_date: searchForm.value.dateRange?.[0],
    end_date: searchForm.value.dateRange?.[1]
  }
  store.dispatch('order/fetchOrders', params)
}

// 生命周期
onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.order-list {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-tabs {
  margin-bottom: 20px;
}

.tab-label {
  font-size: 14px;
}

.search-bar {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.order-item:not(:last-child) {
  border-bottom: 1px solid #eee;
}

.product-image {
  width: 60px;
  height: 60px;
  border-radius: 4px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 14px;
  margin-bottom: 4px;
}

.product-price {
  color: #666;
  font-size: 13px;
}

.address-info {
  font-size: 14px;
  line-height: 1.5;
}

.address-info p {
  margin: 0;
}

.price {
  color: #ff6b6b;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
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
  .search-form {
    flex-direction: column;
  }

  .action-buttons {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
</style> 