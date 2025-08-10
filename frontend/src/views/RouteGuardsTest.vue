<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">🔒 Route Guards Test Console</h1>
      
      <!-- Current User Status -->
      <div class="bg-white shadow rounded-lg p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Current User Status</h2>
        <div v-if="currentUser" class="text-sm">
          <p><strong>Name:</strong> {{ currentUser.name }}</p>
          <p><strong>Email:</strong> {{ currentUser.email }}</p>
          <p><strong>Role:</strong> {{ currentUser.role }}</p>
          <p><strong>Authenticated:</strong> {{ isAuthenticated() ? '✅ Yes' : '❌ No' }}</p>
        </div>
        <div v-else class="text-sm text-gray-500">
          No user logged in
        </div>
      </div>

      <!-- Test User Buttons -->
      <div class="bg-white shadow rounded-lg p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Test User Login</h2>
        <div class="flex flex-wrap gap-2">
          <button @click="clearAuth" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
            Clear Auth
          </button>
          <button @click="loginAs('STUDENT')" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Login as Student
          </button>
          <button @click="loginAs('ENTREPRENEUR')" class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
            Login as Entrepreneur
          </button>
          <button @click="loginAs('CDS_OWNER')" class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600">
            Login as CDS Owner
          </button>
          <button @click="loginAs('LAUNDRY_STAFF')" class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600">
            Login as Laundry Staff
          </button>
        </div>
      </div>

      <!-- Route Testing -->
      <div class="bg-white shadow rounded-lg p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Route Navigation Tests</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="route in testRoutes" :key="route.path" class="border rounded-lg p-4">
            <h3 class="font-medium text-gray-900 mb-2">{{ route.name }}</h3>
            <p class="text-sm text-gray-500 mb-3">{{ route.description }}</p>
            <div class="flex flex-col space-y-2">
              <button 
                @click="testRouteAccess(route)"
                class="px-3 py-1 bg-indigo-500 text-white text-sm rounded hover:bg-indigo-600"
              >
                Test Access
              </button>
              <button 
                @click="navigateToRoute(route.path)"
                class="px-3 py-1 bg-gray-500 text-white text-sm rounded hover:bg-gray-600"
              >
                Navigate
              </button>
            </div>
            <div v-if="route.lastTest" class="mt-2 text-xs" :class="getResultClass(route.lastTest.result)">
              {{ route.lastTest.message }}
            </div>
          </div>
        </div>
      </div>

      <!-- Test Results -->
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Test Results</h2>
        <div class="space-y-2 max-h-96 overflow-y-auto">
          <div 
            v-for="(result, index) in testResults" 
            :key="index"
            class="p-3 rounded text-sm"
            :class="getResultClass(result.type)"
          >
            <span class="text-xs text-gray-500">[{{ result.time }}]</span>
            {{ result.message }}
          </div>
        </div>
        <button 
          @click="clearResults"
          class="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Clear Results
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import jwtAuthService from '@/utils/jwtAuthService.js'
import { 
  isAuthenticated, 
  getCurrentUser, 
  hasRole,
  requireAuth,
  requireGuest,
  requireCDSOwner,
  requireEntrepreneur,
  requireLaundryStaff
} from '@/utils/authGuards'

const router = useRouter()
const currentUser = ref(null)
const testResults = ref([])

const testRoutes = ref([
  { 
    path: '/', 
    name: 'Landing Page', 
    description: 'Public landing page',
    expectedAuth: 'none',
    lastTest: null
  },
  { 
    path: '/home', 
    name: 'Home', 
    description: 'Requires authentication',
    expectedAuth: 'any',
    lastTest: null
  },
  { 
    path: '/cds', 
    name: 'CDS Store', 
    description: 'Requires authentication',
    expectedAuth: 'any',
    lastTest: null
  },
  { 
    path: '/cds/admin', 
    name: 'CDS Admin', 
    description: 'Requires CDS_OWNER role',
    expectedAuth: 'CDS_OWNER',
    lastTest: null
  },
  { 
    path: '/laundry', 
    name: 'Laundry Service', 
    description: 'Requires authentication',
    expectedAuth: 'any',
    lastTest: null
  },
  { 
    path: '/laundry/admin', 
    name: 'Laundry Admin', 
    description: 'Requires LAUNDRY_STAFF role',
    expectedAuth: 'LAUNDRY_STAFF',
    lastTest: null
  },
  { 
    path: '/entrepreneur-hub', 
    name: 'Entrepreneur Hub', 
    description: 'Requires authentication',
    expectedAuth: 'any',
    lastTest: null
  },
  { 
    path: '/entrepreneur/dashboard', 
    name: 'Entrepreneur Dashboard', 
    description: 'Requires ENTREPRENEUR role',
    expectedAuth: 'ENTREPRENEUR',
    lastTest: null
  },
  { 
    path: '/profile', 
    name: 'Profile Page', 
    description: 'Requires authentication',
    expectedAuth: 'any',
    lastTest: null
  },
  { 
    path: '/login', 
    name: 'Login Page', 
    description: 'Guest only (redirects if logged in)',
    expectedAuth: 'guest',
    lastTest: null
  },
  { 
    path: '/register', 
    name: 'Register Page', 
    description: 'Guest only (redirects if logged in)',
    expectedAuth: 'guest',
    lastTest: null
  }
])

const testUsers = {
  STUDENT: {
    id: 1,
    email: 'student@test.com',
    name: 'Test Student',
    role: 'STUDENT',
    is_superuser: false
  },
  ENTREPRENEUR: {
    id: 2,
    email: 'entrepreneur@test.com',
    name: 'Test Entrepreneur',
    role: 'ENTREPRENEUR',
    is_superuser: false
  },
  CDS_OWNER: {
    id: 3,
    email: 'cds@test.com',
    name: 'Test CDS Owner',
    role: 'CDS_OWNER',
    is_superuser: false
  },
  LAUNDRY_STAFF: {
    id: 4,
    email: 'laundry@test.com',
    name: 'Test Laundry Staff',
    role: 'LAUNDRY_STAFF',
    is_superuser: false
  }
}

onMounted(() => {
  updateCurrentUser()
  addResult('Route Guards Test Console initialized', 'info')
})

const updateCurrentUser = () => {
  currentUser.value = getCurrentUser()
}

const addResult = (message, type = 'info') => {
  testResults.value.unshift({
    message,
    type,
    time: new Date().toLocaleTimeString()
  })
}

const clearAuth = () => {
  jwtAuthService.clearAuth()
  updateCurrentUser()
  addResult('Authentication cleared', 'info')
}

const loginAs = (role) => {
  const user = testUsers[role]
  // Simulate JWT auth by setting user data directly
  jwtAuthService.setUser(user)
  // Set a dummy token for testing purposes
  jwtAuthService.setAccessToken('dummy_test_token')
  jwtAuthService.setRefreshToken('dummy_refresh_token')
  updateCurrentUser()
  addResult(`Logged in as ${role}: ${user.name}`, 'success')
}

const testRouteAccess = (route) => {
  const user = getCurrentUser()
  const userRole = user ? user.role : 'GUEST'
  
  let shouldHaveAccess = false
  let expectedBehavior = ''

  switch (route.expectedAuth) {
    case 'none':
      shouldHaveAccess = true
      expectedBehavior = 'Always accessible'
      break
    case 'guest':
      shouldHaveAccess = !user
      expectedBehavior = user ? 'Should redirect to /home' : 'Should be accessible'
      break
    case 'any':
      shouldHaveAccess = !!user
      expectedBehavior = user ? 'Should be accessible' : 'Should redirect to /login'
      break
    default:
      shouldHaveAccess = user && (user.role === route.expectedAuth || user.is_superuser)
      expectedBehavior = shouldHaveAccess ? 'Should be accessible' : 'Should redirect to /unauthorized'
      break
  }

  const result = shouldHaveAccess ? 'success' : 'error'
  const message = `${route.name} | User: ${userRole} | ${expectedBehavior}`
  
  route.lastTest = { result, message }
  addResult(`Route Test: ${message}`, result)
}

const navigateToRoute = (path) => {
  try {
    router.push(path)
    addResult(`Navigating to ${path}`, 'info')
  } catch (error) {
    addResult(`Navigation error to ${path}: ${error.message}`, 'error')
  }
}

const clearResults = () => {
  testResults.value = []
  testRoutes.value.forEach(route => {
    route.lastTest = null
  })
}

const getResultClass = (type) => {
  switch (type) {
    case 'success':
      return 'bg-green-100 text-green-800 border border-green-200'
    case 'error':
      return 'bg-red-100 text-red-800 border border-red-200'
    case 'warning':
      return 'bg-yellow-100 text-yellow-800 border border-yellow-200'
    default:
      return 'bg-blue-100 text-blue-800 border border-blue-200'
  }
}
</script>
