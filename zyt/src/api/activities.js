import http from './http'

export const activityApi = {
  // 获取活动列表
  getActivities(params = {}) {
    return http.get('/activities/', { params })
  },
  
  // 获取活动详情
  getActivityDetail(id) {
    return http.get(`/activities/${id}/`)
  },
  
  // 报名参加活动 - 修改为使用API约定
  reserveActivity(activityId, data) {
    // 准备预约数据，确保包含活动ID
    const reservationData = {
      activity: activityId, // 添加活动ID
      contact_name: data.contact_name,
      contact_phone: data.contact_phone,
      reservation_date: data.reservation_date
    };
    
    console.log('发送预约请求数据:', { url: '/reservations/', data: reservationData });
    
    // 向预约API端点发送请求
    return http.post('/reservations/', reservationData);
  },
  
  // 提交活动评价
  reviewActivity(activityId, data) {
    return http.post(`/activity-reviews/`, {
      activity: activityId,
      ...data
    })
  },
  
  // 获取用户的活动预约
  getUserReservations() {
    return http.get('/reservations/')
  },
  
  // 取消预约
  cancelReservation(reservationId) {
    return http.delete(`/reservations/${reservationId}/`)
  },
  
  // 获取活动分类
  getCategories() {
    return http.get('/activity-categories/')
  },
  
  // 获取标签列表
  getTags() {
    return http.get('/tags/')
  },
  
  // 上传活动照片
  uploadActivityPhoto(activityId, formData) {
    formData.append('activity', activityId);
    return http.post(`/activity-photos/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // 活动签到
  checkInActivity(activityId) {
    return http.post(`/activity-check-ins/`, {
      activity: activityId
    })
  },
  
  // 点赞活动
  likeActivity(activityId) {
    return http.post(`/activity-likes/`, {
      content_type: 'activities.activity',
      object_id: activityId
    })
  },
  
  // 取消点赞
  unlikeActivity(activityId) {
    // 实际需要找到对应的like id
    return http.delete(`/activity-likes/`, {
      data: {
        content_type: 'activities.activity',
        object_id: activityId
      }
    })
  },
  
  // 评论活动
  commentActivity(activityId, data) {
    return http.post(`/activity-comments/`, {
      content_type: 'activities.activity',
      object_id: activityId,
      ...data
    })
  },
  
  // 获取农场主发布的活动
  getFarmerActivities() {
    return http.get('/activities/', {
      params: { farmer: 'me' }
    })
  },
  
  // 创建新活动
  createActivity(data) {
    return http.post('/activities/', data)
  },
  
  // 更新活动
  updateActivity(activityId, data) {
    return http.put(`/activities/${activityId}/`, data)
  },
  
  // 删除活动
  deleteActivity(activityId) {
    return http.delete(`/activities/${activityId}/`)
  },
  
  // 获取活动报名列表
  getActivityReservations(activityId) {
    return http.get(`/reservations/`, {
      params: { activity: activityId }
    })
  },
  
  // 确认活动报名
  confirmReservation(reservationId) {
    return http.patch(`/reservations/${reservationId}/`, {
      status: 'confirmed'
    })
  },
  
  // 获取活动统计数据
  getActivityStats(activityId) {
    return http.get(`/activities/${activityId}/stats/`)
  },
  
  // 获取活动打卡记录
  getActivityCheckIns(activityId) {
    return http.get(`/activity-check-ins/`, {
      params: { activity: activityId }
    })
  },
  
  // 创建活动打卡记录
  createActivityCheckIn(data) {
    return http.post('/activity-check-ins/', data)
  }
} 