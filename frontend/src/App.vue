<script setup>
import { ref, onMounted, reactive } from 'vue'; // 确保导入了 reactive
import touristApiService from './services/touristApi';
import { ElMessage } from 'element-plus';
import { ElDialog, ElForm, ElFormItem, ElInput, ElButton, ElSelect, ElOption } from 'element-plus';


const activeIndex = ref('/');

// 注册相关状态
const registrationDialogVisible = ref(false);
const registrationFormData = reactive({
  username: '',
  password: '',
  email: '',
  first_name: '',
  last_name: '',
  role: ''
});

// 注册表单验证规则
const registrationFormRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少需要 6 位', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
});

// 获取注册表单的引用 (用于手动触发验证和重置)
const registrationFormRef = ref(null);

// 处理导航菜单选择
const handleSelect = (index, indexPath) => {
  console.log('选中:', index);
  activeIndex.value = index;
  // 这里可以根据 index 进行页面滚动或者内容切换，如果需要的话
};

// 显示注册弹窗并重置表单
const showRegistrationDialog = () => {
  // 重置表单数据
  Object.assign(registrationFormData, {
    username: '',
    password: '',
    email: '',
    first_name: '',
    last_name: '',
    role: '' // 重置为空，保持未选择状态
  });
  // 如果有表单引用，清除之前的验证状态
  if (registrationFormRef.value) {
    registrationFormRef.value.resetFields();
  }
  registrationDialogVisible.value = true;
};

// 提交注册表单
const submitRegistration = async () => {
  // 确保获取到表单实例
  if (!registrationFormRef.value) return;

  // 触发表单验证
  registrationFormRef.value.validate(async (valid) => {
    if (valid) {
      // 表单验证通过
      console.log('提交注册数据:', registrationFormData);
      try {
        // 调用 API 服务进行注册 (确保 touristApiService 中有 registerUser 方法)
        const response = await touristApiService.registerUser(registrationFormData);
        console.log('注册成功响应:', response.data);
        ElMessage({
          message: '注册成功！',
          type: 'success',
        });
        registrationDialogVisible.value = false; // 关闭弹窗
        // 可以在此处添加自动登录或跳转到登录页面的逻辑
      } catch (error) {
        console.error('注册失败:', error);
        // 根据后端返回的错误信息进行提示，尝试获取后端返回的特定消息
        const errorMessage = error.response?.data?.message // 检查后端是否有 'message' 字段
                           || error.response?.data?.detail // 检查后端是否有 'detail' 字段 (DRF 常用)
                           || error.response?.data?.username?.[0] // 检查特定字段错误，如用户名重复
                           || error.message // axios 或网络错误消息
                           || '注册失败，请稍后再试。'; // 备用提示
        ElMessage({
          message: errorMessage,
          type: 'error',
        });
      }
    } else {
      // 表单验证失败
      console.log('表单验证失败');
      ElMessage({
        message: '请检查表单输入是否正确',
        type: 'warning',
      });
      return false;
    }
  });
};


onMounted(async () => {
  try {
    activityList.value = await touristApiService.getActivities();
    productList.value = await touristApiService.getProducts();
  } catch (error) {
    console.error('获取数据失败:', error);
  }
});

</script>

<template>
  <el-container>
    <el-header class="header">
      <div class="logo">
        <router-link to="/">
          <span>乡村活动平台</span>
        </router-link>
      </div>
      <div class="nav-menu">
        <el-menu mode="horizontal" :default-active="activeIndex" @select="handleSelect" router>
          <el-menu-item index="/">首页</el-menu-item> <el-menu-item index="/activities">活动</el-menu-item> <el-menu-item index="/products">商品</el-menu-item>  </el-menu>
      </div>
      <div class="nav-right">
        <el-input placeholder="搜索" class="search-input" />
        <el-button type="primary" size="small">登录</el-button>
        <el-button size="small" @click="showRegistrationDialog">注册</el-button>
      </div>
    </el-header>
    <el-main class="main">
      <router-view></router-view>

    </el-main>
    <el-footer class="footer">
       © 2023 乡村活动平台. All rights reserved.
    </el-footer>

    <el-dialog v-model="registrationDialogVisible" title="用户注册" width="30%" :before-close="() => registrationDialogVisible = false">
      <el-form :model="registrationFormData" :rules="registrationFormRules" ref="registrationFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registrationFormData.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="registrationFormData.password" show-password></el-input>
        </el-form-item>
         <el-form-item label="邮箱" prop="email">
          <el-input v-model="registrationFormData.email"></el-input>
        </el-form-item>
         <el-form-item label="名" prop="first_name">
          <el-input v-model="registrationFormData.first_name"></el-input>
        </el-form-item>
         <el-form-item label="姓" prop="last_name">
          <el-input v-model="registrationFormData.last_name"></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="registrationFormData.role" placeholder="请选择注册角色">
            <el-option label="游客" value="tourist"></el-option>
            <el-option label="农户" value="farmer"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="registrationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRegistration">注册</el-button>
        </span>
      </template>
    </el-dialog>


  </el-container>
</template>

<style scoped>
/* 保持原有的样式 */
.header {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 0 20px;
}

.logo {
    font-size: 20px;
    font-weight: bold;
    margin-right: 40px;
    color: #4CAF50;
}

.nav-menu {
  flex-grow: 1;
  display: flex;
  justify-content: center;
}

.nav-menu .el-menu {
  width: fit-content;
  border-bottom: none;
}

.nav-menu .el-menu-item {
    font-size: 16px;
    padding: 0 20px;
}


.nav-right {
  display: flex;
  align-items: center;

}

.search-input {
  width: 200px;
  margin-right: 10px;
}

.main {
  padding: 20px 0;
}
.footer {
  text-align: center;
  padding: 20px; /* 增加内边距 */
  background-color: #f0f0f0; /* 浅灰色背景 */
  border-top: 1px solid #ddd;
  color: #555;
  font-size: 0.9em;
}
</style>