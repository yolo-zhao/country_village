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
  { id: 1, image: 'https://readdy.ai/api/search-image?query=organic%20fresh%20vegetable%20gift%20box%20with%20seasonal%20vegetables%2C%20beautifully%20arranged%20in%20wooden%20box%2C%20vibrant%20colors%2C%20clean%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=10&orientation=landscape', name: '蔬菜礼盒', description: '有机新鲜蔬菜礼盒 - 当季时令蔬菜直送', price: 168.00 },
  { id: 1, image: 'https://readdy.ai/api/search-image?query=premium%20organic%20strawberry%20gift%20box%20with%20fresh%20red%20strawberries%20arranged%20neatly%2C%20elegant%20packaging%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=10&orientation=squarish', name: '有机草莓礼盒', description: '精选优质草莓，无农药，口感甜美多汁', price: 68.00 },
  { id: 1, image: 'https://readdy.ai/api/search-image?query=artisanal%20honey%20gift%20set%20with%20glass%20jars%20of%20different%20honey%20varieties%2C%20wooden%20packaging%2C%20honeycomb%20decoration%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=11&orientation=squarish', name: '手工蜂蜜礼盒', description: '纯天然野生蜂蜜，无添加，滋养健康', price: 128.00 },
  { id: 1, image: 'https://readdy.ai/api/search-image?query=traditional%20Chinese%20homemade%20sausages%20hanging%20to%20dry%2C%20artisanal%20food%20product%2C%20rustic%20presentation%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=12&orientation=squarish', name: '农家自制腊肠', description: '传统工艺制作，肉质鲜美，风味独特', price: 98.00 },
  { id: 1, image: 'https://readdy.ai/api/search-image?query=handcrafted%20bamboo%20basket%20with%20intricate%20weaving%20pattern%2C%20traditional%20Chinese%20craftsmanship%2C%20elegant%20design%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=13&orientation=squarish', name: '手工编织竹篮', description: '传统手工艺品，实用美观，环保耐用', price: 56.00 },
  { id: 1, image: 'https://readdy.ai/api/search-image?query=handmade%20soap%20gift%20set%20with%20various%20natural%20soaps%2C%20herbal%20ingredients%20visible%2C%20elegant%20packaging%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=14&orientation=squarish', name: '乡村手工皂礼盒', description: '天然植物精油制作，温和不刺激', price: 88.00 },
  { id: 1, image: 'https://readdy.ai/api/search-image?query=free%20range%20mountain%20chicken%20eggs%2C%2030%20eggs%20package%2C%20natural%20brown%20eggs%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=11&orientation=landscape', name: '鸡蛋', description: '山地散养土鸡蛋 - 30枚装', price: 68.00 },

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

</style>