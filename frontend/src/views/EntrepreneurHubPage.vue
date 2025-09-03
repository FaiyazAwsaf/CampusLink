<template>
  <NavBar />
  
  <!-- Toast Notification -->
  <div v-if="showToast" class="fixed top-4 right-4 z-50 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 ease-in-out"
       :class="{ 'translate-x-0 opacity-100': showToast, 'translate-x-full opacity-0': !showToast }">
    <div class="flex items-center">
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      {{ toastMessage }}
    </div>
  </div>

  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200">
    <div class="container mx-auto px-4 py-8">

      <div class="mb-6 md:mb-8 transform transition-all duration-500 ease-out relative z-20" :class="{ 'scale-105': searchFocused }">
        <div class="max-w-2xl mx-auto">
          <label for="search" class="block font-medium mb-2 md:mb-3 text-center text-gray-700 transition-colors duration-300 text-sm md:text-base">Search Products</label>
          <div class="relative">
            <input
              v-model="queryProducts"
              @keyup.enter="performSearch"
              @input="handleAutocompleteInput"
              @focus="handleSearchFocus"
              @blur="handleSearchBlur"
              type="text"
              placeholder="Search products..."
              class="block w-full pl-4 pr-12 py-3 md:py-4 border border-gray-300 rounded-xl text-base md:text-lg placeholder-gray-500 focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 bg-white shadow-lg hover:shadow-xl transition-all duration-300 ease-out transform hover:-translate-y-0.5"
            />
            <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
              <Transition name="spin" mode="out-in">
                <svg v-if="!searchLoading" class="h-6 w-6 text-gray-400 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                <div v-else class="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent"></div>
              </Transition>
            </div>
            
            <!-- Autocomplete Suggestions -->
            <Transition name="slide-fade">
              <div v-if="showSuggestions && suggestions.length > 0" class="absolute z-20 w-full mt-2 bg-white border border-gray-200 rounded-xl shadow-2xl max-h-64 overflow-y-auto backdrop-blur-sm">
                <div
                  v-for="(suggestion, index) in suggestions"
                  :key="index"
                  @mousedown="selectSuggestion(suggestion)"
                  class="px-4 py-3 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors duration-200"
                >
                  <div class="flex items-center">
                    <svg class="h-4 w-4 text-gray-400 mr-3 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                    </svg>
                    <span class="text-gray-700 font-medium">{{ suggestion }}</span>
                  </div>
                </div>
              </div>
            </Transition>
            
            <!-- Spell Suggestions -->
            <Transition name="bounce-in">
              <div v-if="spellSuggestions.length > 0 && queryProducts.length > 2" class="mt-3">
                <p class="text-sm text-gray-600 mb-2 font-medium">Did you mean:</p>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="(suggestion, index) in spellSuggestions"
                    :key="suggestion"
                    @click="selectSpellSuggestion(suggestion)"
                    class="px-4 py-2 bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 rounded-full text-sm hover:from-blue-200 hover:to-indigo-200 transition-all duration-300 ease-out transform hover:scale-105 hover:shadow-md"
                    :style="{ animationDelay: `${index * 100}ms` }"
                  >
                    {{ suggestion }}
                  </button>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>

      <div class="lg:flex lg:gap-6">
        <div class="lg:hidden mb-4">
          <button
            @click="toggleFilters"
            class="w-full bg-white text-gray-700 px-4 py-3 rounded-lg shadow-md border border-gray-200 flex items-center justify-between hover:bg-gray-50 transition-colors duration-200"
          >
            <span class="font-medium">Filters & Sort</span>
            <svg 
              class="w-5 h-5 transition-transform duration-200" 
              :class="{ 'rotate-180': showMobileFilters }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
        </div>

        <div class="lg:w-64 lg:flex-shrink-0 mb-6 lg:mb-0">
          <div 
            class="bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 ease-in-out"
            :class="{ 'max-h-0 lg:max-h-none': !showMobileFilters, 'max-h-96 lg:max-h-none': showMobileFilters }"
          >
            <div class="p-4">
              <h3 class="text-lg font-semibold mb-4 text-gray-800 border-b pb-2 hidden lg:block">Filters</h3>
            
            <div class="space-y-4">
              <CategoryFilter
                v-model="selected_category"
                @on-filter-change="onFilterChange"
                :categories="categories"
              />

              <div>
                <label for="store" class="block font-medium mb-2 text-gray-700">Store</label>
                <select v-model="selectedStore" @change="onFilterChange" class="w-full border border-gray-300 p-2 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All Stores</option>
                  <option 
                    v-for="storefront in storefronts"
                      :key="storefront.store_id"
                      :value="storefront.name"
                  >{{ storefront.name }}</option>
                </select>
              </div>

              <div>
                <label for="price_range" class="block font-medium mb-2 text-gray-700">Price Range</label>
                <Slider
                  v-model="price_range"
                    :min="0"
                    :max="1000"
                    :step="10"
                    :tooltip="false"
                    :lazy="true"
                    :range="true"
                    class="mt-2 custom-slider"
                    @update:modelValue="debouncedFilterChnage"
                />
                <div class="flex justify-between text-sm text-gray-600 mt-2">
                  <span>৳{{ price_range[0] }}</span>
                  <span>৳{{ price_range[1] }}</span>
                </div>
              </div>

              <PriceL2HFilter
                v-model="sortOrder"
                @on-filter-change="onFilterChange">
              </PriceL2HFilter>

              <StockFilter
                v-model="selectedAvailability"
                @on-filter-change="onFilterChange"
                :availabilityOptions="availabilityOptions"
              />
            </div>
            </div>
          </div>
        </div>

        <!-- Main Content Area -->
        <div class="flex-1 min-w-0">
          <div>
            <div v-if="loading" class="flex justify-center items-center py-12">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <span class="ml-3 text-lg text-gray-600">
                {{ queryProducts.trim() ? 'Searching...' : 'Loading products...' }}
              </span>
            </div>
          </div>

          <div v-if="products.length === 0 && !loading" class="text-center py-12 bg-white rounded-lg shadow-sm">
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
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              ></path>
            </svg>
            <h3 class="text-lg font-semibold text-gray-600 mb-2">
              {{ queryProducts.trim() ? 'No products found' : 'No Products Available' }}
            </h3>
            <p class="text-gray-500">
              {{ queryProducts.trim() ? 'Try different keywords or check spelling' : 'Check back later for new products!' }}
            </p>
          </div>

          <div v-else class="space-y-8">
            <!-- Storefronts Section -->
            <div class="bg-white rounded-lg shadow-sm p-4 md:p-6">
              <h2 class="text-lg md:text-xl font-semibold text-gray-800 mb-4">Featured Storefronts</h2>
              <div class="relative">
                <button
                  @click="scrollLeft"
                  class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white hover:bg-gray-50 p-1 md:p-2 rounded-full shadow-md border border-gray-200 transition-all duration-200"
                >
                  <svg class="w-3 h-3 md:w-4 md:h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                  </svg>
                </button>
                
                <div 
                  ref="carousel"
                  class="overflow-hidden mx-6 md:mx-8"
                >
                  <div class="flex space-x-3 md:space-x-4 pb-2">
                    <div v-for="storefront in storefronts" 
                      :key="storefront.store_id" 
                      @click="navigateToStore(storefront.store_id)"
                      class="flex-shrink-0 w-24 md:w-32 bg-gray-50 rounded-lg text-center hover:shadow-md transition-all duration-200 relative cursor-pointer hover:scale-105 hover:bg-white">
                      <img
                        :src="storefront.image"
                        class="w-full h-16 md:h-24 object-cover rounded-t-lg"
                        @error="handleImageError"
                      />
                      <h3 class="font-medium text-xs md:text-sm text-gray-700 p-1 md:p-2 truncate">
                        {{ storefront.name }}
                      </h3>
                    </div>
                  </div>
                </div>

                <button
                  @click="scrollRight"
                  class="absolute right-0 top-1/2 -translate-y-1/2 bg-white hover:bg-gray-50 p-1 md:p-2 rounded-full shadow-md border border-gray-200 transition-all duration-200"
                >
                  <svg class="w-3 h-3 md:w-4 md:h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Products Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              <ProductCard
                v-for="product in products"
                  :key="product.id"
                  :product="product"
                  :addedItems="addedItems"
                  @add-to-cart="onAddToCart"
                  @handle-image-error="handleImageError"
              />
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1 && !queryProducts.trim()" class="flex flex-col sm:flex-row justify-center items-center mt-8 space-y-3 sm:space-y-0 sm:space-x-2">
              <div class="flex items-center space-x-2">
                <button
                  @click="goToPage(currentPage - 1)"
                  :disabled="currentPage === 1"
                  :class="[
                    'px-3 md:px-4 py-2 rounded-lg font-medium transition-all duration-200 text-sm md:text-base',
                    currentPage === 1
                      ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300 hover:border-gray-400 shadow-sm'
                  ]"
                >
                  <span class="hidden sm:inline">Previous</span>
                  <span class="sm:hidden">←</span>
                </button>

                <div class="flex space-x-1">
                  <button
                    v-for="page in visiblePages"
                    :key="page"
                    @click="goToPage(page)"
                    :class="[
                      'px-2 md:px-3 py-2 rounded-lg font-medium transition-all duration-200 text-sm md:text-base',
                      page === currentPage
                        ? 'bg-blue-600 text-white shadow-sm'
                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300 hover:border-gray-400 shadow-sm'
                    ]"
                  >
                    {{ page }}
                  </button>
                </div>

                <button
                  @click="goToPage(currentPage + 1)"
                  :disabled="currentPage === totalPages"
                  :class="[
                    'px-3 md:px-4 py-2 rounded-lg font-medium transition-all duration-200 text-sm md:text-base',
                    currentPage === totalPages
                      ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300 hover:border-gray-400 shadow-sm'
                  ]"
                >
                  <span class="hidden sm:inline">Next</span>
                  <span class="sm:hidden">→</span>
                </button>
              </div>
              
              <div class="text-sm text-gray-600 sm:ml-4">
                Page {{ currentPage }} of {{ totalPages }}
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import ProductCard from '@/components/ProductCard.vue'
import PriceL2HFilter from '@/components/PriceL2HFilter.vue'
import CategoryFilter from '@/components/CategoryFilter.vue'
import StockFilter from '@/components/StockFilter.vue'
import '@vueform/slider/themes/default.css'
import Slider from '@vueform/slider'
import debounce from 'lodash.debounce'
import useCart from '@/utils/useCart.js'
import { AuthService } from '@/utils/auth.js'


const router = useRouter()
const { addToCart: addToCartGlobal } = useCart()

const products = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const selected_category = ref('')
const selectedStore = ref('')
const price_range = ref([0,1000])
const loading = ref(false)
const categories = ref([])
const sortOrder = ref('')
const recentlyAdded = ref([])
const popularProducts = ref([])
const selectedAvailability = ref('')
const availabilityOptions = [
  {label : 'All Products', value : ''},
  {label : 'In Stock', value : 'true'},
  {label : 'Out of Stock', value : 'false'},
]
const storefronts = ref([])
const carousel = ref([])
const queryProducts = ref('')
const suggestions = ref([])
const spellSuggestions = ref([])
const showSuggestions = ref(false)
const searchLoading = ref(false)
const searchFocused = ref(false)
const showMobileFilters = ref(false)
const showToast = ref(false)
const toastMessage = ref('')
const addedItems = ref(new Set())

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

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
    currentPage.value = page
    loadProducts()
  }
}

const loadProducts = async () => {
  if(loading.value) {
    return 
  }

  loading.value = true

  try {
    const params = new URLSearchParams()

    params.append('page', currentPage.value)

    if(selected_category.value){
      params.append('category', selected_category.value)
    }

    if(selectedStore.value){
      params.append('store', selectedStore.value)
    }

    if(price_range.value && price_range.value.length === 2){
      params.append('min_price', price_range.value[0])
      params.append('max_price', price_range.value[1])
    }

    if(sortOrder.value){
      params.append('ordering', sortOrder.value)
    }

    if(selectedAvailability.value){
      params.append('availability', selectedAvailability.value)
    }
    
    const res = await fetch(`/api/entrepreneurs_hub/products/?${params.toString()}`)
    const data = await res.json()

    products.value = data.results
    totalPages.value = Math.ceil(data.count / 12) // 12 is page_size

  } catch (err) {
    console.error('Loading products failed', err)
  } finally {
    loading.value = false
  }
}

const fetchFilters = async () =>{
  try{
    const categoryRes = await fetch(`/api/entrepreneurs_hub/products/categories/`)
    const storefrontRes = await fetch(`/api/entrepreneurs_hub/products/storefronts/`)

    categories.value = await categoryRes.json()
    storefronts.value = await storefrontRes.json()
  }
  catch(err){
    console.log("Cannot fetch categories/store : ", err)
  }
}

const fetchSearchQuery = async () =>{
  if(!queryProducts.value.trim()){
    currentPage.value = 1
    loadProducts()
    return
  }

  const query = queryProducts.value.trim()

  try{
    const searchRes = await fetch(`/api/entrepreneurs_hub/search/advanced/?query=${encodeURIComponent(query)}`)
    const searchResults = await searchRes.json()
    
    products.value = searchResults
  }
  catch(err){
    console.log("Error fetching products:", err)
  }
}

const fetchRecentlyAdded = async () =>{
  try{
    const res = await fetch(`/api/entrepreneurs_hub/products/recent/`)
    recentlyAdded.value = await res.json()
  }
  catch(err){
    console.log("Cannot fetch recently added")
  }
}

const onFilterChange = () => {
  queryProducts.value = ''
  currentPage.value = 1
  loadProducts()
}


const debouncedFilterChnage = debounce(onFilterChange, 300)

// Removed scroll-based pagination - using page numbers now

const scrollLeft = () => {
  carousel.value.scrollBy({left : -300, behavior : 'smooth'})
}

const scrollRight = () => {
  carousel.value.scrollBy({left : 300, behavior : 'smooth'})
}


const showToastNotification = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

function onAddToCart(product){
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

const handleImageError = (event) =>{
    event.target.src = '/Default.jpg'
}

const fetchAutocomplete = async (query) => {
  if (query.length < 2) {
    suggestions.value = []
    return
  }

  try {
    const response = await fetch(`/api/entrepreneurs_hub/search/autocomplete/?query=${encodeURIComponent(query)}`)
    suggestions.value = await response.json()
  } catch (err) {
    console.log("Autocomplete error:", err)
    suggestions.value = []
  }
}

const fetchSpellSuggestions = async (query) => {
  if (query.length < 3) {
    spellSuggestions.value = []
    return
  }

  try {
    const response = await fetch(`/api/entrepreneurs_hub/search/suggestions/?query=${encodeURIComponent(query)}`)
    spellSuggestions.value = await response.json()
  } catch (err) {
    console.log("Spell suggestions error:", err)
    spellSuggestions.value = []
  }
}

const handleAutocompleteInput = debounce(async () => {
  await Promise.all([
    fetchAutocomplete(queryProducts.value),
    fetchSpellSuggestions(queryProducts.value)
  ])
}, 300)

const performSearch = async () => {
  if (!queryProducts.value.trim()) {
    loadProducts()
    return
  }
  
  searchLoading.value = true
  await fetchSearchQuery()
  searchLoading.value = false
}

const selectSuggestion = (suggestion) => {
  queryProducts.value = suggestion
  showSuggestions.value = false
  performSearch()
}

const selectSpellSuggestion = (suggestion) => {
  queryProducts.value = suggestion
  spellSuggestions.value = []
  performSearch()
}

const hideSuggestions = () => {
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

const clearSearch = () => {
  queryProducts.value = ''
  suggestions.value = []
  spellSuggestions.value = []
  loadProducts()
}

const handleSearchFocus = () => {
  searchFocused.value = true
  showSuggestions.value = true
}

const handleSearchBlur = () => {
  searchFocused.value = false
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

const toggleFilters = () => {
  showMobileFilters.value = !showMobileFilters.value
}

const navigateToStore = (storeId) => {
  router.push(`/entrepreneur-hub/store/${storeId}`)
}

onMounted(() => {
  loadProducts()
  fetchFilters()
})

</script>

<style scoped>
.custom-slider{
  --slider-handle-size : 25px;
  --slider-height : 6px;
  --slider-connect-bg : #4b5563;
  --slider-handle-bg : #4b5563;
  --slider-tooltip-bg : #000000;
}

.slide-fade-enter-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-5px);
  opacity: 0;
}

/* Bounce In Animation */
.bounce-in-enter-active {
  animation: bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.bounce-in-leave-active {
  transition: all 0.3s ease-in;
}

.bounce-in-enter-from,
.bounce-in-leave-to {
  transform: scale(0.8);
  opacity: 0;
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
  70% {
    transform: scale(0.9);
    opacity: 0.9;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Spin Transition */
.spin-enter-active,
.spin-leave-active {
  transition: all 0.3s ease-in-out;
}

.spin-enter-from {
  transform: rotate(-180deg) scale(0.8);
  opacity: 0;
}

.spin-leave-to {
  transform: rotate(180deg) scale(0.8);
  opacity: 0;
}

/* Enhanced hover effects */
.hover-lift {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

/* Smooth focus ring */
.focus-ring {
  transition: all 0.2s ease-in-out;
}

.focus-ring:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

/* Gradient text animation */
@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.gradient-text {
  background: linear-gradient(-45deg, #3b82f6, #8b5cf6, #06b6d4, #10b981);
  background-size: 400% 400%;
  animation: gradient-shift 3s ease infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Stagger animation for spell suggestions */
.bounce-in-enter-active:nth-child(1) { animation-delay: 0ms; }
.bounce-in-enter-active:nth-child(2) { animation-delay: 100ms; }
.bounce-in-enter-active:nth-child(3) { animation-delay: 200ms; }
.bounce-in-enter-active:nth-child(4) { animation-delay: 300ms; }
.bounce-in-enter-active:nth-child(5) { animation-delay: 400ms; }

/* Smooth scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #cbd5e1, #94a3b8);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #94a3b8, #64748b);
}
</style>
