import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000/api/';

const touristApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  async getActivities() {
    try {
      const response = await touristApi.get('/activities/'); // 示例路径
      return response.data;
    } catch (error) {
      console.error('Error fetching activities:', error);
      throw error;
    }
  },

  async getProducts() {
    try {
      const response = await touristApi.get('/products/'); // 示例路径
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },

  async registerUser(userData) {
    try {

      const response = await touristApi.post('/register/', userData);
      console.log('Registration successful:', response.data);
      return response;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  },

};