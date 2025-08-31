import { createRouter, createWebHistory } from 'vue-router'
import { AuthService } from '../utils/auth.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { 
      path: '/', 
      name: 'landing', 
      component: () => import('../views/LandingPage.vue') 
    },

    {
      path: '/cds',
      name: 'cds',
      component: () => import('../views/CdsPage.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/laundry',
      name: 'laundry',
      component: () => import('../views/LaundryPage.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/entrepreneur-hub',
      name: 'entrepreneur-hub',
      component: () => import('../views/EntrepreneurHubPage.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/entrepreneur-hub/product/:id',
      name: 'product-details',
      component: () => import('../views/ProductDetails.vue'),
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue'),
      meta: { requiresGuest: true }
    },

    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterPage.vue'),
      meta: { requiresGuest: true }
    },

    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfilePage.vue'),
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/CartPage.vue'),
    },
      {
        path: '/entrepreneur/dashboard',
        name: 'EntrepreneurDashboard',
        component: () => import('../views/EntrepreneurDashboard.vue'),
        meta: { requiresAuth: true, role: 'entrepreneur' }
      },
  ],
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = AuthService.isAuthenticated()
  
  // Routes that require authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({
      name: 'login',
      query: { next: to.fullPath }
    })
    return
  }
  
  // Routes that require guest (not authenticated)
  if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'landing' })
    return
  }
  
  next()
})

export default router
