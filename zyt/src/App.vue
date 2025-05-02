<script setup>
import { RouterView } from 'vue-router'
import { ref, computed, onMounted, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'

const userStore = useUserStore()
const router = useRouter()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const isFarmer = computed(() => userStore.isFarmer)

// 导航栏是否折叠（移动端）
const isCollapse = ref(true)

// 退出登录
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

// 错误处理
const hasError = ref(false)
const errorMessage = ref('')

// 全局错误捕获
onErrorCaptured((err) => {
  console.error('应用捕获到错误:', err)
  hasError.value = true
  errorMessage.value = err.message || '应用发生未知错误'
  return false // 阻止错误继续传播
})

// 初始化
onMounted(() => {
  if (userStore.isLoggedIn) {
    userStore.fetchUserProfile()
  }
})
</script>

<template>
  <div class="app-container">
    <!-- 错误提示 -->
    <el-alert
      v-if="hasError"
      type="error"
      :title="errorMessage"
      :closable="true"
      show-icon
      @close="hasError = false"
      style="position: fixed; top: 0; left: 0; right: 0; z-index: 9999;"
    />
    
    <!-- 导航栏 -->
    <el-menu
      :default-active="$route.path"
      class="el-menu-demo"
      mode="horizontal"
      :ellipsis="false"
      router
    >
      <el-menu-item index="/">
        <el-icon><HomeFilled /></el-icon>
        乡村旅游平台
      </el-menu-item>
      
      <div class="flex-grow" />
      
      <el-menu-item index="/activities">
        <el-icon><Calendar /></el-icon>
        乡村活动
      </el-menu-item>
      
      <el-menu-item index="/products">
        <el-icon><ShoppingBag /></el-icon>
        农产品
      </el-menu-item>
      
      <template v-if="!isLoggedIn">
        <el-menu-item index="/login">
          <el-icon><User /></el-icon>
          登录
        </el-menu-item>
        <el-menu-item index="/register">
          <el-icon><EditPen /></el-icon>
          注册
        </el-menu-item>
      </template>
      
      <!-- 农户专属菜单 -->
      <template v-else-if="isFarmer">
        <el-sub-menu index="farmer">
          <template #title>
            <el-icon><Avatar /></el-icon>
            农户中心
          </template>
          
          <el-menu-item index="/user/profile">
            <el-icon><User /></el-icon>
            农户资料
          </el-menu-item>
          
          <el-menu-item index="/farmer/dashboard">
            <el-icon><Setting /></el-icon>
            农户管理平台
          </el-menu-item>
          
          <el-menu-item @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-menu-item>
        </el-sub-menu>
      </template>
      
      <!-- 游客专属菜单 -->
      <template v-else>
        <el-sub-menu index="tourist">
          <template #title>
            <el-icon><Avatar /></el-icon>
            游客中心
          </template>
          
          <el-menu-item index="/user/profile">
            <el-icon><User /></el-icon>
            游客资料
          </el-menu-item>
          
          <el-menu-item index="/user/reservations">
            <el-icon><Calendar /></el-icon>
            我的预约
          </el-menu-item>
          
          <el-menu-item index="/user/cart">
            <el-icon><ShoppingCart /></el-icon>
            购物车
          </el-menu-item>
          
          <el-menu-item @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-menu-item>
        </el-sub-menu>
      </template>
    </el-menu>

    <!-- 主内容区 -->
    <main class="main-content">
      <RouterView />
    </main>

    <!-- 页脚 -->
    <footer class="app-footer">
      <div class="footer-content">
        <p>&copy; {{ new Date().getFullYear() }} 乡村旅游平台 - 连接城市与乡村的桥梁</p>
        <div class="footer-links">
          <a href="#">关于我们</a>
          <a href="#">联系方式</a>
          <a href="#">服务条款</a>
          <a href="#">隐私政策</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.flex-grow {
  flex-grow: 1;
}

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background-color: #f5f5f5;
  padding: 20px;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.footer-links {
  margin-top: 10px;
}

.footer-links a {
  margin: 0 10px;
  color: #666;
  text-decoration: none;
}

.footer-links a:hover {
  color: #409EFF;
}
</style>
