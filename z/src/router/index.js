import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true },
    children: [
      // 活动相关路由
      {
        path: 'activities',
        redirect: '/home/activities/list',
        children: [
          {
            path: 'list',
            name: 'ActivityList',
            component: () => import('../views/tourist/Activities.vue')
          },
          {
            path: 'my-reservations',
            name: 'MyReservations',
            component: () => import('../views/activities/MyReservations.vue')
          },
          {
            path: 'my-checkins',
            name: 'MyCheckins',
            component: () => import('../views/activities/MyCheckins.vue')
          }
        ]
      },
      // 产品相关路由
      {
        path: 'products',
        children: [
          {
            path: 'list',
            name: 'ProductList',
            component: () => import('../views/products/ProductList.vue')
          },
          {
            path: 'cart',
            name: 'ShoppingCart',
            component: () => import('../views/products/ShoppingCart.vue')
          }
        ]
      },
      // 农户相关路由
      {
        path: 'farmer',
        meta: { requiresRole: 'farmer' },
        children: [
          {
            path: 'profile',
            name: 'FarmerProfile',
            component: () => import('../views/farmer/Profile.vue')
          },
          {
            path: 'products',
            name: 'FarmerProducts',
            component: () => import('../views/farmer/Products.vue')
          },
          {
            path: 'orders',
            name: 'FarmerOrders',
            component: () => import('../views/farmer/Orders.vue')
          }
        ]
      },
      // 游客相关路由
      {
        path: 'tourist',
        meta: { requiresRole: 'tourist' },
        children: [
          {
            path: 'profile',
            name: 'TouristProfile',
            component: () => import('../views/tourist/Profile.vue')
          },
          {
            path: 'orders',
            name: 'TouristOrders',
            component: () => import('../views/tourist/Orders.vue')
          },
          {
            path: 'favorites',
            name: 'TouristFavorites',
            component: () => import('../views/tourist/Favorites.vue')
          }
        ]
      },
      // 管理员相关路由
      {
        path: 'admin',
        meta: { requiresRole: 'admin' },
        children: [
          {
            path: 'users',
            name: 'UserManagement',
            component: () => import('../views/admin/Users.vue')
          },
          {
            path: 'activities',
            name: 'ActivityManagement',
            component: () => import('../views/admin/Activities.vue')
          },
          {
            path: 'products',
            name: 'ProductManagement',
            component: () => import('../views/admin/Products.vue')
          },
          {
            path: 'categories',
            name: 'CategoryManagement',
            component: () => import('../views/admin/Categories.vue')
          },
          {
            path: 'orders',
            name: 'OrderManagement',
            component: () => import('../views/admin/Orders.vue')
          },
          {
            path: 'comments',
            name: 'CommentManagement',
            component: () => import('../views/admin/Comments.vue')
          }
        ]
      },
      {
        path: '/orders',
        name: 'OrderList',
        component: () => import('@/views/orders/OrderList.vue'),
        meta: {
          title: '我的订单',
          requiresAuth: true
        }
      },
      {
        path: '/orders/:id',
        name: 'OrderDetail',
        component: () => import('@/views/orders/OrderDetail.vue'),
        meta: {
          title: '订单详情',
          requiresAuth: true
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  const userRole = store.getters.userRole

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else if (to.matched.some(record => record.meta.requiresRole)) {
      // 检查角色权限
      const requiredRole = to.matched.find(record => record.meta.requiresRole).meta.requiresRole
      if (userRole !== requiredRole) {
        next('/home/activities/list') // 重定向到公共页面
      } else {
        next()
      }
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 