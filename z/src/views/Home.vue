<template>
  <div class="home-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="200px">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          router
        >
          <!-- 所有角色都可以看到的菜单项 -->
          <el-sub-menu index="/home/activities">
            <template #title>
              <el-icon><Calendar /></el-icon>
              <span>乡村活动</span>
            </template>
            <el-menu-item index="/home/activities/list">活动列表</el-menu-item>
            <el-menu-item index="/home/activities/my-reservations">我的预约</el-menu-item>
            <el-menu-item index="/home/activities/my-checkins">我的打卡</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/home/products">
            <template #title>
              <el-icon><ShoppingBag /></el-icon>
              <span>农特产品</span>
            </template>
            <el-menu-item index="/home/products/list">产品列表</el-menu-item>
            <el-menu-item index="/home/products/cart">购物车</el-menu-item>
          </el-sub-menu>

          <!-- 农户特有的菜单项 -->
          <template v-if="userRole === 'farmer'">
            <el-sub-menu index="/home/farmer">
              <template #title>
                <el-icon><Shop /></el-icon>
                <span>农户管理</span>
              </template>
              <el-menu-item index="/home/farmer/profile">农户信息</el-menu-item>
              <el-menu-item index="/home/farmer/products">我的产品</el-menu-item>
              <el-menu-item index="/home/farmer/orders">订单管理</el-menu-item>
            </el-sub-menu>
          </template>

          <!-- 游客特有的菜单项 -->
          <template v-if="userRole === 'tourist'">
            <el-sub-menu index="/home/tourist">
              <template #title>
                <el-icon><User /></el-icon>
                <span>游客中心</span>
              </template>
              <el-menu-item index="/home/tourist/profile">个人信息</el-menu-item>
              <el-menu-item index="/home/tourist/orders">我的订单</el-menu-item>
              <el-menu-item index="/home/tourist/favorites">我的收藏</el-menu-item>
            </el-sub-menu>
          </template>

          <!-- 管理员特有的菜单项 -->
          <template v-if="userRole === 'admin'">
            <el-sub-menu index="/home/admin">
              <template #title>
                <el-icon><Setting /></el-icon>
                <span>系统管理</span>
              </template>
              <el-menu-item index="/home/admin/users">用户管理</el-menu-item>
              <el-menu-item index="/home/admin/activities">活动管理</el-menu-item>
              <el-menu-item index="/home/admin/products">产品管理</el-menu-item>
              <el-menu-item index="/home/admin/categories">分类管理</el-menu-item>
              <el-menu-item index="/home/admin/orders">订单管理</el-menu-item>
              <el-menu-item index="/home/admin/comments">评论管理</el-menu-item>
            </el-sub-menu>
          </template>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container>
        <el-header>
          <div class="header-content">
            <div class="header-left">
              <h2>乡村振兴平台</h2>
            </div>
            <div class="header-right">
              <el-dropdown>
                <span class="user-info">
                  <el-avatar :size="32" icon="UserFilled" />
                  {{ username }}
                  <el-icon><CaretBottom /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="goToProfile">个人信息</el-dropdown-item>
                    <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        
        <el-main>
          <router-view></router-view>
        </el-main>

        <el-footer>
          <div class="footer-content">
            © 2024 乡村振兴平台 版权所有
          </div>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessageBox } from 'element-plus'
import {
  Calendar,
  ShoppingBag,
  Shop,
  User,
  Setting,
  CaretBottom,
  UserFilled
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const store = useStore()

const activeMenu = computed(() => route.path)
const userRole = computed(() => store.getters.userRole)
const username = computed(() => store.getters.username)

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    store.dispatch('logout')
    router.push('/login')
  }).catch(() => {})
}

const goToProfile = () => {
  switch (userRole.value) {
    case 'tourist':
      router.push('/home/tourist/profile')
      break
    case 'farmer':
      router.push('/home/farmer/profile')
      break
    case 'admin':
      router.push('/home/admin/profile')
      break
  }
}
</script>

<style scoped>
.home-container {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #545c64;
  color: #fff;
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
}

.header-content {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 0 12px;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}

.el-footer {
  background-color: #fff;
  border-top: 1px solid #e6e6e6;
}

.footer-content {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #909399;
}
</style> 