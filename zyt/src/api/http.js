import axios from 'axios'
import { ElMessage } from 'element-plus'

// 根据错误情况，尝试不同的API基础路径
const API_URL = 'http://localhost:8000/api'

const http = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  // 允许带凭证的跨域请求
  withCredentials: false
})

// 请求拦截器，添加token
http.interceptors.request.use(
  (config) => {
    console.log('发送请求:', config.url, config.params || config.data)
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器，处理错误
http.interceptors.response.use(
  (response) => {
    console.log('收到响应:', response.config.url, response.data)
    return response
  },
  (error) => {
    // 获取更详细的错误信息
    let errorData = '无错误详情';
    try {
      if (error.response && error.response.data) {
        if (typeof error.response.data === 'object') {
          errorData = JSON.stringify(error.response.data, null, 2);
        } else if (typeof error.response.data === 'string') {
          // 尝试从HTML响应中提取错误信息
          if (error.response.data.includes('<!DOCTYPE html>')) {
            const match = error.response.data.match(/<pre class="exception_value">(.*?)<\/pre>/);
            if (match && match[1]) {
              errorData = `HTML错误: ${match[1]}`;
            } else {
              errorData = '服务器返回了HTML错误页面';
            }
          } else {
            errorData = error.response.data;
          }
        }
      }
    } catch (parseError) {
      errorData = `解析错误数据失败: ${parseError.message}`;
    }
    
    // 详细的错误信息
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        '服务器错误';
    
    const url = error.config?.url || '未知URL';
    const status = error.response?.status || '未知状态码';
    const method = error.config?.method?.toUpperCase() || 'GET';
    
    console.error(`请求错误 [${method} ${status}] ${url}: ${errorMessage}`);
    console.error('请求详情:', {
      url: error.config?.url,
      method: error.config?.method,
      headers: error.config?.headers,
      data: error.config?.data,
      params: error.config?.params
    });
    console.error('错误详细信息:', errorData);
    
    // 针对特定错误码的处理
    if (error.response) {
      switch(error.response.status) {
        case 401: // 未授权
          // 清除token，重定向到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('userRole')
          // 避免循环重定向
          if (!window.location.pathname.includes('/login')) {
            ElMessage.error('登录已过期，请重新登录')
            window.location.href = '/login'
          }
          break;
        case 403: // 禁止访问
          ElMessage.error('您没有权限执行此操作')
          break;
        case 404: // 资源不存在
          ElMessage.error('请求的资源不存在')
          break;
        case 500: // 服务器错误
          ElMessage.error(`服务器错误，请稍后再试 (${errorData.substring(0, 100)}...)`)
          break;
        default:
          // 其他错误
          ElMessage.error(errorMessage)
      }
    } else {
      // 网络错误
      ElMessage.error('网络错误，请检查您的连接')
    }
    
    return Promise.reject(error)
  }
)

export default http 