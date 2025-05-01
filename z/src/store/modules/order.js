import { getOrderDetail, payOrder, cancelOrder, confirmReceipt, getOrders, createOrder } from '@/api/order'

// 初始状态
const state = {
  orders: [], // 订单列表
  currentOrder: null, // 当前查看的订单
  loading: false, // 加载状态
  total: 0, // 订单总数
  currentPage: 1, // 当前页码
  pageSize: 10 // 每页数量
}

// getters
const getters = {
  // 按状态分类的订单数量
  orderCountByStatus: (state) => {
    const counts = {
      pending: 0, // 待支付
      paid: 0,    // 已支付
      shipped: 0, // 已发货
      completed: 0, // 已完成
      cancelled: 0  // 已取消
    }
    state.orders.forEach(order => {
      counts[order.status]++
    })
    return counts
  }
}

// mutations
const mutations = {
  SET_ORDERS(state, { orders, total }) {
    state.orders = orders
    state.total = total
  },
  SET_CURRENT_ORDER(state, order) {
    state.currentOrder = order
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_PAGE(state, page) {
    state.currentPage = page
  },
  SET_PAGE_SIZE(state, pageSize) {
    state.pageSize = pageSize
  },
  UPDATE_ORDER_STATUS(state, { orderId, status }) {
    const order = state.orders.find(o => o.id === orderId)
    if (order) {
      order.status = status
    }
    if (state.currentOrder && state.currentOrder.id === orderId) {
      state.currentOrder.status = status
    }
  }
}

// actions
const actions = {
  // 获取订单列表
  async fetchOrders({ commit, state }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const { page = state.currentPage, pageSize = state.pageSize, status } = params
      const response = await getOrders({ page, pageSize, status })
      commit('SET_ORDERS', {
        orders: response.data.orders,
        total: response.data.total
      })
      commit('SET_PAGE', page)
      commit('SET_PAGE_SIZE', pageSize)
    } catch (error) {
      console.error('获取订单列表失败:', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取订单详情
  async fetchOrderDetail({ commit }, orderId) {
    commit('SET_LOADING', true)
    try {
      const response = await getOrderDetail(orderId)
      commit('SET_CURRENT_ORDER', response.data)
    } catch (error) {
      console.error('获取订单详情失败:', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 创建订单
  async createOrder({ commit }, orderData) {
    commit('SET_LOADING', true)
    try {
      const response = await createOrder(orderData)
      return response.data
    } catch (error) {
      console.error('创建订单失败:', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 支付订单
  async payOrder({ commit }, { orderId, paymentMethod }) {
    commit('SET_LOADING', true)
    try {
      await payOrder({ orderId, paymentMethod })
      commit('UPDATE_ORDER_STATUS', { orderId, status: 'paid' })
    } catch (error) {
      console.error('支付订单失败:', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 取消订单
  async cancelOrder({ commit }, orderId) {
    commit('SET_LOADING', true)
    try {
      await cancelOrder(orderId)
      commit('UPDATE_ORDER_STATUS', { orderId, status: 'cancelled' })
    } catch (error) {
      console.error('取消订单失败:', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 确认收货
  async confirmReceipt({ commit }, orderId) {
    commit('SET_LOADING', true)
    try {
      await confirmReceipt(orderId)
      commit('UPDATE_ORDER_STATUS', { orderId, status: 'completed' })
    } catch (error) {
      console.error('确认收货失败:', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
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