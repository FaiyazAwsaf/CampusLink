import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/HomePage.vue'
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
      component: () => import('../views/LandingPage.vue') 
    },

    {
      path: '/home',
      name: 'home',
      component: Home,
      beforeEnter: requireAuth
    },

    {
      path: '/cds',
      name: 'cds',
      component: () => import('../views/CdsPage.vue'),
      beforeEnter: requireAuth
    },

    {
      path: '/cds/admin',
      name: 'cds-admin',
      component: () => import('../views/CdsAdminPage.vue'),
      beforeEnter: requireCDSOwner
    },

    {
      path: '/laundry',
      name: 'laundry',
      component: () => import('../views/LaundryPage.vue'),
      beforeEnter: requireAuth
    },

    {
      path: '/laundry/admin',
      name: 'laundry-admin',
      component: () => import('../views/LaundryAdminPage.vue'),
      beforeEnter: requireLaundryStaff
    },

    {
      path: '/entrepreneur-hub',
      name: 'entrepreneur-hub',
      component: () => import('../views/EntrepreneurHubPage.vue'),
      beforeEnter: requireAuth
    },

    {
      path: '/entrepreneur/dashboard',
      name: 'entrepreneur-dashboard',
      component: () => import('../views/EntrepreneurDashboard.vue'),
      beforeEnter: requireEntrepreneur
    },

    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfilePage.vue'),
      beforeEnter: requireAuth
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue'),
      beforeEnter: requireGuest
    },

    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterPage.vue'),
      beforeEnter: requireGuest
    },

    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../views/UnauthorizedPage.vue')
    },

    {
      path: '/test-guards',
      name: 'test-guards',
      component: () => import('../views/RouteGuardsTest.vue')
    },

    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundPage.vue')
    }
  ],
})

export default router
