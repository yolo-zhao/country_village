import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import ActivitiesPage from '../views/ActivitiesPage.vue';
import ProductsPage from '../views/ProductsPage.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/activities',
    name: 'activities',
    component: ActivitiesPage
  },
  {
    path: '/products',
    name: 'products',
    component: ProductsPage
  },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;