<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="min-h-screen" style="background-color: var(--color-primaryBg)">
    <NavBar />

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-lg text-gray-600">Loading items...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <svg
            class="w-12 h-12 text-red-500 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <h3 class="text-lg font-semibold text-red-800 mb-2">Error Loading Items</h3>
          <p class="text-red-600">{{ error }}</p>
          <button
            @click="fetchItems"
            class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>

      <!-- Items Grid -->
      <div v-else>
        <!-- Stats Bar -->
        <div class="mb-6 bg-white rounded-lg shadow-sm p-4">
          <div class="flex justify-between items-center">
            <p class="text-gray-600">
              Showing <span class="font-semibold">{{ items.length }}</span> items
            </p>
          </div>
        </div>

        <!-- Products Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="item in items"
            :key="item.item_id"
            class="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden border border-gray-100 flex flex-col h-full"
          >
            <!-- Image Section (Top Half) -->
            <div class="relative h-48 bg-gray-100">
              <img
                v-if="item.image"
                :src="item.image"
                :alt="item.name"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200"
              >
                <svg
                  class="w-16 h-16 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  ></path>
                </svg>
              </div>

              <!-- Availability Badge -->
              <div class="absolute top-3 right-3">
                <span
                  v-if="item.availability"
                  class="bg-green-500 text-white text-xs font-semibold px-2 py-1 rounded-full"
                >
                  In Stock
                </span>
                <span
                  v-else
                  class="bg-red-500 text-white text-xs font-semibold px-2 py-1 rounded-full"
                >
                  Out of Stock
                </span>
              </div>
            </div>

            <!-- Product Info Section -->
            <div class="p-4 flex flex-col flex-1">
              <div class="flex-1">
                <!-- Product Name -->
                <h3 class="font-semibold text-gray-900 text-lg mb-2 line-clamp-2">
                  {{ item.name }}
                </h3>

                <!-- Product Description -->
                <p class="text-gray-600 text-sm mb-3 line-clamp-2">
                  {{ item.description }}
                </p>
              </div>

              <div>
                <!-- Price and Stock Info -->
                <div class="flex justify-between items-center mb-4">
                  <div>
                    <span class="text-2xl font-bold text-blue-600 mt-auto"
                      >Tk. {{ item.price }}</span
                    >
                  </div>
                </div>

                <!-- Add to Cart Button -->
                <button
                  :disabled="!item.availability"
                  :class="[
                    'w-full py-2 px-4 rounded-lg font-semibold transition-all duration-200 mt-auto',
                    item.availability
                      ? 'bg-blue-600 hover:bg-blue-700 text-white hover:shadow-md'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed',
                  ]"
                  @click="addToCart(item)"
                >
                  <span v-if="item.availability"> Add to Cart </span>
                  <span v-else> Out of Stock </span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="items.length === 0" class="text-center py-12">
          <svg
            class="w-16 h-16 text-gray-400 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
            ></path>
          </svg>
          <h3 class="text-lg font-semibold text-gray-600 mb-2">No Items Available</h3>
          <p class="text-gray-500">Check back later for new products!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import { ref, onMounted } from 'vue'

// State variables
const items = ref([])
const loading = ref(true)
const error = ref(null)

// Fetch data from the backend API
const fetchItems = async () => {
  try {
    loading.value = true
    error.value = null

    const response = await fetch('/api/cds/items/')

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()
    items.value = data.items || []
  } catch (err) {
    error.value = `Failed to load items: ${err.message}`
    console.error('Error fetching CDS items:', err)
  } finally {
    loading.value = false
  }
}

// Handle image loading errors
const handleImageError = (event) => {
  // Hide broken image and show placeholder
  event.target.style.display = 'none'
}

// Add to cart function (placeholder for future implementation)
const addToCart = (item) => {
  // TODO: Implement cart functionality
  console.log('Adding to cart:', item)
  alert(`Added "${item.name}" to cart! (Cart functionality coming soon)`)
}

// Fetch data when component is mounted
onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
/* Custom styles for line clamping */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Smooth hover animations */
.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}

/* Loading animation */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
