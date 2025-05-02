import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/test-api',
    name: 'TestApi',
    component: () => import('../views/TestApi.vue')
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
    path: '/activities',
    name: 'Activities',
    component: () => import('../views/Activities.vue')
  },
  {
    path: '/activities/:id',
    name: 'ActivityDetail',
    component: () => import('../views/ActivityDetail.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/Products.vue')
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetail.vue')
  },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: () => import('../views/user/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/reservations',
    name: 'UserReservations',
    component: () => import('../views/user/Reservations.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/cart',
    name: 'UserCart',
    component: () => import('../views/user/Cart.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/farmer/dashboard',
    name: 'FarmerDashboard',
    component: () => import('../views/farmer/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'farmer' }
  },
  {
    path: '/farmer/activities/create',
    name: 'CreateActivity',
    component: () => import('../views/farmer/ActivityForm.vue'),
    meta: { requiresAuth: true, role: 'farmer' }
  },
  {
    path: '/farmer/activities/edit/:id',
    name: 'EditActivity',
    component: () => import('../views/farmer/ActivityForm.vue'),
    meta: { requiresAuth: true, role: 'farmer' }
  },
  {
    path: '/farmer/products/create',
    name: 'CreateProduct',
    component: () => import('../views/farmer/ProductForm.vue'),
    meta: { requiresAuth: true, role: 'farmer' }
  },
  {
    path: '/farmer/products/edit/:id',
    name: 'EditProduct',
    component: () => import('../views/farmer/ProductForm.vue'),
    meta: { requiresAuth: true, role: 'farmer' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由导航守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')
  
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    // 需要登录但未登录，重定向到登录页
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (to.matched.some(record => record.meta.role) && 
             to.matched.some(record => record.meta.role !== userRole)) {
    // 需要特定角色但角色不匹配，重定向到首页
    next('/')
  } else {
    // 允许通过
    next()
  }
})

export default router 