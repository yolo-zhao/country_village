<template>
  <div class="admin-comments">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>评论管理</h3>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="产品名称">
            <el-input v-model="searchForm.product_name" placeholder="请输入产品名称" clearable />
          </el-form-item>
          <el-form-item label="用户">
            <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="待审核" value="pending" />
              <el-option label="已通过" value="approved" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 评论列表 -->
      <el-table :data="comments" border style="width: 100%">
        <el-table-column prop="product_name" label="产品名称" />
        <el-table-column prop="username" label="用户" />
        <el-table-column prop="content" label="评论内容" />
        <el-table-column prop="rating" label="评分">
          <template #default="{ row }">
            <el-rate v-model="row.rating" disabled />
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
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button 
              v-if="row.status === 'pending'"
              type="success" 
              size="small" 
              @click="handleApprove(row)"
            >通过</el-button>
            <el-button 
              v-if="row.status === 'pending'"
              type="danger" 
              size="small" 
              @click="handleReject(row)"
            >拒绝</el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDelete(row)"
            >删除</el-button>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useStore()
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 搜索表单
const searchForm = ref({
  product_name: '',
  username: '',
  status: ''
})

// 从 store 获取评论列表
const comments = computed(() => store.state.admin.comments)

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态名称
const getStatusName = (status) => {
  const names = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return names[status] || status
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchComments()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    product_name: '',
    username: '',
    status: ''
  }
  handleSearch()
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchComments()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchComments()
}

// 审核通过
const handleApprove = async (row) => {
  try {
    loading.value = true
    await store.dispatch('admin/approveComment', row.id)
    ElMessage.success('审核通过')
    fetchComments()
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    loading.value = false
  }
}

// 审核拒绝
const handleReject = async (row) => {
  try {
    loading.value = true
    await store.dispatch('admin/rejectComment', row.id)
    ElMessage.success('已拒绝')
    fetchComments()
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    loading.value = false
  }
}

// 删除评论
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await store.dispatch('admin/deleteComment', row.id)
    ElMessage.success('删除成功')
    fetchComments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取评论列表
const fetchComments = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      ...searchForm.value
    }
    
    await store.dispatch('admin/fetchComments', params)
    total.value = store.state.admin.total
  } catch (error) {
    ElMessage.error('获取评论列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.admin-comments {
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
</style> 