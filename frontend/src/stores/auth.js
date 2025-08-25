import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { AuthService, TokenManager } from '../utils/auth.js'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => {
    return !!user.value && AuthService.isAuthenticated()
  })

  const isCDSOwner = computed(() => {
    return user.value?.role === 'cds_owner' || false
  })

  const isLaundryStaff = computed(() => {
    return user.value?.role === 'laundry_staff' || false
  })

  const isAdmin = computed(() => {
    return user.value?.is_admin || false
  })

  const userRole = computed(() => {
    return user.value?.role || 'guest'
  })

  const userPermissions = computed(() => {
    return user.value?.permissions || []
  })

  // Actions
  const login = async (email, password) => {
    isLoading.value = true
    error.value = null

    try {
      const result = await AuthService.login(email, password)
      
      if (result.success) {
        user.value = result.user
        return { success: true }
      } else {
        error.value = result.error
        return { success: false, error: result.error }
      }
    } catch (err) {
      error.value = 'Login failed'
      return { success: false, error: 'Login failed' }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    isLoading.value = true
    error.value = null

    try {
      const result = await AuthService.register(userData)
      
      if (result.success) {
        user.value = result.user
        return { success: true }
      } else {
        return { success: false, errors: result.errors }
      }
    } catch (err) {
      error.value = 'Registration failed'
      return { success: false, errors: { general: 'Registration failed' } }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true
    
    try {
      await AuthService.logout()
    } catch (err) {
      // Ignore logout errors
    } finally {
      user.value = null
      error.value = null
      isLoading.value = false
    }
  }

  const refreshUser = async () => {
    try {
      const result = await AuthService.getCurrentUser()
      if (result.success) {
        user.value = result.user
      }
    } catch (err) {
      // If refresh fails, user is likely not authenticated
      user.value = null
    }
  }

  const updateProfile = async (profileData) => {
    isLoading.value = true
    error.value = null

    try {
      const formData = new FormData()
      Object.keys(profileData).forEach(key => {
        if (profileData[key] !== null && profileData[key] !== undefined) {
          formData.append(key, profileData[key])
        }
      })

      const token = TokenManager.getAccessToken()
      const response = await fetch('http://127.0.0.1:8000/api/accounts/jwt/update-profile/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })

      const data = await response.json()

      if (response.ok && data.success) {
        user.value = { ...user.value, ...data.user }
        TokenManager.setUser(user.value)
        return { success: true }
      } else {
        error.value = data.error || 'Profile update failed'
        return { success: false, errors: data.errors }
      }
    } catch (err) {
      error.value = 'Profile update failed'
      return { success: false, error: 'Profile update failed' }
    } finally {
      isLoading.value = false
    }
  }

  const checkPermission = (permission) => {
    return userPermissions.value.includes(permission)
  }

  const hasAnyPermission = (permissions) => {
    return permissions.some(permission => userPermissions.value.includes(permission))
  }

  const initializeAuth = () => {
    // Check if user is already authenticated
    if (AuthService.isAuthenticated()) {
      const userData = AuthService.getCurrentUserData()
      if (userData) {
        user.value = userData
      } else {
        // Try to get user data from server
        refreshUser()
      }
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    user,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    isCDSOwner,
    isLaundryStaff,
    isAdmin,
    userRole,
    userPermissions,
    
    // Actions
    login,
    register,
    logout,
    refreshUser,
    updateProfile,
    checkPermission,
    hasAnyPermission,
    initializeAuth,
    clearError
  }
})
