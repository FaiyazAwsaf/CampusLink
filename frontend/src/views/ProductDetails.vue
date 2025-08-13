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

            <div class="pt-6 border-t border-gray-200">
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

const route = useRoute()
const router = useRouter()

const product = ref(null)
const loading = ref(true)
const error = ref(null)

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


const addToCart = () => {
  console.log('Adding to cart:', product.value)
  alert(`Added "${product.value.name}" to cart! (Cart functionality coming soon)`)
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
