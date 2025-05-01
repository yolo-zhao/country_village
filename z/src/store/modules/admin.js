import axios from 'axios'

const state = {
  users: [],
  products: [],
  categories: [],
  comments: [],
  activities: [],
  total: 0
}

const mutations = {
  SET_USERS(state, users) {
    state.users = users
  },
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  SET_CATEGORIES(state, categories) {
    state.categories = categories
  },
  SET_COMMENTS(state, comments) {
    state.comments = comments
  },
  SET_ACTIVITIES(state, activities) {
    state.activities = activities
  },
  SET_TOTAL(state, total) {
    state.total = total
  }
}

const actions = {
  // 用户管理
  async fetchUsers({ commit }, params) {
    try {
      const response = await axios.get('/api/admin/users/', { params })
      commit('SET_USERS', response.data.items)
      commit('SET_TOTAL', response.data.total)
    } catch (error) {
      throw error
    }
  },

  async createUser({ commit }, userData) {
    try {
      const response = await axios.post('/api/admin/users/', userData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updateUser({ commit }, { id, userData }) {
    try {
      const response = await axios.put(`/api/admin/users/${id}/`, userData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async deleteUser({ commit }, id) {
    try {
      await axios.delete(`/api/admin/users/${id}/`)
    } catch (error) {
      throw error
    }
  },

  // 产品管理
  async fetchProducts({ commit }, params) {
    try {
      const response = await axios.get('/api/admin/products/', { params })
      commit('SET_PRODUCTS', response.data.items)
      commit('SET_TOTAL', response.data.total)
    } catch (error) {
      throw error
    }
  },

  async createProduct({ commit }, productData) {
    try {
      const response = await axios.post('/api/admin/products/', productData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updateProduct({ commit }, { id, productData }) {
    try {
      const response = await axios.put(`/api/admin/products/${id}/`, productData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async deleteProduct({ commit }, id) {
    try {
      await axios.delete(`/api/admin/products/${id}/`)
    } catch (error) {
      throw error
    }
  },

  // 分类管理
  async fetchCategories({ commit }, params) {
    try {
      const response = await axios.get('/api/admin/categories/', { params })
      commit('SET_CATEGORIES', response.data.items)
      commit('SET_TOTAL', response.data.total)
    } catch (error) {
      throw error
    }
  },

  async createCategory({ commit }, categoryData) {
    try {
      const response = await axios.post('/api/admin/categories/', categoryData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updateCategory({ commit }, { id, categoryData }) {
    try {
      const response = await axios.put(`/api/admin/categories/${id}/`, categoryData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async deleteCategory({ commit }, id) {
    try {
      await axios.delete(`/api/admin/categories/${id}/`)
    } catch (error) {
      throw error
    }
  },

  // 评论管理
  async fetchComments({ commit }, params) {
    try {
      const response = await axios.get('/api/admin/comments/', { params })
      commit('SET_COMMENTS', response.data.items)
      commit('SET_TOTAL', response.data.total)
    } catch (error) {
      throw error
    }
  },

  async approveComment({ commit }, id) {
    try {
      await axios.post(`/api/admin/comments/${id}/approve/`)
    } catch (error) {
      throw error
    }
  },

  async rejectComment({ commit }, id) {
    try {
      await axios.post(`/api/admin/comments/${id}/reject/`)
    } catch (error) {
      throw error
    }
  },

  async deleteComment({ commit }, id) {
    try {
      await axios.delete(`/api/admin/comments/${id}/`)
    } catch (error) {
      throw error
    }
  },

  // 活动管理
  async fetchActivities({ commit }, params) {
    try {
      const response = await axios.get('/api/admin/activities/', { params })
      commit('SET_ACTIVITIES', response.data.items)
      commit('SET_TOTAL', response.data.total)
    } catch (error) {
      throw error
    }
  },

  async createActivity({ commit }, activityData) {
    try {
      const response = await axios.post('/api/admin/activities/', activityData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updateActivity({ commit }, { id, activityData }) {
    try {
      const response = await axios.put(`/api/admin/activities/${id}/`, activityData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async deleteActivity({ commit }, id) {
    try {
      await axios.delete(`/api/admin/activities/${id}/`)
    } catch (error) {
      throw error
    }
  }
}

const getters = {
  users: state => state.users,
  products: state => state.products,
  categories: state => state.categories,
  comments: state => state.comments,
  activities: state => state.activities,
  total: state => state.total
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 