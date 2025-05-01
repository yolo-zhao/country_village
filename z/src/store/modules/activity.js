import axios from 'axios'

export default {
  namespaced: true,
  state: {
    activities: [],
    total: 0
  },
  mutations: {
    SET_ACTIVITIES(state, { activities, total }) {
      state.activities = activities
      state.total = total
    }
  },
  actions: {
    async fetchActivities({ commit }, params) {
      try {
        const response = await axios.get('/api/activities/', { params })
        commit('SET_ACTIVITIES', {
          activities: response.data.results,
          total: response.data.count
        })
      } catch (error) {
        throw error
      }
    },
    async registerActivity({ dispatch }, activityId) {
      try {
        await axios.post(`/api/activities/${activityId}/register/`)
        // 重新获取活动列表以更新数据
        await dispatch('fetchActivities')
      } catch (error) {
        throw error
      }
    }
  },
  getters: {
    activities: state => state.activities,
    total: state => state.total
  }
} 