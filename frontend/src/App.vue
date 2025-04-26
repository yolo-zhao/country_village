<script setup>
import { ref, onMounted } from 'vue';
import ActivityList from './components/ActivityList.vue';
import ProductList from './components/ProductList.vue';
import touristApiService from './services/touristApi';

const activeIndex = ref('home');
const activityList = ref([]);
const productList = ref([]);

const handleSelect = (index, indexPath) => {
  console.log('选中:', index);
  activeIndex.value = index;
  // 这里可以根据 index 进行页面滚动或者内容切换，如果需要的话
};

onMounted(async () => {
  // 在这里调用 API 获取数据
  try {
    activityList.value = await touristApiService.getActivities();
    productList.value = await touristApiService.getProducts();
  } catch (error) {
    console.error('获取数据失败:', error);
    // 可以根据需要添加错误处理逻辑，例如显示错误消息给用户
  }
});
</script>

<template>
  <el-container>
    <el-header class="header">
      <div class="logo">
        <span>乡村活动平台</span>
      </div>
      <div class="nav-menu">
        <el-menu mode="horizontal" :default-active="activeIndex" @select="handleSelect">
          <el-menu-item index="home">首页</el-menu-item>
          <el-menu-item index="activity">活动</el-menu-item>
          <el-menu-item index="product">商品</el-menu-item>
          <el-menu-item index="about">关于我们</el-menu-item>
        </el-menu>
      </div>
      <div class="nav-right">
        <el-input placeholder="搜索" class="search-input" />
        <el-button type="primary" size="small">登录</el-button>
        <el-button size="small">注册</el-button>
      </div>
    </el-header>
    <el-main class="main">
      <div class="banner">
        <h1>农村活动体验</h1>
        <p>感受乡村慢生活，远离城市喧嚣</p>
      </div>

      <div class="main-content-wrapper">
        <div class="activity-section">
          <h2>精选活动</h2>
          <ActivityList :activities="activityList" />
        </div>
        <div class="product-section">
          <h2>热门商品</h2>
          <ProductList :products="productList" />
        </div>
      </div>

    </el-main>
    <el-footer class="footer">
    </el-footer>
  </el-container>
</template>

<style scoped>
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
  padding: 20px;
}

.banner {
  margin-bottom: 20px;
  padding: 20px;
  text-align: center;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  color: white;
}

.main-content-wrapper {
    max-width: 1200px; /* 最大宽度 */
    margin: 0 auto; /* 居中显示 */
    padding: 0 20px; /* 添加左右内边距 */
    width: 100%;
    box-sizing: border-box;
}


.activity-section {
    margin-bottom: 40px;
}

.product-section {
    margin-bottom: 20px;
}


.footer {
  text-align: center;
  padding: 10px;
  background-color: #f9f9f9;
  border-top: 1px solid #eee;
}
</style>