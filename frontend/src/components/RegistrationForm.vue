<template>
  <el-container class="registration-container">
    <el-card class="registration-card">
      <template #header>
        <div class="card-header">
          <span>用户注册</span>
        </div>
      </template>

      <el-form
        ref="registrationFormRef"
        :model="registrationForm"
        :rules="rules"
        label-width="100px"
        @submit.prevent="onSubmit" >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registrationForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="registrationForm.password" placeholder="请输入密码" show-password></el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
           <el-input type="password" v-model="registrationForm.confirmPassword" placeholder="请再次输入密码" show-password></el-input>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registrationForm.email" placeholder="请输入邮箱 (可选)"></el-input>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="registrationForm.role">
            <el-radio label="tourist">游客</el-radio>
            <el-radio label="farmer">农户</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading">注册</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </el-container>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const router = useRouter();

const registrationForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  role: '',
});

// 表单校验规则
const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少需要 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    // 自定义校验规则，检查密码是否匹配
    {
      validator: (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== registrationForm.password) {
          callback(new Error('两次输入的密码不匹配!'));
        } else {
          callback(); // 校验通过
        }
      },
      trigger: 'blur',
    },
  ],
  role: [
    { required: true, message: '请选择您的角色', trigger: 'change' },
  ],
  email: [
     { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }
  ]
});


const registrationFormRef = ref(null);


const loading = ref(false);


const onSubmit = () => {

  registrationFormRef.value.validate(async (valid) => {
    if (valid) {

      loading.value = true; // 显示加载状态

      // 构建发送给后端的数据体
      const postData = {
        username: registrationForm.username,
        password: registrationForm.password, // 发送密码
        email: registrationForm.email || undefined, // 如果邮箱为空，发送 undefined 或忽略该字段
        role: registrationForm.role,
      };

      // 移除空的邮箱字段，避免发送 null 或空字符串
      if (!postData.email) {
          delete postData.email;
      }


      try {

        const backendUrl = 'http://localhost:8000/api/register/'; // !!! 请替换为您的实际后端地址 !!!

        // 使用 Axios 发送 POST 请求
        const response = await axios.post(backendUrl, postData, {
           headers: {
               'Content-Type': 'application/json',
           }

        });

        console.log('注册成功响应:', response.data);


        ElMessage({
          message: response.data.message || '注册成功！',
          type: 'success',
        });

        const router = useRouter();
        router.push('/login');

      } catch (error) {
        // 请求失败，Axios 会捕获非 2xx 状态码或网络错误
        console.error('注册失败:', error);

        let errorMessage = '注册失败。';
        if (error.response) {

          const errorData = error.response.data;
          if (typeof errorData === 'object') {

               for (const field in errorData) {

                   errorMessage += `${field}: ${Array.isArray(errorData[field]) ? errorData[field].join(' ') : errorData[field]} `;
               }
           } else {

               errorMessage += ' ' + (errorData.detail || JSON.stringify(errorData));
           }
        } else if (error.request) {

          errorMessage = '网络错误，服务器无响应。请检查网络或联系管理员。';
        } else {

          errorMessage = '请求设置出错。';
        }

        ElMessage({
          message: errorMessage.trim(),
          type: 'error',
          duration: 5000,
        });

      } finally {
        loading.value = false;
      }
    } else {
      console.log('表单校验失败!');

      return false;
    }
  });
};


const resetForm = () => {
  registrationFormRef.value.resetFields(); // 使用 Element Plus 提供的方法重置表单和校验状态
};

</script>

<style scoped>
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f5f7;
}

.registration-card {
  width: 400px;
  max-width: 90%;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}
</style>