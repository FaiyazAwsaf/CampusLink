// Router utilities for JWT-enhanced navigation
import { useRouter, useRoute } from 'vue-router'
import jwtAuthService from './jwtAuthService.js'

/**
 * Check if user can access a specific route
 * @param {string} routeName - Name of the route to check
 * @returns {boolean} - Whether user can access the route
 */
export function canAccessRoute(routeName) {
  const router = useRouter()
  const route = router.resolve({ name: routeName })
  
  if (!route || !route.meta) return false
  
  // Public routes are always accessible
  if (route.meta.public) return true
  
  // Guest-only routes when authenticated
  if (route.meta.guestOnly && jwtAuthService.isAuthenticated()) {
    return false
  }
  
  // Authentication required routes
  if (route.meta.requiresAuth && !jwtAuthService.isAuthenticated()) {
    return false
  }
  
  // Role-based access
  if (route.meta.roles) {
    const user = jwtAuthService.getCurrentUser()
    if (!user) return false
    
    return route.meta.roles.includes(user.role) || user.is_superuser
  }
  
  return true
}

/**
 * Get accessible routes for current user
 * @returns {Array} - Array of route objects accessible to current user
 */
export function getAccessibleRoutes() {
  const router = useRouter()
  const user = jwtAuthService.getCurrentUser()
  
  return router.getRoutes().filter(route => {
    // Skip routes without names or meta
    if (!route.name || !route.meta) return false
    
    // Skip development routes in production
    if (route.meta.development && import.meta.env.PROD) return false
    
    // Public routes
    if (route.meta.public) return true
    
    // Authenticated user routes
    if (route.meta.requiresAuth && jwtAuthService.isAuthenticated()) {
      if (!route.meta.roles) return true
      return route.meta.roles.includes(user?.role) || user?.is_superuser
    }
    
    // Guest routes
    if (route.meta.guestOnly && !jwtAuthService.isAuthenticated()) {
      return true
    }
    
    return false
  })
}

/**
 * Get navigation items for NavBar based on user role
 * @returns {Array} - Array of navigation items
 */
export function getNavigationItems() {
  const user = jwtAuthService.getCurrentUser()
  if (!user) return []
  
  const items = [
    { name: 'Home', path: '/home', icon: '🏠' },
    { name: 'CDS', path: '/cds', icon: '🏪', roles: ['STUDENT', 'CDS_OWNER'] },
    { name: 'Laundry', path: '/laundry', icon: '🧺', roles: ['STUDENT', 'LAUNDRY_STAFF'] },
    { name: 'Entrepreneur Hub', path: '/entrepreneur-hub', icon: '💼', roles: ['STUDENT', 'ENTREPRENEUR'] }
  ]
  
  // Admin items
  const adminItems = [
    { name: 'CDS Admin', path: '/cds/admin', icon: '⚙️', roles: ['CDS_OWNER'], class: 'text-yellow-300' },
    { name: 'Laundry Admin', path: '/laundry/admin', icon: '🔧', roles: ['LAUNDRY_STAFF'], class: 'text-purple-300' },
    { name: 'My Dashboard', path: '/entrepreneur/dashboard', icon: '📊', roles: ['ENTREPRENEUR'], class: 'text-green-300' }
  ]
  
  const allItems = [...items, ...adminItems]
  
  return allItems.filter(item => {
    if (!item.roles) return true
    return item.roles.includes(user.role) || user.is_superuser
  })
}

/**
 * Check if current route requires specific role
 * @returns {boolean} - Whether current route has role restrictions
 */
export function currentRouteHasRoleRestriction() {
  const route = useRoute()
  return !!(route.meta?.roles && route.meta.roles.length > 0)
}

/**
 * Get current user's allowed roles for current route
 * @returns {Array} - Array of allowed roles
 */
export function getCurrentRouteAllowedRoles() {
  const route = useRoute()
  return route.meta?.roles || []
}

/**
 * Navigate with automatic token refresh
 * @param {string|object} to - Route to navigate to
 */
export async function navigateWithTokenCheck(to) {
  const router = useRouter()
  
  try {
    // Refresh token if needed before navigation
    if (jwtAuthService.isAuthenticated()) {
      await jwtAuthService.refreshIfNeeded()
    }
    
    await router.push(to)
  } catch (error) {
    console.error('Navigation failed:', error)
    
    // If token refresh failed, clear auth and redirect to login
    if (jwtAuthService.isAuthenticated()) {
      jwtAuthService.clearAuth()
      router.push('/login')
    }
  }
}

/**
 * Get breadcrumb navigation for current route
 * @returns {Array} - Array of breadcrumb items
 */
export function getBreadcrumbs() {
  const route = useRoute()
  const router = useRouter()
  
  const breadcrumbs = []
  const pathSegments = route.path.split('/').filter(segment => segment !== '')
  
  let currentPath = ''
  for (const segment of pathSegments) {
    currentPath += `/${segment}`
    
    // Find matching route
    const matchedRoute = router.resolve(currentPath)
    if (matchedRoute && matchedRoute.meta?.title) {
      breadcrumbs.push({
        name: matchedRoute.meta.title,
        path: currentPath,
        active: currentPath === route.path
      })
    }
  }
  
  return breadcrumbs
}

/**
 * Check if user session is valid and refresh if needed
 * @returns {Promise<boolean>} - Whether session is valid
 */
export async function validateSession() {
  if (!jwtAuthService.isAuthenticated()) {
    return false
  }
  
  try {
    // Attempt to refresh token if needed
    await jwtAuthService.refreshIfNeeded()
    
    // Verify token is still valid
    const isValid = await jwtAuthService.verifyToken()
    
    if (!isValid) {
      jwtAuthService.clearAuth()
      return false
    }
    
    return true
  } catch (error) {
    console.error('Session validation failed:', error)
    jwtAuthService.clearAuth()
    return false
  }
}

/**
 * Get user role display information
 * @param {string} role - User role
 * @returns {object} - Role display information
 */
export function getRoleInfo(role) {
  const roleInfo = {
    'STUDENT': { 
      label: 'Student', 
      color: 'blue', 
      icon: '🎓',
      description: 'Campus student with access to services' 
    },
    'CDS_OWNER': { 
      label: 'CDS Owner', 
      color: 'yellow', 
      icon: '🏪',
      description: 'Central Departmental Store owner/manager' 
    },
    'LAUNDRY_STAFF': { 
      label: 'Laundry Staff', 
      color: 'purple', 
      icon: '🧺',
      description: 'Laundry service staff member' 
    },
    'ENTREPRENEUR': { 
      label: 'Entrepreneur', 
      color: 'green', 
      icon: '💼',
      description: 'Campus entrepreneur with business dashboard' 
    }
  }
  
  return roleInfo[role] || { 
    label: 'User', 
    color: 'gray', 
    icon: '👤',
    description: 'Campus user' 
  }
}
