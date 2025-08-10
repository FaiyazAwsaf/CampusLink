// JWT-based Authentication Service for CampusLink
import axios from 'axios'

/**
 * JWT-based Authentication Service for CampusLink
 * Handles secure token-based authentication with automatic refresh
 */
class JWTAuthService {
  constructor() {
    this.accessTokenKey = 'jwt_access_token'
    this.refreshTokenKey = 'jwt_refresh_token'
    this.userKey = 'jwt_user'
    this.apiBaseUrl = '/api/accounts/auth'
    
    // Setup axios interceptors
    this.setupInterceptors()
  }

  /**
   * Setup axios request/response interceptors for JWT token management
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
              const { access, refresh, user } = response.data
              
              this.setAccessToken(access)
              if (refresh) {
                this.setRefreshToken(refresh)
              }
              if (user) {
                this.setUser(user)
              }
              
              originalRequest.headers.Authorization = `Bearer ${access}`
              return axios(originalRequest)
            }
          } catch (refreshError) {
            this.clearAuth()
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
      const response = await axios.post(`${this.apiBaseUrl}/login/`, {
        email,
        password
      })

      if (response.data.access) {
        const { access, refresh, user } = response.data
        
        // Store tokens and user data
        this.setAccessToken(access)
        this.setRefreshToken(refresh)
        this.setUser(user)
        
        return { success: true, user }
      }

      return { success: false, error: 'Login failed' }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || error.response?.data?.error || 'Login failed' 
      }
    }
  }

  /**
   * Register new user
   */
  async register(userData) {
    try {
      // Prepare form data for file upload if image is present
      let requestData = userData
      let headers = {}

      if (userData.image && userData.image instanceof File) {
        requestData = new FormData()
        Object.keys(userData).forEach(key => {
          requestData.append(key, userData[key])
        })
        headers['Content-Type'] = 'multipart/form-data'
      }

      const response = await axios.post(`${this.apiBaseUrl}/register/`, requestData, {
        headers
      })

      if (response.data.success) {
        const { access, refresh, user } = response.data
        
        // Store tokens and user data
        this.setAccessToken(access)
        this.setRefreshToken(refresh)
        this.setUser(user)
        
        return { success: true, user }
      }

      return { 
        success: false, 
        errors: response.data.errors || { general: 'Registration failed' }
      }
    } catch (error) {
      return { 
        success: false, 
        errors: error.response?.data?.errors || { general: 'Registration failed' }
      }
    }
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      const refreshToken = this.getRefreshToken()
      if (refreshToken) {
        await axios.post(`${this.apiBaseUrl}/logout/`, {
          refresh: refreshToken
        })
      }
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
    return await axios.post(`${this.apiBaseUrl}/refresh/`, {
      refresh: refreshToken
    })
  }

  /**
   * Verify if token is valid
   */
  async verifyToken() {
    try {
      const response = await axios.get(`${this.apiBaseUrl}/verify-token/`)
      return response.data.valid
    } catch (error) {
      console.error('Token verification failed:', error)
      return false
    }
  }

  /**
   * Get current user from server
   */
  async getCurrentUserFromServer() {
    try {
      const response = await axios.get(`${this.apiBaseUrl}/current-user/`)
      if (response.data.success) {
        this.setUser(response.data.user)
        return response.data.user
      }
    } catch (error) {
      console.error('Failed to get current user:', error)
    }
    return null
  }

  /**
   * Update user profile
   */
  async updateProfile(userData) {
    try {
      // Prepare form data for file upload if image is present
      let requestData = userData
      let headers = {}

      if (userData.image && userData.image instanceof File) {
        requestData = new FormData()
        Object.keys(userData).forEach(key => {
          requestData.append(key, userData[key])
        })
        headers['Content-Type'] = 'multipart/form-data'
      }

      const response = await axios.put(`${this.apiBaseUrl}/update-profile/`, requestData, {
        headers
      })
      
      if (response.data.success) {
        this.setUser(response.data.user)
        return { success: true, user: response.data.user }
      }
      return { success: false, errors: response.data.errors }
    } catch (error) {
      return { 
        success: false, 
        errors: error.response?.data?.errors || { general: 'Update failed' }
      }
    }
  }

  /**
   * Change password
   */
  async changePassword(oldPassword, newPassword, confirmPassword) {
    try {
      const response = await axios.post(`${this.apiBaseUrl}/change-password/`, {
        old_password: oldPassword,
        new_password: newPassword,
        confirm_password: confirmPassword
      })
      
      return { 
        success: response.data.success, 
        message: response.data.message 
      }
    } catch (error) {
      return { 
        success: false, 
        errors: error.response?.data?.errors || { general: 'Password change failed' }
      }
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    const token = this.getAccessToken()
    const user = this.getUser()
    
    if (!token || !user) return false
    
    // Check if token is expired
    if (this.isTokenExpired()) {
      this.clearAuth()
      return false
    }
    
    return true
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
  hasPermission(permission) {
    const user = this.getUser()
    return user && user.permissions ? user.permissions.includes(permission) : false
  }

  // Token management methods
  getAccessToken() {
    return localStorage.getItem(this.accessTokenKey)
  }

  setAccessToken(token) {
    localStorage.setItem(this.accessTokenKey, token)
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
    localStorage.removeItem(this.accessTokenKey)
    localStorage.removeItem(this.refreshTokenKey)
    localStorage.removeItem(this.userKey)
  }

  /**
   * Get token expiration time
   */
  getTokenExpiration() {
    const token = this.getAccessToken()
    if (!token) return null
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return new Date(payload.exp * 1000)
    } catch (error) {
      console.error('Error parsing token:', error)
      return null
    }
  }

  /**
   * Check if token is expired
   */
  isTokenExpired() {
    const expiration = this.getTokenExpiration()
    if (!expiration) return true
    
    return new Date() >= expiration
  }

  /**
   * Check if token will expire soon (within 5 minutes)
   */
  isTokenExpiringSoon() {
    const expiration = this.getTokenExpiration()
    if (!expiration) return true
    
    const fiveMinutesFromNow = new Date(Date.now() + 5 * 60 * 1000)
    return expiration <= fiveMinutesFromNow
  }

  /**
   * Automatically refresh token if it's expiring soon
   */
  async refreshIfNeeded() {
    if (this.isTokenExpiringSoon() && this.getRefreshToken()) {
      try {
        const response = await this.refreshAccessToken(this.getRefreshToken())
        const { access, refresh, user } = response.data
        
        this.setAccessToken(access)
        if (refresh) {
          this.setRefreshToken(refresh)
        }
        if (user) {
          this.setUser(user)
        }
        
        return true
      } catch (error) {
        console.error('Auto-refresh failed:', error)
        this.clearAuth()
        return false
      }
    }
    return true
  }
}

// Export singleton instance
const jwtAuthService = new JWTAuthService()
export default jwtAuthService
