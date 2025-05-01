import request from '@/utils/request'

// 获取订单详情
export function getOrderDetail(orderId) {
  return request({
    url: `/api/orders/${orderId}`,
    method: 'get'
  })
}

// 支付订单
export function payOrder(data) {
  return request({
    url: `/api/orders/${data.orderId}/pay`,
    method: 'post',
    data: {
      payment_method: data.paymentMethod
    }
  })
}

// 取消订单
export function cancelOrder(orderId) {
  return request({
    url: `/api/orders/${orderId}/cancel`,
    method: 'post'
  })
}

// 确认收货
export function confirmReceipt(orderId) {
  return request({
    url: `/api/orders/${orderId}/confirm`,
    method: 'post'
  })
}

// 获取订单列表
export function getOrders(params) {
  return request({
    url: '/api/orders',
    method: 'get',
    params
  })
}

// 创建订单
export function createOrder(data) {
  return request({
    url: '/api/orders',
    method: 'post',
    data
  })
} 