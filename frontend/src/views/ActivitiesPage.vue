<script setup>
import { ref, onMounted } from 'vue';
import ActivityList from '../components/ActivityList.vue';
import touristApiService from '../services/touristApi';

const activityList = ref([]);

onMounted(async () => {
  console.log('ActivitiesPage mounted, fetching data...');
  try {
    activityList.value = await touristApiService.getActivities();
    console.log('ActivitiesPage fetched activities:', activityList.value);
  } catch (error) {
    console.error('ActivitiesPage Error fetching activities:', error);
  }
});








</script>


<template>
  <div class="activities-page">
    <h1>精彩活动</h1>

    <div class="main-content-wrapper"> <div class="activity-section">
        <ActivityList v-if="activityList.length > 0" :activities="activityList" />
        <p v-else>暂无活动</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activities-page h1 {
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

.activity-section {
    margin-bottom: 40px;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
</style>