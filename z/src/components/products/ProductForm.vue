<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-width="100px"
    class="product-form"
  >
    <el-form-item label="产品名称" prop="name">
      <el-input v-model="form.name" placeholder="请输入产品名称" />
    </el-form-item>

    <el-form-item label="产品分类" prop="category">
      <el-select v-model="form.category" placeholder="请选择产品分类">
        <el-option
          v-for="item in categories"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </el-form-item>

    <el-form-item label="产品价格" prop="price">
      <el-input-number
        v-model="form.price"
        :min="0"
        :precision="2"
        :step="0.1"
        style="width: 200px"
      />
    </el-form-item>

    <el-form-item label="库存数量" prop="stock">
      <el-input-number
        v-model="form.stock"
        :min="0"
        :precision="0"
        style="width: 200px"
      />
    </el-form-item>

    <el-form-item label="产品图片" prop="image">
      <el-upload
        class="product-image-upload"
        :action="uploadUrl"
        :headers="uploadHeaders"
        :show-file-list="false"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
      >
        <el-image
          v-if="form.image"
          :src="form.image"
          class="preview-image"
          fit="cover"
        />
        <el-icon v-else class="upload-icon"><Plus /></el-icon>
      </el-upload>
      <div class="upload-tip">建议尺寸：800x800px，支持 jpg、png 格式</div>
    </el-form-item>

    <el-form-item label="产品描述" prop="description">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="4"
        placeholder="请输入产品描述"
      />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="handleSubmit">保存</el-button>
      <el-button @click="$emit('cancel')">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  product: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formRef = ref(null)
const form = ref({
  name: '',
  category: '',
  price: 0,
  stock: 0,
  image: '',
  description: ''
})

const categories = [
  { label: '水果', value: 'fruits' },
  { label: '蔬菜', value: 'vegetables' },
  { label: '粮食', value: 'grains' },
  { label: '特产', value: 'specialties' },
  { label: '其他', value: 'others' }
]

const rules = {
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择产品分类', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入产品价格', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存数量', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入产品描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ]
}

// 上传相关
const uploadUrl = '/api/upload/'
const uploadHeaders = {
  'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)?.[1] || ''
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

const handleUploadSuccess = (response) => {
  form.value.image = response.url
  ElMessage.success('上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

// 表单提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    emit('submit', { ...form.value })
  } catch (error) {
    console.error('Validation error:', error)
  }
}

// 初始化表单数据
onMounted(() => {
  if (props.product) {
    form.value = { ...props.product }
  }
})
</script>

<style scoped>
.product-form {
  max-width: 600px;
  margin: 0 auto;
}

.product-image-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.product-image-upload:hover {
  border-color: var(--el-color-primary);
}

.preview-image {
  width: 100%;
  height: 100%;
}

.upload-icon {
  font-size: 28px;
  color: #8c939d;
}

.upload-tip {
  font-size: 12px;
  color: #606266;
  margin-top: 8px;
}
</style> 