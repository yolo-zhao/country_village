<script setup>
import { ref, onMounted } from 'vue';
import touristApiService from '../services/touristApi';
import ProductList from '../components/ProductList.vue';

const productList = ref([]);

onMounted(async () => {
  console.log('ProductsPage mounted, fetching products...');
  try {
    productList.value = await touristApiService.getProducts(); // 调用 API 获取数据
    console.log('ProductsPage fetched products:', productList.value);
  } catch (error) {
    console.error('ProductsPage Error fetching products:', error);
    // 处理错误显示
  }
});
</script>

<template>
  <div class="products-page">
    <h1>所有商品</h1> <div class="main-content-wrapper"> <div class="product-section"> <ProductList v-if="productList.length > 0" :products="productList" />
        <p v-else>暂无商品</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.products-page h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}


.main-content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    width: 100%;
    box-sizing: border-box;
}

</style>