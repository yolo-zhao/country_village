<template>
  <div class="activity-list-container">
    <div class="activity-grid">
      <el-card class="activity-card" v-for="activity in activities" :key="activity.id">
        <img :src="activity.image" class="activity-image" :alt="activity.title">
        <div class="activity-info">
          <h3>{{ activity.title }}</h3>
          <p>地点：{{ activity.location }}</p>
          <p>时间：{{ activity.time }}</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activities = ref([
  { id: 1, image: 'https://readdy.ai/api/search-image?query=organic%20vegetable%20farm%20with%20people%20picking%20vegetables%2C%20green%20fields%2C%20sunny%20day%2C%20colorful%20vegetables%2C%20people%20enjoying%20farming%20experience%2C%20high%20quality%20photorealistic&width=400&height=250&seq=4&orientation=landscape', title: '有机蔬菜采摘体验 - 感受自然农耕的魅力', location: '北京市密云区', time: '2025-05-01' },
  { id: 2, image: 'https://readdy.ai/api/search-image?query=traditional%20farming%20culture%20experience%2C%20people%20planting%20rice%20in%20paddy%20fields%2C%20plowing%20with%20traditional%20tools%2C%20beautiful%20countryside%20scenery%2C%20sunny%20day%2C%20high%20quality%20photorealistic&width=400&height=250&seq=5&orientation=landscape', title: '传统农耕文化体验 - 插秧、犁地、收割全流程', location: '河北省张家口市', time: '2025-05-15' },
  { id: 3, image: 'https://readdy.ai/api/search-image?query=rural%20handicraft%20making%20workshop%2C%20people%20making%20pottery%2C%20weaving%20baskets%2C%20and%20tie-dyeing%20fabrics%2C%20colorful%20materials%2C%20indoor%20workshop%20with%20natural%20light%2C%20high%20quality%20photorealistic&width=400&height=250&seq=6&orientation=landscape', title: '乡村手工艺制作 - 陶艺、编织、扎染', location: '北京市怀柔区', time: '2025-05-20' },
  // ... 更多活动
]);

// 之后替换为从后端获取的活动数据
</script>

<style scoped>
.activity-list-container {
  padding: 20px 0;
}

/* 应用 CSS Grid 布局到这个类 */
.activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px; /* 网格项之间的间距 */
}


.activity-card {
  /* Element UI 的 el-card 默认有一些样式，可能需要调整 */
  width: 100%; /* 确保卡片填满网格单元格的宽度 */
  box-sizing: border-box; /* 确保内边距和边框计算在宽度内 */
  margin-bottom: 0; /* 因为 gap 会提供间距，这里的 margin-bottom 可以移除 */
}

.activity-image {
  width: 100%;
  display: block;
  object-fit: cover;
  height: 200px; /* 可以调整一个合适的图片高度，例如 200px 或 250px */
}

.activity-info {
  padding: 15px;
}

.activity-info h3 {
  margin-top: 0;
  margin-bottom: 5px;
  font-size: 1.1em; /* 调整字体大小 */
}

.activity-info p {
  margin-bottom: 5px;
  color: #555;
  font-size: 0.9em; /* 调整字体大小 */
}


</style>