<template>
  <div class="product-list-container">
    <div class="product-grid">
      <el-card class="product-card" v-for="product in products" :key="product.id">
        <img :src="product.image" class="product-image" :alt="product.name">
        <div class="product-info">
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <div class="product-price">单价：￥{{ product.price }}</div>
          <el-button type="primary" size="small">咨询</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const products = ref([
  { id: 1, image: 'https://readdy.ai/api/search-image?query=free%20range%20mountain%20chicken%20eggs%2C%2030%20eggs%20package%2C%20natural%20brown%20eggs%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=11&orientation=landscape', name: '鸡蛋', description: '山地散养土鸡蛋 - 30枚装', price: 98.00 },
  { id: 2, image: 'https://readdy.ai/api/search-image?query=handmade%20pickled%20vegetables%20in%20glass%20jar%2C%20traditional%20craftsmanship%2C%20colorful%20vegetables%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=12&orientation=landscape', name: '泡菜', description: '手工腌制泡菜 - 传统工艺', price: 58.00 },
  { id: 3, image: 'https://readdy.ai/api/search-image?query=rural%20honey%20gift%20box%20with%20different%20types%20of%20flower%20honey%2C%20glass%20jars%20with%20honey%2C%20elegant%20packaging%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=14&orientation=landscape', name: '百花蜜', description: '乡村蜂蜜礼盒 - 百花蜜组合', price: 199.00 },
  // ... 更多商品
]);

// 之后替换为从后端获取的商品数据
</script>

<style scoped>
.product-list-container {
  padding: 20px 0;
}

/* 应用 CSS Grid 布局到这个类 */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* 根据商品卡片尺寸调整 minmax */
  gap: 20px; /* 网格项之间的间距 */
}


.product-card {
  /* Element UI 的 el-card 默认有一些样式，可能需要调整 */
  width: 100%; /* 确保卡片填满网格单元格的宽度 */
  box-sizing: border-box; /* 确保内边距和边框计算在宽度内 */
  margin-bottom: 0; /* 因为 gap 会提供间距，这里的 margin-bottom 可以移除 */
}

.product-image {
  width: 100%;
  display: block;
  object-fit: cover;
  height: 180px; /* 调整一个合适的图片高度 */
}

.product-info {
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-info h3 {
  margin-top: 0;
  margin-bottom: 0;
  font-size: 1.1em;
}

.product-price {
  color: #ff6700;
  font-weight: bold;
}

/* 移除或注释掉不再使用的 Element UI 栅格相关的样式 */
/* .el-row { display: flex; } */
/* .el-col { ... } */
</style>