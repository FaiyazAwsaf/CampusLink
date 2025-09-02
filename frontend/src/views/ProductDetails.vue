<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200">
    <NavBar />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-lg text-gray-600">Loading product details...</span>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <h3 class="text-lg font-semibold text-red-800 mb-2">Error Loading Product</h3>
          <p class="text-red-600">{{ error }}</p>
          <button
            @click="fetchProduct"
            class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>

      <div v-else-if="product" class="bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="grid md:grid-cols-2 gap-8 p-8">
          <div class="space-y-4">
            <div class="aspect-square bg-gray-100 rounded-lg overflow-hidden">
              <img
                v-if="product.image"
                :src="product.image"
                :alt="product.name"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200"
              >
                <svg class="w-24 h-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 002 2z"/>
                </svg>
              </div>
            </div>
          </div>

          <div class="flex flex-col space-y-6">
            <div>
              <h1 class="text-4xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>
              <p class="text-lg text-gray-700 leading-relaxed">{{ product.description }}</p>
            </div>

            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-3xl font-bold text-blue-600">৳{{ product.price }}</span>
                <div class="flex items-center">
                  <span
                    v-if="product.availability"
                    class="bg-green-100 text-green-800 text-sm font-semibold px-3 py-1 rounded-full"
                  >
                    In Stock
                  </span>
                  <span
                    v-else
                    class="bg-red-100 text-red-800 text-sm font-semibold px-3 py-1 rounded-full"
                  >
                    Out of Stock
                  </span>
                </div>
              </div>

              <div class="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="flex items-center mr-3">
                      <span
                        v-for="star in 5"
                        :key="star"
                        class="text-2xl"
                        :class="star <= Math.round(product.average_rating) ? 'text-yellow-400' : 'text-gray-300'"
                      >
                        ★
                      </span>
                    </div>
                    <div>
                      <span class="text-lg font-semibold text-gray-900">{{ product.average_rating || 0 }}</span>
                      <span class="text-sm text-gray-600 ml-1">({{ product.rating_count || 0 }} {{ product.rating_count === 1 ? 'review' : 'reviews' }})</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-1 gap-4">
                <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                    </svg>
                    <div>
                      <span class="text-sm font-medium text-gray-600">Storefront</span>
                      <p class="text-gray-900 font-semibold">{{ product.store_name }}</p>
                    </div>
                  </div>
                </div>

                <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                    </svg>
                    <div>
                      <span class="text-sm font-medium text-gray-600">Category</span>
                      <p class="text-gray-900 font-semibold">{{ product.category }}</p>
                    </div>
                  </div>
                </div>

                <div v-if="product.views" class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    <div>
                      <span class="text-sm font-medium text-gray-600">Views</span>
                      <p class="text-gray-900 font-semibold">{{ product.views }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="pt-6 border-t border-gray-200 space-y-4">
              <button
                :disabled="!product.availability"
                :class="[
                  'w-full py-4 px-6 rounded-lg font-semibold text-lg transition-all duration-200 transform',
                  product.availability
                    ? 'bg-blue-600 hover:bg-blue-700 text-white hover:scale-105 shadow-lg hover:shadow-xl'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                ]"
                @click="addToCart"
              >
                <span v-if="product.availability">Add to Cart</span>
                <span v-else>Out of Stock</span>
              </button>

              <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900 mb-3">Rate this product</h3>
                <div class="space-y-3">
                  <div class="flex items-center space-x-2">
                    <span class="text-sm font-medium text-gray-700">Your rating:</span>
                    <div class="flex items-center">
                      <button
                        v-for="star in 5"
                        :key="star"
                        @click="setRating(star)"
                        class="text-2xl transition-colors duration-200"
                        :class="star <= userRating ? 'text-yellow-400 hover:text-yellow-500' : 'text-gray-300 hover:text-yellow-300'"
                      >
                        ★
                      </button>
                    </div>
                    <span v-if="userRating" class="text-sm text-gray-600 ml-2">{{ userRating }} star{{ userRating !== 1 ? 's' : '' }}</span>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Review (optional)</label>
                    <textarea
                      v-model="userReview"
                      rows="3"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Share your thoughts about this product..."
                    ></textarea>
                  </div>

                  <button
                    @click="submitRating"
                    :disabled="!userRating || submittingRating"
                    class="w-full py-2 px-4 bg-yellow-500 text-white rounded-lg font-semibold hover:bg-yellow-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors duration-200"
                  >
                    <span v-if="submittingRating">Submitting...</span>
                    <span v-else>Submit Rating</span>
                  </button>

                  <div v-if="ratingMessage" class="mt-3 p-3 rounded-lg transition-all duration-300" :class="{
                    'bg-green-50 border border-green-200 text-green-800': ratingMessageType === 'success',
                    'bg-red-50 border border-red-200 text-red-800': ratingMessageType === 'error'
                  }">
                    <div class="flex items-center">
                      <svg v-if="ratingMessageType === 'success'" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                      </svg>
                      <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                      <span class="text-sm font-medium">{{ ratingMessage }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import useCart from '@/utils/useCart.js'
import { AuthService } from '@/utils/auth.js'

const route = useRoute()
const router = useRouter()
const { addToCart: addToCartGlobal } = useCart()

const product = ref(null)
const loading = ref(true)
const error = ref(null)
const userRating = ref(0)
const userReview = ref('')
const submittingRating = ref(false)
const ratingMessage = ref('')
const ratingMessageType = ref('') 

const fetchProduct = async () => {
  loading.value = true
  error.value = null

  try {
    const productId = route.params.id
    const response = await fetch(`/api/entrepreneurs_hub/products/${productId}/`)
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`)
    }

    product.value = await response.json()
  } catch (err) {
    error.value = `Failed to load product: ${err.message}`
    console.error('Error fetching product:', err)
  } finally {
    loading.value = false
  }
}


const setRating = (rating) => {
  userRating.value = rating
}

const getCsrfToken = async () => {
  try {
    const response = await fetch('/api/accounts/csrf/', {
      credentials: 'include'
    })
    if (response.ok) {
      return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1]
    }
  } catch (err) {
    console.error('Error getting CSRF token:', err)
  }
  return null
}

const showMessage = (message, type) => {
  ratingMessage.value = message
  ratingMessageType.value = type
  
  setTimeout(() => {
    ratingMessage.value = ''
    ratingMessageType.value = ''
  }, 5000)
}

const submitRating = async () => {
  if (!userRating.value) return

  const storedUser = localStorage.getItem('user')
  if (!storedUser) {
    showMessage('Please log in to rate this product', 'error')
    return
  }

  submittingRating.value = true
  ratingMessage.value = ''

  try {
    const productId = route.params.id
    
    const csrfToken = await getCsrfToken()

    const headers = {
      'Content-Type': 'application/json',
    }

    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken
    }

    const response = await fetch(`/api/entrepreneurs_hub/products/${productId}/rate/`, {
      method: 'POST',
      headers: headers,
      credentials: 'include', 
      body: JSON.stringify({
        rating: userRating.value,
        review: userReview.value
      })
    })

    const data = await response.json()

    if (response.ok && data.success) {
      product.value.average_rating = data.average_rating
      product.value.rating_count = data.rating_count
      
      userRating.value = 0
      userReview.value = ''
      
      showMessage(data.message, 'success')
    } else {
      console.error('Rating submission failed:', data)
      showMessage(data.error || `Failed to submit rating: ${response.status} ${response.statusText}`, 'error')
    }
  } catch (err) {
    console.error('Error submitting rating:', err)
    showMessage('Failed to submit rating. Please try again.', 'error')
  } finally {
    submittingRating.value = false
  }
}

const addToCart = () => {
  // Check if user is authenticated
  if (!AuthService.isAuthenticated()) {
    // Store current route to redirect back after login
    const currentRoute = router.currentRoute.value.fullPath
    router.push({
      name: 'login',
      query: { next: currentRoute }
    })
    return
  }
  
  // Add to cart if authenticated
  addToCartGlobal(product.value, 'entrepreneurs_hub')
  alert(`Added "${product.value.name}" to cart!`)
}

const handleImageError = (event) => {
  event.target.src = '/Default.jpg'
}

onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>
.hover\:scale-105:hover {
  transform: scale(1.05);
}
</style>
