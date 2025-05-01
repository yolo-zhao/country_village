<script setup>
import { ref, onMounted } from 'vue';
import ProductList from '../components/ProductList.vue';
import ActivityList from '../components/ActivityList.vue';
import touristApiService from '../services/touristApi';
const productList = ref([]);

onMounted(async () => {
  console.log('HomePage mounted, fetching data...');
  try {
    productList.value = await touristApiService.getProducts();
     console.log('HomePage fetched products:', productList.value);
  } catch (error) {
    console.error('HomePage Error fetching products:', error);
  }
});
const featuredActivities = ref([ // 使用 ref() 包装数组，尽管是静态数据，以保持响应性结构的统一
  {
    id: 1, // 建议给活动数据加上 ID
    title: '有机蔬菜采摘体验，感受自然农耕的魅力',
    location: '北京密云区',
    date: '2025-05-01',
    image: '/path/to/your/image1.jpg' // <-- 请将这里和下面的图片路径替换为你的实际图片地址
    // 添加其他属性，如 description, price 等
  },
  {
    // id: 2,
    title: '传统农耕文化体验 - 插秧、割稻全流程',
    location: '河北保定市',
    date: '2025-05-15',
    image: '/path/to/your/image2.jpg'
  },
  {
    id: 3,
    title: '乡村手工制作 - 陶艺、编织、扎染',
    location: '河南郑州',
    date: '2025-05-20',
    image: '/path/to/your/image3.jpg'
  }
]);

</script>

<template>
  <div class="home-page">
    <div class="banner">
      <h1>农村活动体验</h1>
      <p>感受乡村慢生活，远离城市喧嚣</p>
    </div>

    <div class="main-content-wrapper">
      <div class="activity-section">
        <h2>精选活动</h2> <ActivityList :activities="featuredActivities.value" />
      </div>

      <div class="product-section">
        <h2>热门商品</h2>
        <ProductList v-if="productList.length > 0" :products="productList" />
        <p v-else>暂无商品</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
/* 将 Banner 和商品列表相关的样式从 App.vue 移动到这里 */
.banner {
  margin-bottom: 20px;
  padding: 40px 20px;
  text-align: center;
  background-image: url('/background.jpg'); /* 确保图片路径正确 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  color: white;
  border-radius: 8px;
  overflow: hidden;
}

.banner h1 {
    font-size: 3em;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.banner p {
    font-size: 1.5em;
     text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.main-content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
}

.product-section {
    margin-bottom: 20px; /* 或者更大，取决于布局 */
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.product-section h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}
</style>