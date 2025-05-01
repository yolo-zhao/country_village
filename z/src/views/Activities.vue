<template>
  <div class="activities-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>活动列表</h3>
          <el-button type="primary" @click="handleCreate" v-if="userRole === 'admin'">
            创建活动
          </el-button>
        </div>
      </template>

      <el-table :data="activities" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="活动标题" />
        <el-table-column prop="description" label="活动描述" />
        <el-table-column prop="start_time" label="开始时间" />
        <el-table-column prop="end_time" label="结束时间" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">
              查看详情
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDelete(row)"
              v-if="userRole === 'admin'"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        class="pagination"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const store = useStore()
const loading = ref(false)
const activities = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const userRole = computed(() => store.getters.userRole)

const getStatusType = (status) => {
  const types = {
    'pending': 'warning',
    'ongoing': 'success',
    'completed': 'info',
    'cancelled': 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'pending': '未开始',
    'ongoing': '进行中',
    'completed': '已结束',
    'cancelled': '已取消'
  }
  return texts[status] || status
}

const fetchActivities = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/activities/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    activities.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('Fetch activities error:', error)
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchActivities()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchActivities()
}

const handleCreate = () => {
  // TODO: 实现创建活动功能
}

const handleView = (row) => {
  // TODO: 实现查看活动详情功能
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/activities/${row.id}/`)
    ElMessage.success('删除成功')
    fetchActivities()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Delete activity error:', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
.activities-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 