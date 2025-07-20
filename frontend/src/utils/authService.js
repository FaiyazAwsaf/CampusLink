// JWT and session management utilities
import axios from 'axios'

class AuthService {
  constructor() {
    this.tokenKey = 'access_token'
    this.refreshTokenKey = 'refresh_token'
    this.userKey = 'user'
    
    // Setup axios interceptors
    this.setupInterceptors()
  }

  /**
   * Setup axios request/response interceptors for token management
   */
  setupInterceptors() {
    // Request interceptor to add token to headers
    axios.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor to handle token refresh
    axios.interceptors.response.use(
      (response) => {
        return response
      },
      async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            const refreshToken = this.getRefreshToken()
            if (refreshToken) {
              const response = await this.refreshAccessToken(refreshToken)
              const { access_token } = response.data
              
              this.setAccessToken(access_token)
              originalRequest.headers.Authorization = `Bearer ${access_token}`
              
              return axios(originalRequest)
            }
          } catch (refreshError) {
            this.logout()
            window.location.href = '/login'
          }
        }

        return Promise.reject(error)
      }
    )
  }

  /**
   * Login with email and password
   */
  async login(email, password) {
    try {
      const response = await axios.post('/api/accounts/login/', {
        email,
        password
      })

      if (response.data.success) {
        const { user, access_token, refresh_token } = response.data
        
        // Store tokens and user data
        this.setAccessToken(access_token)
        this.setRefreshToken(refresh_token)
        this.setUser(user)
        
        return { success: true, user }
      }

      return { success: false, error: response.data.error }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      }
    }
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      await axios.post('/api/accounts/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      this.clearAuth()
    }
  }

  /**
   * Refresh access token
   */
  async refreshAccessToken(refreshToken) {
    return await axios.post('/api/accounts/token/refresh/', {
      refresh: refreshToken
    })
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    const token = this.getAccessToken()
    const user = this.getUser()
    return !!(token && user)
  }

  /**
   * Get current user
   */
  getCurrentUser() {
    return this.getUser()
  }

  /**
   * Check if user has specific role
   */
  hasRole(role) {
    const user = this.getUser()
    return user ? user.role === role : false
  }

  /**
   * Check if user has specific permission
   */
  async hasPermission(permission) {
    try {
      const response = await axios.get(`/api/accounts/check-permission/?permission=${permission}`)
      return response.data.has_permission
    } catch (error) {
      console.error('Permission check failed:', error)
      return false
    }
  }

  // Token management methods
  getAccessToken() {
    return localStorage.getItem(this.tokenKey)
  }

  setAccessToken(token) {
    localStorage.setItem(this.tokenKey, token)
  }

  getRefreshToken() {
    return localStorage.getItem(this.refreshTokenKey)
  }

  setRefreshToken(token) {
    localStorage.setItem(this.refreshTokenKey, token)
  }

  getUser() {
    const user = localStorage.getItem(this.userKey)
    return user ? JSON.parse(user) : null
  }

  setUser(user) {
    localStorage.setItem(this.userKey, JSON.stringify(user))
  }

  clearAuth() {
    localStorage.removeItem(this.tokenKey)
    localStorage.removeItem(this.refreshTokenKey)
    localStorage.removeItem(this.userKey)
  }
}

// Create singleton instance
const authService = new AuthService()
export default authService
