/**
 * JWT Token Management Utilities
 * Handles token storage, validation, and automatic refresh
 */

const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
const USER_KEY = 'user'
const API_BASE_URL = 'http://127.0.0.1:8000' // Backend API URL

export class TokenManager {
  /**
   * Store JWT tokens in localStorage
   */
  static setTokens(accessToken, refreshToken) {
    localStorage.setItem(TOKEN_KEY, accessToken)
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  }

  /**
   * Get access token from localStorage
   */
  static getAccessToken() {
    return localStorage.getItem(TOKEN_KEY)
  }

  /**
   * Get refresh token from localStorage
   */
  static getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  }

  /**
   * Remove all tokens and user data from localStorage
   */
  static clearTokens() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  }

  /**
   * Check if user has valid access token
   */
  static hasValidToken() {
    const token = this.getAccessToken()
    if (!token) return false
    
    try {
      const payload = this.parseJWT(token)
      const currentTime = Date.now() / 1000
      return payload.exp > currentTime
    } catch (error) {
      return false
    }
  }

  /**
   * Parse JWT token payload
   */
  static parseJWT(token) {
    try {
      const base64Url = token.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      }).join(''))
      return JSON.parse(jsonPayload)
    } catch (error) {
      throw new Error('Invalid token format')
    }
  }

  /**
   * Get user data from token payload
   */
  static getUserFromToken() {
    const token = this.getAccessToken()
    if (!token) return null
    
    try {
      const payload = this.parseJWT(token)
      return {
        id: payload.user_id,
        email: payload.email,
        name: payload.name,
        role: payload.role,
        is_admin: payload.is_admin,
        is_verified: payload.is_verified
      }
    } catch (error) {
      return null
    }
  }

  /**
   * Store user data in localStorage
   */
  static setUser(userData) {
    localStorage.setItem(USER_KEY, JSON.stringify(userData))
  }

  /**
   * Get user data from localStorage
   */
  static getUser() {
    const userData = localStorage.getItem(USER_KEY)
    return userData ? JSON.parse(userData) : null
  }

  /**
   * Check if token will expire within given minutes
   */
  static willExpireSoon(minutes = 5) {
    const token = this.getAccessToken()
    if (!token) return true
    
    try {
      const payload = this.parseJWT(token)
      const currentTime = Date.now() / 1000
      const expirationTime = payload.exp
      const timeUntilExpiration = expirationTime - currentTime
      const minutesUntilExpiration = timeUntilExpiration / 60
      
      return minutesUntilExpiration <= minutes
    } catch (error) {
      return true
    }
  }
}

export class AuthService {
  /**
   * Login user with email and password
   */
  static async login(email, password, role) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/accounts/jwt/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, role })
      })

      const data = await response.json()

      if (response.ok && data.success) {
        TokenManager.setTokens(data.tokens.access, data.tokens.refresh)
        TokenManager.setUser(data.user)
        return { success: true, user: data.user }
      } else {
        return { success: false, error: data.error || 'Login failed' }
      }
    } catch (error) {
      return { success: false, error: 'Network error' }
    }
  }

  /**
   * Register new user
   */
  static async register(userData) {
    try {
      // Check if we have a file to upload
      const hasFile = userData.image && userData.image instanceof File
      
      let requestData
      let headers = {}
      
      if (hasFile) {
        // Use FormData for file uploads
        const formData = new FormData()
        Object.keys(userData).forEach(key => {
          if (userData[key] !== null && userData[key] !== undefined) {
            formData.append(key, userData[key])
          }
        })
        requestData = formData
        // Don't set Content-Type header, let browser set it with boundary
      } else {
        // Use JSON for text-only data
        requestData = JSON.stringify(userData)
        headers['Content-Type'] = 'application/json'
      }

      const response = await fetch(`${API_BASE_URL}/api/accounts/jwt/register/`, {
        method: 'POST',
        headers: headers,
        body: requestData
      })

      const data = await response.json()

      if (response.ok && data.success) {
        TokenManager.setTokens(data.tokens.access, data.tokens.refresh)
        TokenManager.setUser(data.user)
        return { success: true, user: data.user }
      } else {
        return { success: false, errors: data.errors || { general: data.error } }
      }
    } catch (error) {
      console.error('Registration error:', error)
      return { success: false, errors: { general: `Network error: ${error.message}` } }
    }
  }

  /**
   * Logout user
   */
  static async logout() {
    try {
      const refreshToken = TokenManager.getRefreshToken()
      const accessToken = TokenManager.getAccessToken()

      if (refreshToken && accessToken) {
        await fetch(`${API_BASE_URL}/api/accounts/jwt/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          },
          body: JSON.stringify({ refresh: refreshToken })
        })
      }
    } catch (error) {
      // Ignore errors during logout
    } finally {
      TokenManager.clearTokens()
    }
  }

  /**
   * Refresh access token
   */
  static async refreshToken() {
    try {
      const refreshToken = TokenManager.getRefreshToken()
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }

      const response = await fetch(`${API_BASE_URL}/api/accounts/jwt/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken })
      })

      const data = await response.json()

      if (response.ok && data.success) {
        TokenManager.setTokens(data.tokens.access, data.tokens.refresh)
        if (data.user) {
          TokenManager.setUser(data.user)
        }
        return { success: true }
      } else {
        TokenManager.clearTokens()
        throw new Error('Token refresh failed')
      }
    } catch (error) {
      TokenManager.clearTokens()
      throw error
    }
  }

  /**
   * Get current user info from server
   */
  static async getCurrentUser() {
    try {
      const accessToken = TokenManager.getAccessToken()
      if (!accessToken) {
        throw new Error('No access token')
      }

      const response = await fetch(`${API_BASE_URL}/api/accounts/jwt/current-user/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      })

      const data = await response.json()

      if (response.ok && data.success) {
        TokenManager.setUser(data.user)
        return { success: true, user: data.user }
      } else {
        throw new Error(data.error || 'Failed to get user')
      }
    } catch (error) {
      throw error
    }
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated() {
    return TokenManager.hasValidToken()
  }

  /**
   * Get current user data
   */
  static getCurrentUserData() {
    return TokenManager.getUser() || TokenManager.getUserFromToken()
  }
}
