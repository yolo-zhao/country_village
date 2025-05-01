<template>
  <div class="admin-orders">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>订单管理</h3>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="订单号">
            <el-input v-model="searchForm.order_number" placeholder="请输入订单号" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="待付款" value="pending" />
              <el-option label="待发货" value="paid" />
              <el-option label="已发货" value="shipped" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="日期范围">
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
        <el-table-column prop="order_number" label="订单号" />
        <el-table-column prop="total_amount" label="总金额">
          <template #default="{ row }">
            ¥{{ row.total_amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column prop="shipping_address" label="收货地址" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleViewDetails(row)">查看详情</el-button>
            <el-button 
              v-if="row.status === 'paid'"
              type="success" 
              size="small" 
              @click="handleShip(row)"
            >发货</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 订单详情对话框 -->
    <el-dialog
      title="订单详情"
      v-model="detailsVisible"
      width="800px"
    >
      <div v-if="currentOrder">
        <h4>订单信息</h4>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ currentOrder.order_number }}</el-descriptions-item>
          <el-descriptions-item label="总金额">¥{{ currentOrder.total_amount.toFixed(2) }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentOrder.status)">
              {{ getStatusName(currentOrder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentOrder.created_at }}</el-descriptions-item>
        </el-descriptions>

        <h4>收货信息</h4>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="收货人">{{ currentOrder.shipping_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.shipping_phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2">{{ currentOrder.shipping_address }}</el-descriptions-item>
        </el-descriptions>

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

        <h4 v-if="currentOrder.status === 'shipped' || currentOrder.status === 'completed'">物流信息</h4>
        <el-descriptions v-if="currentOrder.status === 'shipped' || currentOrder.status === 'completed'" :column="2" border>
          <el-descriptions-item label="物流公司">{{ currentOrder.shipping_company }}</el-descriptions-item>
          <el-descriptions-item label="物流单号">{{ currentOrder.tracking_number }}</el-descriptions-item>
          <el-descriptions-item label="发货时间">{{ currentOrder.shipped_at }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 发货对话框 -->
    <el-dialog
      title="订单发货"
      v-model="shipVisible"
      width="500px"
    >
      <el-form
        ref="shipFormRef"
        :model="shipForm"
        :rules="shipRules"
        label-width="100px"
      >
        <el-form-item label="物流公司" prop="shipping_company">
          <el-input v-model="shipForm.shipping_company" />
        </el-form-item>
        <el-form-item label="物流单号" prop="tracking_number">
          <el-input v-model="shipForm.tracking_number" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="shipVisible = false">取消</el-button>
          <el-button type="primary" @click="handleShipSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const store = useStore()
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const detailsVisible = ref(false)
const shipVisible = ref(false)
const currentOrder = ref(null)
const shipFormRef = ref(null)

// 搜索表单
const searchForm = ref({
  order_number: '',
  status: '',
  dateRange: []
})

// 发货表单
const shipForm = ref({
  order_id: '',
  shipping_company: '',
  tracking_number: ''
})

// 发货表单验证规则
const shipRules = {
  shipping_company: [
    { required: true, message: '请输入物流公司', trigger: 'blur' }
  ],
  tracking_number: [
    { required: true, message: '请输入物流单号', trigger: 'blur' }
  ]
}

// 从 store 获取订单列表
const orders = computed(() => store.state.admin.orders)

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    paid: 'primary',
    shipped: 'success',
    completed: 'info',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态名称
const getStatusName = (status) => {
  const names = {
    pending: '待付款',
    paid: '待发货',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return names[status] || status
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchOrders()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    order_number: '',
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
const handleViewDetails = (row) => {
  currentOrder.value = row
  detailsVisible.value = true
}

// 发货
const handleShip = (row) => {
  shipForm.value = {
    order_id: row.id,
    shipping_company: '',
    tracking_number: ''
  }
  shipVisible.value = true
}

// 提交发货
const handleShipSubmit = async () => {
  if (!shipFormRef.value) return
  
  try {
    await shipFormRef.value.validate()
    loading.value = true
    
    await store.dispatch('admin/shipOrder', shipForm.value)
    ElMessage.success('发货成功')
    shipVisible.value = false
    fetchOrders()
  } catch (error) {
    ElMessage.error('发货失败')
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
    
    await store.dispatch('admin/fetchOrders', params)
    total.value = store.state.admin.total
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
.admin-orders {
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

h4 {
  margin: 20px 0 10px;
  font-weight: 500;
}
</style> 