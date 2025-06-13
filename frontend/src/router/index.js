import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
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
    }
  ],
})

export default router
