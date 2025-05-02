<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
  router.push('/');
};

const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <h1 class="error-code">404</h1>
      <h2 class="error-title">页面不存在</h2>
      <p class="error-message">抱歉，您访问的页面不存在或已被移除。</p>
      
      <div class="action-buttons">
        <el-button type="primary" @click="goHome">返回首页</el-button>
        <el-button type="info" @click="goBack">返回上一页</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.not-found-container {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 600px;
  width: 100%;
}

.error-code {
  font-size: 72px;
  color: #409EFF;
  margin: 0 0 20px 0;
}

.error-title {
  font-size: 28px;
  color: #303133;
  margin: 0 0 20px 0;
}

.error-message {
  font-size: 16px;
  color: #606266;
  margin: 0 0 30px 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

@media (max-width: 576px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .not-found-container {
    padding: 30px 20px;
  }
  
  .error-code {
    font-size: 60px;
  }
}
</style> 