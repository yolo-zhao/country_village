import http from './http'

export const aiApi = {
  /**
   * 发送消息到AI助手
   * @param {string} message - 用户消息内容
   * @returns {Promise} - 返回AI助手的响应
   */
  sendMessage(message) {
    return http.post('/core/ai-assistant/', { message })
  },
  
  /**
   * 获取AI助手的健康状态
   * @returns {Promise} - 返回AI助手的状态信息
   */
  getStatus() {
    return http.get('/core/ai-assistant/status/')
  }
} 