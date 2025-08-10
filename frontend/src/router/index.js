import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/HomePage.vue'
import jwtAuthService from '@/utils/jwtAuthService.js'
import { 
  requireAuth, 
  requireGuest, 
  requireCDSOwner, 
  requireEntrepreneur, 
  requireLaundryStaff 
} from '@/utils/authGuards'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { 
      path: '/', 
      name: 'landing', 
      component: () => import('../views/LandingPage.vue'),
      meta: { 
        public: true,
        title: 'Welcome to CampusLink'
      }
    },

    {
      path: '/home',
      name: 'home',
      component: Home,
      beforeEnter: requireAuth,
      meta: { 
        requiresAuth: true,
        roles: ['STUDENT', 'CDS_OWNER', 'LAUNDRY_STAFF', 'ENTREPRENEUR'],
        title: 'Home - CampusLink'
      }
    },

    {
      path: '/cds',
      name: 'cds',
      component: () => import('../views/CdsPage.vue'),
      beforeEnter: requireAuth,
      meta: { 
        requiresAuth: true,
        roles: ['STUDENT', 'CDS_OWNER'],
        title: 'Central Departmental Store'
      }
    },

    {
      path: '/cds/admin',
      name: 'cds-admin',
      component: () => import('../views/CdsAdminPage.vue'),
      beforeEnter: requireCDSOwner,
      meta: { 
        requiresAuth: true,
        roles: ['CDS_OWNER'],
        adminOnly: true,
        title: 'CDS Admin Panel'
      }
    },

    {
      path: '/laundry',
      name: 'laundry',
      component: () => import('../views/LaundryPage.vue'),
      beforeEnter: requireAuth,
      meta: { 
        requiresAuth: true,
        roles: ['STUDENT', 'LAUNDRY_STAFF'],
        title: 'Laundry Service'
      }
    },

    {
      path: '/laundry/admin',
      name: 'laundry-admin',
      component: () => import('../views/LaundryAdminPage.vue'),
      beforeEnter: requireLaundryStaff,
      meta: { 
        requiresAuth: true,
        roles: ['LAUNDRY_STAFF'],
        adminOnly: true,
        title: 'Laundry Admin Panel'
      }
    },

    {
      path: '/entrepreneur-hub',
      name: 'entrepreneur-hub',
      component: () => import('../views/EntrepreneurHubPage.vue'),
      beforeEnter: requireAuth,
      meta: { 
        requiresAuth: true,
        roles: ['STUDENT', 'ENTREPRENEUR'],
        title: 'Entrepreneur Hub'
      }
    },

    {
      path: '/entrepreneur/dashboard',
      name: 'entrepreneur-dashboard',
      component: () => import('../views/EntrepreneurDashboard.vue'),
      beforeEnter: requireEntrepreneur,
      meta: { 
        requiresAuth: true,
        roles: ['ENTREPRENEUR'],
        adminOnly: true,
        title: 'Entrepreneur Dashboard'
      }
    },

    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfilePage.vue'),
      beforeEnter: requireAuth,
      meta: { 
        requiresAuth: true,
        roles: ['STUDENT', 'CDS_OWNER', 'LAUNDRY_STAFF', 'ENTREPRENEUR'],
        title: 'My Profile'
      }
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue'),
      beforeEnter: requireGuest,
      meta: { 
        guestOnly: true,
        title: 'Login - CampusLink'
      }
    },

    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterPage.vue'),
      beforeEnter: requireGuest,
      meta: { 
        guestOnly: true,
        title: 'Register - CampusLink'
      }
    },

    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../views/UnauthorizedPage.vue'),
      meta: { 
        public: true,
        title: 'Access Denied'
      }
    },

    {
      path: '/test-guards',
      name: 'test-guards',
      component: () => import('../views/RouteGuardsTest.vue'),
      meta: { 
        development: true,
        title: 'Route Guards Test'
      }
    },

    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundPage.vue'),
      meta: { 
        public: true,
        title: 'Page Not Found'
      }
    }
  ],
})

// Global navigation guards for JWT token management
router.beforeEach(async (to, from, next) => {
  // Set document title based on route meta
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = 'CampusLink'
  }

  // Skip JWT checks for public routes
  if (to.meta.public) {
    next()
    return
  }

  // Check and refresh JWT token if needed
  if (jwtAuthService.isAuthenticated()) {
    try {
      // Automatically refresh token if expiring soon
      await jwtAuthService.refreshIfNeeded()
      
      // Validate user role for protected routes
      if (to.meta.roles) {
        const user = jwtAuthService.getCurrentUser()
        const hasValidRole = to.meta.roles.includes(user?.role) || user?.is_superuser
        
        if (!hasValidRole) {
          console.warn(`Access denied: User role '${user?.role}' not in allowed roles:`, to.meta.roles)
          next('/unauthorized')
          return
        }
      }
      
      next()
    } catch (error) {
      console.error('Token refresh failed during navigation:', error)
      jwtAuthService.clearAuth()
      next('/login')
    }
  } else {
    // Handle unauthenticated access
    if (to.meta.requiresAuth) {
      next('/login')
    } else {
      next()
    }
  }
})

// Global after navigation hook for analytics/logging
router.afterEach((to, from) => {
  // Log route navigation for authenticated users
  if (jwtAuthService.isAuthenticated()) {
    const user = jwtAuthService.getCurrentUser()
    console.log(`Navigation: ${user?.email} -> ${to.path}`)
  }

  // Track token expiration warnings
  if (jwtAuthService.isAuthenticated() && jwtAuthService.isTokenExpiringSoon()) {
    console.info('JWT token expiring soon, will auto-refresh on next API call')
  }
})

export default router
