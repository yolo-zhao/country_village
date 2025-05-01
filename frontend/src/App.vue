<script setup>
import { ref, onMounted, reactive } from 'vue'; // 确保导入了 reactive 和 ref
// 假设 touristApiService 和相关 Element Plus 组件已导入
// import touristApiService from './services/touristApi';
import { ElMessage } from 'element-plus';
import {
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElSelect,
  ElOption,
  ElContainer,
  ElHeader,
  ElMain,
  ElFooter,
  ElMenu, // 导航菜单
  ElMenuItem, // 导航菜单项
  // ElInput as ElInputAlias, // 避免与 ElInputAlias 冲突，如果不需要别名可以移除
  ElDropdown, // 导入下拉菜单组件
  ElDropdownMenu, // 导入下拉菜单容器组件
  ElDropdownItem, // 导入下拉菜单项组件
} from 'element-plus';

// 导入 Element Plus Icons Vue
import { User, Tickets, Star, Setting, ArrowDown } from '@element-plus/icons-vue'; // 导入需要的图标

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

// === 新增：用户登录状态和登录弹窗相关状态 ===
const isLoggedIn = ref(false); // 默认为未登录

const loginDialogVisible = ref(false); // 控制登录弹窗显示状态
const loginFormData = reactive({ // 登录表单数据
    username: '',
    password: ''
});
// ==============================================


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
      // try {
        // 调用 API 服务进行注册 (确保 touristApiService 中有 registerUser 方法)
        // const response = await touristApiService.registerUser(registrationFormData);
        // console.log('注册成功响应:', response.data);
        ElMessage({
          message: '注册成功!', // 模拟成功
          type: 'success',
        });
        registrationDialogVisible.value = false; // 关闭弹窗
        // 可以在此处添加自动登录或跳转到登录页面的逻辑
      // } catch (error) {
      //   console.error('注册失败:', error);
        // 根据后端返回的错误信息进行提示
      //   const errorMessage = error.response?.data?.message // 检查后端是否有 'message' 字段
      //                      || error.response?.data?.detail // 检查后端是否有 'detail' 字段 (DRF 常用)
      //                      || error.response?.data?.username?.[0] // 检查特定字段错误，如用户名重复
      //                      || error.message // axios 或网络错误消息
      //                      || '注册失败，请稍后再试。'; // 备用提示
      //   ElMessage({
      //     message: errorMessage,
      //     type: 'error',
      //   });
      // }
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

// === 新增：处理个人中心下拉菜单项点击 ===
const handleUserCommand = (command) => {
    console.log('执行个人中心命令:', command);
    // 根据 command 执行不同的操作
    switch (command) {
        case 'viewReservations':
            ElMessage({ message: '查看我的预约', type: 'info' });
            // 实际应用中：跳转到我的预约页面或打开弹窗
            break;
        case 'viewEvaluations':
             ElMessage({ message: '查看我的评价', type: 'info' });
            // 实际应用中：跳转到我的评价页面或打开弹窗
            break;
        case 'manageProfile':
             ElMessage({ message: '管理个人信息', type: 'info' });
            // 实际应用中：跳转到个人信息管理页面或打开弹窗
            break;
         case 'logout': // 登出操作
             ElMessage({ message: '已登出', type: 'info' });
             isLoggedIn.value = false; // 设置登录状态为未登录
             loginFormData.username = ''; // 清空登录信息
             loginFormData.password = '';
            break;
        default:
            break;
    }
};
// ======================================

// === 新增：登录弹窗显示和提交处理函数 ===
// 显示登录弹窗并重置表单
const showLoginDialog = () => {
    // 重置登录表单数据
    Object.assign(loginFormData, {
        username: '',
        password: ''
    });
    loginDialogVisible.value = true; // 显示登录弹窗
};

// 提交登录表单 (模拟)
const submitLogin = () => {
    // 在实际应用中，这里需要调用后端 API 进行用户认证
    // 这里的逻辑只是模拟，不进行实际的用户名密码验证
    if (!loginFormData.username || !loginFormData.password) {
        ElMessage({
            message: '请输入用户名和密码',
            type: 'warning',
        });
        return;
    }

    console.log('登录:', loginFormData);

    // 模拟登录成功
    ElMessage({
        message: '登录成功！',
        type: 'success',
    });

    isLoggedIn.value = true; // 设置登录状态为已登录
    loginDialogVisible.value = false; // 关闭登录弹窗

    // 可以在这里清空密码字段，保留用户名（可选）
    loginFormData.password = '';
};
// ======================================


// onMounted(async () => {
//   try {
//     activityList.value = await touristApiService.getActivities();
//     productList.value = await touristApiService.getProducts();
//   } catch (error) {
//     console.error('获取数据失败:', error);
//   }
// });

// 假设你之前有 activityList 和 productList 的定义和获取逻辑
// 如果没有，请根据你的实际情况添加或修改
const activityList = ref([]);
const productList = ref([]);


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
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/activities">活动</el-menu-item>
          <el-menu-item index="/products">商品</el-menu-item>
           </el-menu>
      </div>
      <div class="nav-right">
        <el-input placeholder="搜索" class="search-input" />

        <div v-if="!isLoggedIn" class="auth-buttons">
            <el-button type="primary" size="small" @click="showLoginDialog">登录</el-button>
            <el-button size="small" @click="showRegistrationDialog">注册</el-button>
        </div>

        <div v-else class="user-center-dropdown">
             <el-dropdown @command="handleUserCommand">
                <span class="el-dropdown-link">
                    <el-button type="primary" size="small">
                         <el-icon class="el-icon--left"><User /></el-icon>
                         个人中心
                         <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                    </el-button>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item command="viewReservations">
                             <el-icon><Tickets /></el-icon>查看我的预约
                        </el-dropdown-item>
                        <el-dropdown-item command="viewEvaluations">
                             <el-icon><Star /></el-icon>查看我的评价
                        </el-dropdown-item>
                        <el-dropdown-item command="manageProfile">
                             <el-icon><Setting /></el-icon>管理个人信息
                        </el-dropdown-item>
                         <el-dropdown-item command="logout" divided>
                             登出
                         </el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>

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

    <el-dialog v-model="loginDialogVisible" title="用户登录" width="30%" :before-close="() => loginDialogVisible = false">
        <el-form :model="loginFormData" label-width="80px">
            <el-form-item label="用户名">
                <el-input v-model="loginFormData.username"></el-input>
            </el-form-item>
            <el-form-item label="密码">
                <el-input type="password" v-model="loginFormData.password" show-password></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="loginDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitLogin">登录</el-button>
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
  height: 60px; /* 明确设置头部高度 */
}

.logo {
    font-size: 20px;
    font-weight: bold;
    margin-right: 40px;
    color: #4CAF50;
}

.logo a {
    text-decoration: none; /* 移除 router-link 的下划线 */
    color: inherit; /* 继承父元素的颜色 */
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
  /* 添加一些右侧的间距 */
  padding-right: 10px;
}

.search-input {
  width: 200px;
  margin-right: 10px;
}

/* 新增：登录/注册按钮组和个人中心下拉菜单的样式 */
.auth-buttons .el-button {
    margin-left: 10px;
}

.user-center-dropdown .el-dropdown-link {
    cursor: pointer; /* 鼠标悬停时显示手型 */
    /* 根据需要调整样式，比如颜色 */
}


.main {
  padding: 20px 0;
  /* 为了让 footer 始终在底部，main 需要 flex-grow */
  flex-grow: 1;
}
.footer {
  text-align: center;
  padding: 20px; /* 增加内边距 */
  background-color: #f0f0f0; /* 浅灰色背景 */
  border-top: 1px solid #ddd;
  color: #555;
  font-size: 0.9em;
}

/* 覆盖 Element Plus Dialog Footer 的 flex 布局 */
.el-dialog__footer {
    display: flex;
    justify-content: flex-end; /* 按钮靠右 */
    padding: 10px 20px 20px;
    border-top: 1px solid #eee;
}

.dialog-footer .el-button {
    margin-left: 10px; /* 确保弹窗按钮间距 */
}


</style>