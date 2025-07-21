// Authentication and authorization guards for Vue Router with JWT
import axios from 'axios'
import jwtAuthService from './jwtAuthService.js'

/**
 * Check if user is authenticated with JWT
 */
export function isAuthenticated() {
  return jwtAuthService.isAuthenticated()
}

/**
 * Get current user data from JWT auth service
 */
export function getCurrentUser() {
  return jwtAuthService.getCurrentUser()
}

/**
 * Check if user has specific role
 */
export function hasRole(requiredRole) {
  return jwtAuthService.hasRole(requiredRole)
}

/**
 * Check if user has specific permission
 */
export async function hasPermission(permission) {
  return jwtAuthService.hasPermission(permission)
}

/**
 * Auth guard for routes requiring login
 */
export function requireAuth(to, from, next) {
  if (isAuthenticated()) {
    // Check if token needs refresh
    jwtAuthService.refreshIfNeeded()
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
  if (user && (user.role === 'CDS_OWNER' || user.is_superuser)) {
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
