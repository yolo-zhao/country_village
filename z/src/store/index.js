import { createStore } from 'vuex'
import axios from 'axios'
import router from '../router'
import cart from './modules/cart'
import order from './modules/order'
import favorite from './modules/favorite'
import admin from './modules/admin'
import activity from './modules/activity'

const store = createStore({
  state() {
    return {
      user: null,
      token: localStorage.getItem('token') || ''
    }
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    CLEAR_AUTH(state) {
      state.user = null
      state.token = ''
      localStorage.removeItem('token')
    }
  },
  actions: {
    async login({ commit }, { username, password, role }) {
      try {
        const response = await axios.post('/api/login/', {
          username,
          password,
          role
        })
        commit('SET_TOKEN', response.data.token)
        commit('SET_USER', response.data.user)
        
        // 登录成功后跳转到首页
        router.push('/home')
        return response.data
      } catch (error) {
        throw error
      }
    },
    async logout({ commit }) {
      try {
        await axios.post('/api/logout/')
        commit('CLEAR_AUTH')
        router.push('/login')
      } catch (error) {
        throw error
      }
    },
    async getCurrentUser({ commit }) {
      try {
        const response = await axios.get('/api/user/')
        commit('SET_USER', response.data)
        return response.data
      } catch (error) {
        throw error
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user,
    username: state => state.user?.username || '',
    userRole: state => state.user?.role || ''
  },
  modules: {
    cart,
    order,
    favorite,
    admin,
    activity
  }
})

export default store 