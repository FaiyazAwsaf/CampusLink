import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/HomePage.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', 
      name: 'landing', 
      component: () => import('../views/LandingPage.vue') },

    {
      path: '/home',
      name: 'home',
      component: Home
    },

    {
      path: '/cds',
      name: 'cds',
      component: () => import('../views/CdsPage.vue'),
    },

    {
      path: '/laundry',
      name: 'laundry',
      component: () => import('../views/LaundryPage.vue'),
    },

    {
      path: '/entrepreneur-hub',
      name: 'entrepreneur-hub',
      component: () => import('../views/EntrepreneurHubPage.vue'),
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue'),
    },

    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterPage.vue'),
    }
  ],
})

export default router
