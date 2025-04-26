import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // 你的 Django API 前缀

const touristApiService = {
  async getActivities() {
    try {
      const response = await axios.get(`${API_BASE_URL}/activities/`);
      return response.data;
    } catch (error) {
      console.error('获取 activities 失败:', error);
      return [];
    }
  },

  async getProducts() {
    try {
      const response = await axios.get(`${API_BASE_URL}/products/`);
      return response.data;
    } catch (error) {
      console.error('获取 products 失败:', error);
      return [];
    }
  },

  // 其他游客相关的 API 请求...
};

export default touristApiService;