<template>
  <NavBar />
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200">
    <div class="container mx-auto px-4 py-8">
      
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
        <span class="ml-4 text-xl text-gray-600">Loading store...</span>
      </div>

      <div v-else-if="store" class="space-y-8">
        
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
          <div class="relative h-48 md:h-64 bg-gradient-to-r from-blue-500 to-indigo-600">
            <img 
              v-if="store.image" 
              :src="store.image" 
              :alt="store.name"
              class="w-full h-full object-cover opacity-80"
              @error="handleImageError"
            />
            <div class="absolute inset-0 bg-black bg-opacity-30"></div>
            <div class="absolute bottom-6 left-6 text-white">
              <h1 class="text-3xl md:text-4xl font-bold mb-2">{{ store.name }}</h1>
              <div class="flex items-center space-x-4 text-sm md:text-base">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                  {{ store.average_rating || 0 }} Stars
                </div>
                <div>{{ store.total_products }} Products</div>
                <div>{{ store.total_reviews }} Reviews</div>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          <div class="lg:col-span-2 space-y-8">
            
            <div class="bg-white rounded-xl shadow-md p-6">
              <h2 class="text-2xl font-bold text-gray-800 mb-4">About This Store</h2>
              <p v-if="store.description" class="text-gray-600 leading-relaxed mb-4">
                {{ store.description }}
              </p>
              <p v-else class="text-gray-500 italic">No description available.</p>
              
              <div v-if="store.established_date || store.location" class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-if="store.established_date" class="flex items-center text-gray-600">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  Established: {{ formatDate(store.established_date) }}
                </div>
                <div v-if="store.location" class="flex items-center text-gray-600">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  {{ store.location }}
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-md p-6">
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-4 sm:mb-0">Store Products</h2>
                <select 
                  v-model="sortOrder" 
                  @change="loadProducts"
                  class="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="created_at">Newest First</option>
                  <option value="-created_at">Oldest First</option>
                  <option value="name">Name A-Z</option>
                  <option value="-name">Name Z-A</option>
                  <option value="price">Price Low to High</option>
                  <option value="-price">Price High to Low</option>
                </select>
              </div>

              <div v-if="productsLoading" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>

              <div v-else-if="products.length === 0" class="text-center py-12">
                <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2 2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
                </svg>
                <h3 class="text-lg font-semibold text-gray-600 mb-2">No Products Yet</h3>
                <p class="text-gray-500">This store hasn't added any products yet.</p>
              </div>

              <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                <ProductCard
                  v-for="product in products"
                  :key="product.product_id"
                  :product="product"
                  @add-to-cart="onAddToCart"
                  @handle-image-error="handleImageError"
                />
              </div>

              <div v-if="totalPages > 1" class="flex justify-center items-center mt-8 space-x-2">
                <button
                  @click="goToPage(currentPage - 1)"
                  :disabled="currentPage === 1"
                  class="px-4 py-2 rounded-lg font-medium transition-all duration-200 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
                >
                  Previous
                </button>

                <div class="flex space-x-1">
                  <button
                    v-for="page in visiblePages"
                    :key="page"
                    @click="goToPage(page)"
                    :class="[
                      'px-3 py-2 rounded-lg font-medium transition-all duration-200',
                      page === currentPage
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                    ]"
                  >
                    {{ page }}
                  </button>
                </div>

                <button
                  @click="goToPage(currentPage + 1)"
                  :disabled="currentPage === totalPages"
                  class="px-4 py-2 rounded-lg font-medium transition-all duration-200 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
                >
                  Next
                </button>
              </div>
            </div>
          </div>

          <div class="space-y-6">
            
            <div v-if="store.owner" class="bg-white rounded-xl shadow-md p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-4">Store Owner</h3>
              <div class="flex items-center space-x-4 mb-4">
                <img 
                  v-if="store.owner.image" 
                  :src="store.owner.image" 
                  :alt="store.owner.name"
                  class="w-16 h-16 rounded-full object-cover border-2 border-gray-200"
                  @error="handleImageError"
                />
                <div v-else class="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center text-2xl font-bold text-gray-600">
                  {{ store.owner.name.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <h4 class="font-semibold text-gray-800">{{ store.owner.name }}</h4>
                  <p class="text-sm text-gray-600">Store Owner</p>
                </div>
              </div>
              
              <p v-if="store.owner.bio" class="text-gray-600 text-sm leading-relaxed mb-4">
                {{ store.owner.bio }}
              </p>

              <div v-if="store.owner.facebook_url || store.owner.instagram_url || store.owner.website_url" class="flex space-x-3">
                <a v-if="store.owner.facebook_url" :href="store.owner.facebook_url" target="_blank" class="text-blue-600 hover:text-blue-800">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                </a>
                <a v-if="store.owner.instagram_url" :href="store.owner.instagram_url" target="_blank" class="text-pink-600 hover:text-pink-800">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987 6.62 0 11.987-5.367 11.987-11.987C24.014 5.367 18.637.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.49-3.323-1.297C4.198 14.895 3.708 13.744 3.708 12.447s.49-2.448 1.418-3.323c.875-.807 2.026-1.297 3.323-1.297s2.448.49 3.323 1.297c.928.875 1.418 2.026 1.418 3.323s-.49 2.448-1.418 3.244c-.875.807-2.026 1.297-3.323 1.297zm7.83-9.608h-1.507V6.61h1.507v.77zm-.77 2.295c-.49-.49-1.125-.735-1.908-.735s-1.418.245-1.908.735-.735 1.125-.735 1.908.245 1.418.735 1.908.1.125.735.735 1.418.735c.783 0 1.418-.245 1.908-.735s.735-1.125.735-1.908-.245-1.418-.735-1.908z"/>
                  </svg>
                </a>
                <a v-if="store.owner.website_url" :href="store.owner.website_url" target="_blank" class="text-gray-600 hover:text-gray-800">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>
                  </svg>
                </a>
              </div>
            </div>

            <div v-if="store.store_hours || store.return_policy || store.shipping_info" class="bg-white rounded-xl shadow-md p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-4">Store Information</h3>
              
              <div v-if="store.store_hours" class="mb-4">
                <h4 class="font-semibold text-gray-700 mb-2">Store Hours</h4>
                <p class="text-gray-600 text-sm">{{ store.store_hours }}</p>
              </div>

              <div v-if="store.return_policy" class="mb-4">
                <h4 class="font-semibold text-gray-700 mb-2">Return Policy</h4>
                <p class="text-gray-600 text-sm">{{ store.return_policy }}</p>
              </div>

              <div v-if="store.shipping_info">
                <h4 class="font-semibold text-gray-700 mb-2">Shipping Information</h4>
                <p class="text-gray-600 text-sm">{{ store.shipping_info }}</p>
              </div>
            </div>

            <div v-if="store.owner && (store.owner.phone || store.owner.email)" class="bg-white rounded-xl shadow-md p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-4">Contact Information</h3>
              
              <div v-if="store.owner.phone" class="flex items-center mb-3">
                <svg class="w-5 h-5 mr-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                </svg>
                <span class="text-gray-700">{{ store.owner.phone }}</span>
              </div>

              <div v-if="store.owner.email" class="flex items-center">
                <svg class="w-5 h-5 mr-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                <span class="text-gray-700">{{ store.owner.email }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <h2 class="text-2xl font-semibold text-gray-600 mb-2">Store Not Found</h2>
        <p class="text-gray-500">The store you're looking for doesn't exist or has been removed.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import ProductCard from '@/components/ProductCard.vue'
import useCart from '@/utils/useCart.js'
import { AuthService } from '@/utils/auth.js'

const route = useRoute()
const router = useRouter()
const { addToCart: addToCartGlobal } = useCart()
const storeId = route.params.storeId

const store = ref(null)
const products = ref([])
const loading = ref(true)
const productsLoading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const sortOrder = ref('created_at')

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)

  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const loadStore = async () => {
  try {
    const response = await fetch(`/api/entrepreneurs_hub/storefronts/${storeId}/`)
    if (response.ok) {
      store.value = await response.json()
    } else {
      console.error('Store not found')
    }
  } catch (error) {
    console.error('Error loading store:', error)
  } finally {
    loading.value = false
  }
}

const loadProducts = async () => {
  productsLoading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value,
      ordering: sortOrder.value
    })
    
    const response = await fetch(`/api/entrepreneurs_hub/storefronts/${storeId}/products/?${params}`)
    if (response.ok) {
      const data = await response.json()
      products.value = data.results
      totalPages.value = Math.ceil(data.count / 12)
    }
  } catch (error) {
    console.error('Error loading products:', error)
  } finally {
    productsLoading.value = false
  }
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
    currentPage.value = page
    loadProducts()
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const handleImageError = (event) => {
  event.target.src = '/Default.jpg'
}

const onAddToCart = (product) => {
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
  addToCartGlobal(product, 'entrepreneurs_hub')
  alert(`Added "${product.name}" to cart!`)
}

onMounted(() => {
  loadStore()
  loadProducts()
})
</script>
