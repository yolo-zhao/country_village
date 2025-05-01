import axios from 'axios'

// 初始状态
const state = {
  items: [], // 购物车商品列表
  loading: false, // 加载状态
}

// getters
const getters = {
  totalCount: (state) => {
    return state.items.reduce((total, item) => total + item.quantity, 0)
  },
  totalPrice: (state) => {
    return state.items.reduce((total, item) => {
      return total + item.product.price * item.quantity
    }, 0)
  }
}

// mutations
const mutations = {
  SET_CART_ITEMS(state, items) {
    state.items = items
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  ADD_CART_ITEM(state, item) {
    const existingItem = state.items.find(i => i.product.id === item.product.id)
    if (existingItem) {
      existingItem.quantity += item.quantity
    } else {
      state.items.push(item)
    }
  },
  UPDATE_CART_ITEM_QUANTITY(state, { id, quantity }) {
    const item = state.items.find(i => i.id === id)
    if (item) {
      item.quantity = quantity
    }
  },
  REMOVE_CART_ITEM(state, id) {
    const index = state.items.findIndex(item => item.id === id)
    if (index > -1) {
      state.items.splice(index, 1)
    }
  },
  REMOVE_MULTIPLE_ITEMS(state, ids) {
    state.items = state.items.filter(item => !ids.includes(item.id))
  },
  CLEAR_CART(state) {
    state.items = []
  }
}

// actions
const actions = {
  // 获取购物车列表
  async fetchCart({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get('/api/cart/')
      commit('SET_CART_ITEMS', response.data)
    } catch (error) {
      console.error('Fetch cart error:', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 添加商品到购物车
  async addToCart({ commit }, { product_id, quantity = 1 }) {
    try {
      const response = await axios.post('/api/cart/add/', {
        product_id,
        quantity
      })
      commit('ADD_CART_ITEM', response.data)
      return response.data
    } catch (error) {
      console.error('Add to cart error:', error)
      throw error
    }
  },

  // 更新购物车商品数量
  async updateQuantity({ commit }, { id, quantity }) {
    try {
      await axios.put(`/api/cart/${id}/`, {
        quantity
      })
      commit('UPDATE_CART_ITEM_QUANTITY', { id, quantity })
    } catch (error) {
      console.error('Update quantity error:', error)
      throw error
    }
  },

  // 从购物车中移除商品
  async removeFromCart({ commit }, id) {
    try {
      await axios.delete(`/api/cart/${id}/`)
      commit('REMOVE_CART_ITEM', id)
    } catch (error) {
      console.error('Remove from cart error:', error)
      throw error
    }
  },

  // 批量移除商品
  async removeMultiple({ commit }, ids) {
    try {
      await axios.post('/api/cart/remove_multiple/', { ids })
      commit('REMOVE_MULTIPLE_ITEMS', ids)
    } catch (error) {
      console.error('Remove multiple items error:', error)
      throw error
    }
  },

  // 清空购物车
  async clearCart({ commit }) {
    try {
      await axios.delete('/api/cart/')
      commit('CLEAR_CART')
    } catch (error) {
      console.error('Clear cart error:', error)
      throw error
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
} 