<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '../../api/products'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 获取产品ID（如果是编辑模式）
const productId = computed(() => route.params.id)

// 判断是否是编辑模式
const isEditMode = computed(() => !!productId.value)

// 页面标题
const pageTitle = computed(() => isEditMode.value ? '编辑产品' : '添加新产品')

// 产品表单数据
const productForm = reactive({
  name: '',
  description: '',
  price: 0,
  stock: 1,
  status: 'published',
  images: []
})

// 表单规则
const rules = {
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度应在2-100个字符之间', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入产品描述', trigger: 'blur' }
  ],
  price: [
    { required: true, type: 'number', message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '价格必须大于0', trigger: 'blur' }
  ],
  stock: [
    { required: true, type: 'number', message: '请输入库存数量', trigger: 'blur' },
    { type: 'number', min: 0, message: '库存不能为负数', trigger: 'blur' }
  ]
}

// 表单引用
const formRef = ref(null)

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 上传图片列表
const fileList = ref([])

// 获取产品详情（编辑模式）
const fetchProductDetail = async () => {
  if (!isEditMode.value) return
  
  loading.value = true
  try {
    const response = await productApi.getProductDetail(productId.value)
    const product = response.data
    
    // 填充表单数据
    productForm.name = product.name
    productForm.description = product.description
    productForm.price = parseFloat(product.price)
    productForm.stock = product.stock
    productForm.status = product.status
    
    // 处理图片列表
    if (product.images && product.images.length > 0) {
      productForm.images = product.images.map(img => img.image)
      fileList.value = product.images.map(img => ({
        name: img.caption || '产品图片',
        url: img.image
      }))
    }
  } catch (error) {
    console.error('获取产品详情失败:', error)
    ElMessage.error('获取产品详情失败')
    router.push('/farmer/dashboard')
  } finally {
    loading.value = false
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        // 准备图片数据
        const imagesData = fileList.value
          .filter(file => file && file.url) // 过滤掉空URL
          .map(file => {
            // 检查URL是否是HTTP(S)链接
            const isHttpUrl = typeof file.url === 'string' && 
                          (file.url.startsWith('http://') || file.url.startsWith('https://'));
            
            // 区分URL和文件
            if (file.is_url || isHttpUrl) {
              return {
                image_url: file.url,
                caption: file.name
              }
            } else {
              return {
                image: file.url,
                caption: file.name
              }
            }
          });
        
        const submitData = {
          ...productForm,
          images: imagesData
        }
        
        console.log('提交的产品数据:', submitData);
        
        if (isEditMode.value) {
          // 编辑产品
          await productApi.updateProduct(productId.value, submitData)
          ElMessage.success('产品更新成功')
        } else {
          // 创建产品
          await productApi.createProduct(submitData)
          ElMessage.success('产品添加成功')
        }
        
        // 返回到农场主管理面板
        router.push('/farmer/dashboard')
      } catch (error) {
        console.error('保存产品失败:', error)
        ElMessage.error('保存产品失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 取消操作
const cancelForm = () => {
  ElMessageBox.confirm(
    '确定要取消吗？所有未保存的更改将丢失。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    router.push('/farmer/dashboard')
  }).catch(() => {})
}

// 上传图片成功
const handleUploadSuccess = (res) => {
  console.log('图片上传成功:', res);
  
  // 添加调试日志
  if (res && res.url) {
    console.log('获取到图片URL:', res.url);
  } else if (res && res.data && res.data.url) {
    console.log('从data中获取图片URL:', res.data.url);
  } else {
    console.warn('未能找到有效的图片URL:', res);
  }
  
  let imageUrl = '';
  if (res && res.url) {
    imageUrl = res.url;
  } else if (res && res.data && res.data.url) {
    imageUrl = res.data.url;
  }
  
  if (imageUrl) {
    // 确保URL格式正确
    if (imageUrl.startsWith('/media/')) {
      // 如果是相对路径，不需要前缀
      imageUrl = imageUrl.substring(7); // 移除 /media/ 前缀
    } else if (imageUrl.includes('/media/')) {
      // 尝试提取media后的路径
      const match = imageUrl.match(/\/media\/(.*)/);
      if (match && match[1]) {
        imageUrl = match[1];
      }
    }
    
    // 使用image_url字段存储完整URL
    fileList.value.push({
      name: res.name || '产品图片',
      url: imageUrl,
      is_url: true  // 标记这是一个URL，不是文件对象
    });
    console.log('当前图片列表:', fileList.value);
  } else {
    ElMessage.warning('图片上传成功，但无法获取图片URL');
  }
}

// 移除图片
const handleRemove = (file) => {
  const index = fileList.value.findIndex(item => item.url === file.url)
  if (index !== -1) {
    fileList.value.splice(index, 1)
    productForm.images.splice(index, 1)
  }
}

// 图片上传前的验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!')
    return false
  }
  
  return true
}

// 页面加载时获取数据
onMounted(() => {
  fetchProductDetail()
})
</script>

<template>
  <div class="product-form-page">
    <h1 class="page-title">{{ pageTitle }}</h1>
    
    <el-skeleton :rows="10" animated v-if="loading" />
    
    <el-form
      v-else
      ref="formRef"
      :model="productForm"
      :rules="rules"
      label-width="120px"
      class="product-form"
    >
      <el-form-item label="产品名称" prop="name">
        <el-input v-model="productForm.name" placeholder="请输入产品名称" />
      </el-form-item>
      
      <el-form-item label="产品描述" prop="description">
        <el-input
          v-model="productForm.description"
          type="textarea"
          rows="5"
          placeholder="请详细描述产品的特点、用途、产地等信息"
        />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="价格 (元)" prop="price">
            <el-input-number 
              v-model="productForm.price" 
              :precision="2" 
              :step="0.1" 
              :min="0.01" 
              controls-position="right"
              style="width: 100%;"
            />
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="库存数量" prop="stock">
            <el-input-number 
              v-model="productForm.stock" 
              :min="0" 
              :step="1" 
              controls-position="right"
              style="width: 100%;"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="产品状态" prop="status">
        <el-radio-group v-model="productForm.status">
          <el-radio label="published">上架销售</el-radio>
          <el-radio label="unavailable">下架</el-radio>
          <el-radio label="sold_out" :disabled="true">售罄</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="产品图片">
        <el-upload
          class="product-uploader"
          action="/api/upload/"
          :headers="{
            Authorization: `Token ${userStore.getToken}`
          }"
          :file-list="fileList"
          list-type="picture-card"
          :on-success="handleUploadSuccess"
          :on-remove="handleRemove"
          :before-upload="beforeUpload"
          multiple
        >
          <el-icon><Plus /></el-icon>
        </el-upload>
        <div class="upload-tip">请上传产品图片，支持多张，每张不超过2MB</div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="submitLoading">
          {{ isEditMode ? '保存修改' : '添加产品' }}
        </el-button>
        <el-button @click="cancelForm">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.product-form-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 1.8rem;
  margin-bottom: 30px;
  text-align: center;
}

.product-form {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.product-uploader {
  width: 100%;
}

.upload-tip {
  margin-top: 10px;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}
</style> 