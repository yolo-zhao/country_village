/**
 * 前端序列化器 - 用于处理数据转换和格式化
 */

/**
 * 活动序列化器 - 用于创建和更新活动数据
 * @param {Object} data - 原始活动数据
 * @returns {Object} - 格式化后的活动数据，适合API提交
 */
export const serializeActivity = (data) => {
  if (!data) return null;
  
  // 创建一个新对象，避免修改原始数据
  const serialized = { ...data };
  
  // 处理category字段 - 确保它是数字，并添加category_id
  if (serialized.category) {
    const categoryId = Number(serialized.category);
    if (!isNaN(categoryId)) {
      serialized.category = categoryId;
      serialized.category_id = categoryId; // 添加category_id字段
    }
  }
  
  // 确保状态字段存在
  if (!serialized.status) {
    serialized.status = 'published';
  }
  
  // 处理时间字段
  if (serialized.start_time && typeof serialized.start_time === 'string') {
    serialized.start_time = serialized.start_time.endsWith('Z') 
      ? serialized.start_time 
      : serialized.start_time + 'Z';
  }
  
  if (serialized.end_time && typeof serialized.end_time === 'string') {
    serialized.end_time = serialized.end_time.endsWith('Z') 
      ? serialized.end_time 
      : serialized.end_time + 'Z';
  }
  
  return serialized;
};

/**
 * 为FormData添加活动数据
 * @param {FormData} formData - 要填充的FormData对象
 * @param {Object} data - 活动数据
 * @returns {FormData} - 填充后的FormData对象
 */
export const populateActivityFormData = (formData, data) => {
  if (!formData || !data) return formData;
  
  // 处理category字段
  if (data.category) {
    const categoryId = Number(data.category);
    if (!isNaN(categoryId)) {
      formData.append('category', categoryId);
      formData.append('category_id', categoryId); // 添加category_id字段
    }
  }
  
  // 确保状态字段存在
  if (!data.status) {
    formData.append('status', 'published');
  }
  
  // 处理tags数组
  if (data.tags && Array.isArray(data.tags)) {
    data.tags.forEach(tag => {
      formData.append('tags', tag);
    });
  }
  
  // 添加其他字段，排除已处理的特殊字段
  Object.keys(data).forEach(key => {
    if (key !== 'category' && key !== 'tags' && key !== 'cover_image') {
      formData.append(key, data[key]);
    }
  });
  
  return formData;
}; 