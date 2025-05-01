<template>
  <el-carousel height="300px" indicator-position="bottom" :autoplay="true">
    <el-carousel-item v-for="item in banners" :key="item.id">
      <div class="banner-item">
        <img :src="item.image" class="banner-image" :alt="item.title">
        <div class="banner-info">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </div>
      </div>
    </el-carousel-item>
    <template #prev>
      <el-button type="primary" class="carousel-arrow">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
    </template>
    <template #next>
      <el-button type="primary" class="carousel-arrow">
        <el-icon><ArrowRight /></el-icon>
      </el-button>
    </template>
  </el-carousel>
</template>

<script setup>
import { ref } from 'vue';
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue';

const banners = ref([
  { id: 1, image: 'https://via.placeholder.com/1200x300/f0f0f0/333?Text=Activity+1', title: '精彩活动一', description: '活动简介一...' },
  { id: 2, image: 'https://via.placeholder.com/1200x300/e0e0e0/444?Text=Activity+2', title: '热门活动二', description: '活动简介二...' },
  { id: 3, image: 'https://via.placeholder.com/1200x300/d0d0d0/555?Text=Activity+3', title: '推荐活动三', description: '活动简介三...' },
]);


</script>

<style scoped>
.banner-item {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.banner-image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-info {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
}

.banner-info h3 {
  margin-top: 0;
  margin-bottom: 5px;
}

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.3);
  border: none;
  color: white;
  z-index: 10;
}

.el-carousel__container:hover .carousel-arrow {
  opacity: 1;
  transition: opacity 0.3s ease;
}

.carousel-arrow:hover {
  background-color: rgba(0, 0, 0, 0.5);
}

.el-carousel__button {
  background-color: rgba(0, 0, 0, 0.5) !important;
}

.el-carousel__indicator--horizontal {
  bottom: 10px !important;
}
</style>