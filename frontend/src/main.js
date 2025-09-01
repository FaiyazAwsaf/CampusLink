import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import { TokenManager, AuthService } from './utils/auth.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// Axios global config for JWT authentication
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Request interceptor to add JWT token
axios.interceptors.request.use(
  (config) => {
    const token = TokenManager.getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for token refresh and error handling
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh token
        await AuthService.refreshToken()
        
        // Retry original request with new token
        const newToken = TokenManager.getAccessToken()
        if (newToken) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return axios(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        TokenManager.clearTokens()
        
        // Only redirect if not already on login page
        const currentPath = window.location.pathname
        if (!currentPath.startsWith('/login') && !currentPath.startsWith('/register')) {
          router.push({ 
            name: 'login', 
            query: { next: currentPath } 
          })
        }
      }
    }

    return Promise.reject(error)
  }
)

// Auto-refresh token if it will expire soon
setInterval(async () => {
  if (TokenManager.willExpireSoon(5) && TokenManager.getRefreshToken()) {
    try {
      await AuthService.refreshToken()
    } catch (error) {
      // Token refresh failed, will be handled by interceptor
    }
  }
}, 60000) // Check every minute
