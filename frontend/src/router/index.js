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
      meta: { excludeRoles: ['entrepreneur'] }
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
      meta: { excludeRoles: ['entrepreneur'] }
    },

    {
      path: '/entrepreneur-hub/product/:id',
      name: 'product-details',
      component: () => import('../views/ProductDetails.vue'),
      meta: { excludeRoles: ['entrepreneur'] }
    },

    {
      path: '/entrepreneur-hub/store/:storeId',
      name: 'storefront-profile',
      component: () => import('../views/StorefrontProfile.vue'),
      meta: { excludeRoles: ['entrepreneur'] }
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
      meta: { requiresAuth: true }
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
  const user = AuthService.getCurrentUserData()
  const userRole = user?.role
  
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
    // If user is entrepreneur, redirect to their dashboard
    if (userRole === 'entrepreneur') {
      next({ name: 'EntrepreneurDashboard' })
    } else {
      next({ name: 'landing' })
    }
    return
  }
  
  // Role-based access control
  if (isAuthenticated && userRole) {
    // Check if route excludes certain roles
    if (to.meta.excludeRoles && to.meta.excludeRoles.includes(userRole)) {
      if (userRole === 'entrepreneur') {
        next({ name: 'EntrepreneurDashboard' })
      } else {
        next({ name: 'landing' })
      }
      return
    }
    
    // Entrepreneur restrictions
    if (userRole === 'entrepreneur') {
      // Entrepreneurs can only access their dashboard, profile, and landing page
      const allowedRoutes = ['landing', 'EntrepreneurDashboard', 'profile']
      
      if (!allowedRoutes.includes(to.name)) {
        next({ name: 'EntrepreneurDashboard' })
        return
      }
    }
    
    // Role-specific route requirements
    if (to.meta.role && to.meta.role !== userRole) {
      // User doesn't have required role for this route
      if (userRole === 'entrepreneur') {
        next({ name: 'EntrepreneurDashboard' })
      } else {
        next({ name: 'landing' })
      }
      return
    }
  }
  
  next()
})

export default router
