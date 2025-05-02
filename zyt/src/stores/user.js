import { defineStore } from 'pinia'
import http from '../api/http'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    userRole: localStorage.getItem('userRole') || null
  }),
  
  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    isLoggedIn: (state) => state.isAuthenticated,
    isFarmer: (state) => state.userRole === 'farmer',
    isTourist: (state) => state.userRole === 'tourist'
  },
  
  actions: {
    async login(credentials) {
      try {
        const response = await http.post('/login/', credentials)
        const { token, user, role } = response.data
        
        this.token = token
        this.user = user
        this.isAuthenticated = true
        this.userRole = role
        
        localStorage.setItem('token', token)
        localStorage.setItem('userRole', role)
        
        return true
      } catch (error) {
        console.error('登录失败:', error)
        return false
      }
    },
    
    async register(userData) {
      try {
        const response = await http.post('/register/', userData)
        return { success: true, data: response.data }
      } catch (error) {
        console.error('注册失败:', error)
        return { success: false, error: error.response?.data || '注册失败' }
      }
    },
    
    async fetchUserProfile() {
      if (!this.token) return null
      
      try {
        const response = await http.get('/me/', {
          headers: { Authorization: `Token ${this.token}` }
        })
        this.user = response.data
        return response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return null
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      this.userRole = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
    }
  }
}) 