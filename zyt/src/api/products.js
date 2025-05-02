import http from './http'

export const productApi = {
  // 获取产品列表
  getProducts(params = {}) {
    return http.get('/products/', { params })
  },
  
  // 获取产品详情
  getProductDetail(id) {
    return http.get(`/products/${id}/`)
  },
  
  // 发送产品咨询
  sendInquiry(productId, data) {
    return http.post(`/products/${productId}/inquiries/`, data)
  },
  
  // 获取购物车
  getCart() {
    // 尝试使用/cart/路径，如果失败则使用/carts/路径
    return http.get('/cart/').catch(error => {
      console.log('使用/cart/路径失败，尝试/carts/路径');
      return http.get('/carts/');
    });
  },
  
  // 添加商品到购物车
  addToCart(productId, quantity = 1) {
    // 尝试使用/cart/add_item/路径，如果失败则使用/carts/路径
    return http.post('/cart/add_item/', { 
      product_id: productId, 
      quantity 
    }).catch(error => {
      console.log('使用/cart/add_item/路径失败，尝试使用/carts/路径');
      // 使用先前的逻辑
      return http.get('/carts/').then(response => {
        // 判断用户是否已有购物车
        if (response.data && response.data.length > 0) {
          // 使用第一个购物车
          const cartId = response.data[0].id;
          // 添加商品到购物车
          return http.post(`/carts/${cartId}/add_item/`, { product_id: productId, quantity });
        } else {
          // 如果没有购物车，先创建一个
          return http.post('/carts/', {}).then(cartResponse => {
            const cartId = cartResponse.data.id;
            // 然后添加商品
            return http.post(`/carts/${cartId}/add_item/`, { product_id: productId, quantity });
          });
        }
      });
    });
  },
  
  // 更新购物车商品数量
  updateCartItem(itemId, quantity) {
    return http.put(`/cart-items/${itemId}/`, { quantity })
  },
  
  // 从购物车移除商品
  removeFromCart(itemId) {
    return http.delete(`/cart-items/${itemId}/`)
  },
  
  // 清空购物车 - 先获取购物车，然后删除所有项目
  clearCart() {
    return http.get('/carts/').then(response => {
      if (response.data && response.data.length > 0) {
        const cartId = response.data[0].id;
        const promises = response.data[0].items.map(item => 
          http.delete(`/cart-items/${item.id}/`)
        );
        return Promise.all(promises);
      }
      return Promise.resolve();
    });
  },
  
  // 获取农场主发布的产品
  getFarmerProducts() {
    return http.get('/farmer-products/')
  },
  
  // 创建新产品
  createProduct(data) {
    return http.post('/products/', data)
  },
  
  // 更新产品
  updateProduct(productId, data) {
    return http.put(`/products/${productId}/`, data)
  },
  
  // 删除产品
  deleteProduct(productId) {
    return http.delete(`/products/${productId}/`)
  },
  
  // 上传产品图片
  uploadProductImage(productId, formData) {
    return http.post(`/products/${productId}/images/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // 删除产品图片
  deleteProductImage(imageId) {
    return http.delete(`/images/${imageId}/`)
  },
  
  // 更新产品库存
  updateProductStock(productId, stock) {
    return http.put(`/products/${productId}/stock/`, { stock })
  },
  
  // 创建订单
  createOrder(data) {
    return http.post('/orders/', data)
  },
  
  // 获取订单列表
  getOrders() {
    return http.get('/my-orders/')
  },
  
  // 获取订单详情
  getOrderDetail(orderId) {
    return http.get(`/orders/${orderId}/`)
  },
  
  // 取消订单
  cancelOrder(orderId) {
    return http.post(`/orders/${orderId}/cancel/`)
  },
  
  // 支付订单
  payOrder(orderId, paymentMethod) {
    return http.post(`/orders/${orderId}/pay/`, { payment_method: paymentMethod })
  }
} 