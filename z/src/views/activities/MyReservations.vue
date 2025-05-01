<template>
  <div class="my-reservations">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>我的预约</h3>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="待参加" name="pending">
          <reservation-list :status="'pending'" />
        </el-tab-pane>
        <el-tab-pane label="已完成" name="completed">
          <reservation-list :status="'completed'" />
        </el-tab-pane>
        <el-tab-pane label="已取消" name="cancelled">
          <reservation-list :status="'cancelled'" />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ReservationList from '@/components/activities/ReservationList.vue'

const activeTab = ref('pending')
</script>

<style scoped>
.my-reservations {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 