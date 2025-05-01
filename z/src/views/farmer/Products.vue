<template>
  <div class="farmer-products">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>产品管理</h3>
          <el-button type="primary" @click="handleAdd">添加产品</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="产品名称">
            <el-input v-model="searchForm.name" placeholder="请输入产品名称" clearable />
          </el-form-item>
          <el-form-item label="产品状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="上架" value="active" />
              <el-option label="下架" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 产品列表 -->
      <el-table :data="products" border style="width: 100%">
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="category" label="产品类别" />
        <el-table-column prop="price" label="价格">
          <template #default="{ row }">
            ¥{{ row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button
              type="primary"
              link
              @click="handleStatusChange(row)"
            >
              {{ row.status === 'active' ? '下架' : '上架' }}
            </el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
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

    <!-- 产品表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加产品' : '编辑产品'"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="产品类别" prop="category">
          <el-select v-model="form.category" placeholder="请选择类别">
            <el-option label="水果" value="fruit" />
            <el-option label="蔬菜" value="vegetable" />
            <el-option label="粮食" value="grain" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="产品价格" prop="price">
          <el-input-number v-model="form.price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="产品库存" prop="stock">
          <el-input-number v-model="form.stock" :min="0" :precision="0" />
        </el-form-item>
        <el-form-item label="产品图片" prop="image">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <img v-if="form.image" :src="form.image" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="产品描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入产品描述"
          />
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
import { Plus } from '@element-plus/icons-vue'

const store = useStore()
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 搜索表单
const searchForm = ref({
  name: '',
  status: ''
})

// 产品表单
const form = ref({
  name: '',
  category: '',
  price: 0,
  stock: 0,
  image: '',
  description: ''
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择产品类别', trigger: 'change' }],
  price: [{ required: true, message: '请输入产品价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入产品库存', trigger: 'blur' }],
  image: [{ required: true, message: '请上传产品图片', trigger: 'change' }],
  description: [{ required: true, message: '请输入产品描述', trigger: 'blur' }]
}

// 从 store 获取产品列表
const products = computed(() => store.state.product.products)

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
  fetchProducts()
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
  fetchProducts()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchProducts()
}

// 添加产品
const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    name: '',
    category: '',
    price: 0,
    stock: 0,
    image: '',
    description: ''
  }
  dialogVisible.value = true
}

// 编辑产品
const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

// 删除产品
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该产品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await store.dispatch('product/deleteProduct', row.id)
    ElMessage.success('删除成功')
    fetchProducts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 修改产品状态
const handleStatusChange = async (row) => {
  try {
    const newStatus = row.status === 'active' ? 'inactive' : 'active'
    await store.dispatch('product/updateProductStatus', {
      id: row.id,
      status: newStatus
    })
    ElMessage.success('状态更新成功')
    fetchProducts()
  } catch (error) {
    ElMessage.error('状态更新失败')
  }
}

// 图片上传
const handleUploadSuccess = (response) => {
  form.value.image = response.url
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return false
  }
  return true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    if (dialogType.value === 'add') {
      await store.dispatch('product/createProduct', form.value)
      ElMessage.success('添加成功')
    } else {
      await store.dispatch('product/updateProduct', form.value)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    fetchProducts()
  } catch (error) {
    ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
  } finally {
    loading.value = false
  }
}

// 获取产品列表
const fetchProducts = async () => {
  loading.value = true
  try {
    await store.dispatch('product/fetchProducts', {
      page: currentPage.value,
      pageSize: pageSize.value,
      ...searchForm.value
    })
    total.value = store.state.product.total
  } catch (error) {
    ElMessage.error('获取产品列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.farmer-products {
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

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 178px;
  height: 178px;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style> 