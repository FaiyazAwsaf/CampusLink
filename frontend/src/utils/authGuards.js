// Authentication and authorization guards for Vue Router
import axios from 'axios'

/**
 * Check if user is authenticated
 */
export function isAuthenticated() {
  const user = localStorage.getItem('user')
  return user !== null
}

/**
 * Get current user data
 */
export function getCurrentUser() {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

/**
 * Check if user has specific role
 */
export function hasRole(requiredRole) {
  const user = getCurrentUser()
  return user ? user.role === requiredRole : false
}

/**
 * Check if user has specific permission
 */
export async function hasPermission(permission) {
  try {
    const response = await axios.get(`/api/accounts/check-permission/?permission=${permission}`)
    return response.data.has_permission
  } catch (error) {
    console.error('Permission check failed:', error)
    return false
  }
}

/**
 * Auth guard for routes requiring login
 */
export function requireAuth(to, from, next) {
  if (isAuthenticated()) {
    next()
  } else {
    next('/login')
  }
}

/**
 * Auth guard for routes requiring specific role
 */
export function requireRole(requiredRole) {
  return function(to, from, next) {
    if (!isAuthenticated()) {
      next('/login')
      return
    }
    
    if (hasRole(requiredRole)) {
      next()
    } else {
      next('/unauthorized')
    }
  }
}

/**
 * Auth guard for guest-only routes (login/register)
 */
export function requireGuest(to, from, next) {
  if (isAuthenticated()) {
    next('/home')
  } else {
    next()
  }
}

/**
 * Admin/CDS Owner guard
 */
export function requireCDSOwner(to, from, next) {
  if (!isAuthenticated()) {
    next('/login')
    return
  }
  
  const user = getCurrentUser()
  if (user.role === 'CDS_OWNER' || user.is_superuser) {
    next()
  } else {
    next('/unauthorized')
  }
}

/**
 * Entrepreneur guard
 */
export function requireEntrepreneur(to, from, next) {
  if (!isAuthenticated()) {
    next('/login')
    return
  }
  
  if (hasRole('ENTREPRENEUR')) {
    next()
  } else {
    next('/unauthorized')
  }
}

/**
 * Laundry staff guard
 */
export function requireLaundryStaff(to, from, next) {
  if (!isAuthenticated()) {
    next('/login')
    return
  }
  
  if (hasRole('LAUNDRY_STAFF')) {
    next()
  } else {
    next('/unauthorized')
  }
}
