import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', 
      name: 'landing', 
      component: () => import('../views/Landing.vue') },

    {
      path: '/home',
      name: 'home',
      component: Home
    },

    {
      path: '/cds',
      name: 'cds',
      component: () => import('../views/Cds.vue'),
    },

    {
      path: '/laundry',
      name: 'laundry',
      component: () => import('../views/Laundry.vue'),
    },

    {
      path: '/entrepreneur-hub',
      name: 'entrepreneur-hub',
      component: () => import('../views/EntrepreneurHub.vue'),
    },

    {
      path: '/product/:id',
      name: 'product-details',
      component: ()=> import('../views/ProductDetails.vue'),
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },

    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
    }
  ],
})

export default router
