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
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/department-store',
      name: 'department-store',
      component: () => import('../views/DepartmentStore.vue'),
    },
  ],
})

export default router
