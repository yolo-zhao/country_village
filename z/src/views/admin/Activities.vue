<template>
  <div class="admin-activities">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>活动管理</h3>
          <el-button type="primary" @click="handleAdd">添加活动</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="活动名称">
            <el-input v-model="searchForm.name" placeholder="请输入活动名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="未开始" value="pending" />
              <el-option label="进行中" value="active" />
              <el-option label="已结束" value="ended" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 活动列表 -->
      <el-table :data="activities" border style="width: 100%">
        <el-table-column prop="name" label="活动名称" />
        <el-table-column prop="description" label="活动描述" show-overflow-tooltip />
        <el-table-column prop="start_time" label="开始时间" />
        <el-table-column prop="end_time" label="结束时间" />
        <el-table-column prop="max_participants" label="最大参与人数" />
        <el-table-column prop="current_participants" label="当前参与人数" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusName(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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

    <!-- 添加/编辑活动对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="活动描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择开始时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选择结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="最大参与人数" prop="max_participants">
          <el-input-number v-model="form.max_participants" :min="1" />
        </el-form-item>
        <el-form-item label="活动状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="未开始" value="pending" />
            <el-option label="进行中" value="active" />
            <el-option label="已结束" value="ended" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
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
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('添加活动')
const formRef = ref(null)

// 搜索表单
const searchForm = ref({
  name: '',
  status: ''
})

// 表单数据
const form = ref({
  id: '',
  name: '',
  description: '',
  start_time: '',
  end_time: '',
  max_participants: 1,
  status: 'pending'
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入活动名称', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入活动描述', trigger: 'blur' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  max_participants: [
    { required: true, message: '请输入最大参与人数', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择活动状态', trigger: 'change' }
  ]
}

// 从 store 获取活动列表
const activities = computed(() => store.state.admin.activities)

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'info',
    active: 'success',
    ended: 'warning',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态名称
const getStatusName = (status) => {
  const names = {
    pending: '未开始',
    active: '进行中',
    ended: '已结束',
    cancelled: '已取消'
  }
  return names[status] || status
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchActivities()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    name: '',
    status: ''
  }
  handleSearch()
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchActivities()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchActivities()
}

// 添加活动
const handleAdd = () => {
  dialogTitle.value = '添加活动'
  form.value = {
    id: '',
    name: '',
    description: '',
    start_time: '',
    end_time: '',
    max_participants: 1,
    status: 'pending'
  }
  dialogVisible.value = true
}

// 编辑活动
const handleEdit = (row) => {
  dialogTitle.value = '编辑活动'
  form.value = { ...row }
  dialogVisible.value = true
}

// 删除活动
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await store.dispatch('admin/deleteActivity', row.id)
    ElMessage.success('删除成功')
    fetchActivities()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    if (form.value.id) {
      await store.dispatch('admin/updateActivity', form.value)
      ElMessage.success('更新成功')
    } else {
      await store.dispatch('admin/createActivity', form.value)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    fetchActivities()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 获取活动列表
const fetchActivities = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      ...searchForm.value
    }
    
    await store.dispatch('admin/fetchActivities', params)
    total.value = store.state.admin.total
  } catch (error) {
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
.admin-activities {
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