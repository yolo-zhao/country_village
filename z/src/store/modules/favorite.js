import axios from 'axios'

const state = {
  favorites: [],
  total: 0
}

const mutations = {
  SET_FAVORITES(state, favorites) {
    state.favorites = favorites
  },
  SET_TOTAL(state, total) {
    state.total = total
  },
  ADD_FAVORITE(state, favorite) {
    state.favorites.push(favorite)
  },
  REMOVE_FAVORITE(state, id) {
    const index = state.favorites.findIndex(item => item.id === id)
    if (index !== -1) {
      state.favorites.splice(index, 1)
    }
  }
}

const actions = {
  // 获取收藏列表
  async fetchFavorites({ commit }, params) {
    try {
      const response = await axios.get('/api/favorites/', { params })
      commit('SET_FAVORITES', response.data.items)
      commit('SET_TOTAL', response.data.total)
    } catch (error) {
      throw error
    }
  },

  // 添加收藏
  async addFavorite({ commit }, productId) {
    try {
      const response = await axios.post('/api/favorites/', { product_id: productId })
      commit('ADD_FAVORITE', response.data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // 删除收藏
  async removeFavorite({ commit }, id) {
    try {
      await axios.delete(`/api/favorites/${id}/`)
      commit('REMOVE_FAVORITE', id)
    } catch (error) {
      throw error
    }
  }
}

const getters = {
  favorites: state => state.favorites,
  total: state => state.total
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 