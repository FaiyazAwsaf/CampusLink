<template>
  <NavBar />
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200">
    <div class="container mx-auto px-4 py-8">

      <!-- Search Bar at Top -->
      <div class="mb-8">
        <div class="max-w-2xl mx-auto">
          <label for="search" class="block font-medium mb-3 text-center text-gray-700">Search Products</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <input
              v-model="queryProducts"
              @input="fetchSearchQuery"
              type="text"
              placeholder="Enter product name or related keywords..."
              class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white shadow-sm"
            />
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="lg:flex lg:gap-6">
        <!-- Sidebar with Filters -->
        <div class="lg:w-64 lg:flex-shrink-0 mb-6 lg:mb-0">
          <div class="bg-white rounded-lg shadow-md p-4 lg:sticky lg:top-4">
            <h3 class="text-lg font-semibold mb-4 text-gray-800 border-b pb-2">Filters</h3>
            
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

        <!-- Main Content Area -->
        <div class="flex-1 min-w-0">
          <div>
            <div v-if="loading" class="flex justify-center items-center py-12">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <span class="ml-3 text-lg text-gray-600">Loading products...</span>
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
                d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
              ></path>
            </svg>
            <h3 class="text-lg font-semibold text-gray-600 mb-2">No Products Available</h3>
            <p class="text-gray-500">Check back later for new products!</p>
          </div>

          <div v-else class="space-y-8">
            <!-- Storefronts Section -->
            <div class="bg-white rounded-lg shadow-sm p-6">
              <h2 class="text-xl font-semibold text-gray-800 mb-4">Featured Storefronts</h2>
              <div class="relative">
                <button
                  @click="scrollLeft"
                  class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white hover:bg-gray-50 p-2 rounded-full shadow-md border border-gray-200 transition-all duration-200"
                >
                  <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                  </svg>
                </button>
                
                <div 
                  ref="carousel"
                  class="overflow-x-auto scrollbar-hide mx-8"
                >
                  <div class="flex space-x-4 pb-2">
                    <div v-for="storefront in storefronts" 
                      :key="storefront.store_id" 
                      class="flex-shrink-0 w-32 bg-gray-50 rounded-lg text-center hover:shadow-md transition-shadow duration-200">
                      <img
                        :src="storefront.image"
                        class="w-full h-24 object-cover rounded-t-lg"
                        @error="handleImageError"
                      />
                      <h3 class="font-medium text-sm text-gray-700 p-2 truncate">
                        {{ storefront.name }}
                      </h3>
                    </div>
                  </div>
                </div>

                <button
                  @click="scrollRight"
                  class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white hover:bg-gray-50 p-2 rounded-full shadow-md border border-gray-200 transition-all duration-200"
                >
                  <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                  @add-to-cart="onAddToCart"
                  @product-detail="handleProductDetail"
                  @handle-image-error="handleImageError"
              />
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="flex justify-center items-center mt-8 space-x-2">
              <button
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                :class="[
                  'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                  currentPage === 1
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300 hover:border-gray-400 shadow-sm'
                ]"
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
                  'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                  currentPage === totalPages
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300 hover:border-gray-400 shadow-sm'
                ]"
              >
                Next
              </button>
            </div>
          </div>

          <ProductModal
            v-if="showModal"
            :key="selectedProduct.id"
            :product="selectedProduct"
            @close="closeModal"
            @click.self="closeModal"
          />
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import ProductCard from '@/components/ProductCard.vue'
import ProductModal from '@/components/ProductModal.vue'
import PriceL2HFilter from '@/components/PriceL2HFilter.vue'
import CategoryFilter from '@/components/CategoryFilter.vue'
import StockFilter from '@/components/StockFilter.vue'
import '@vueform/slider/themes/default.css'
import Slider from '@vueform/slider'
import debounce from 'lodash.debounce'

const products = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const selected_category = ref('')
const selectedStore = ref('')
const price_range = ref([0,1000])
const loading = ref(false)
const selectedProduct = ref(null)
const showModal = ref(false)
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
const queryProducts = ref([])

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
    totalPages.value = Math.ceil(data.count / 10) // 10 is page_size

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
    const searchRes = await fetch(`/api/entrepreneurs_hub/search/?query=${encodeURIComponent(query)}`)
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

function handleProductDetail(product){
  selectedProduct.value = product
  showModal.value = true
}

function closeModal(){
  showModal.value = false
  selectedProduct.value = null
}

function onAddToCart(product){
  console.log("Added ", product, " to cart")
}

const handleImageError = (event) =>{
    event.target.src = '/Default.jpg'
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
</style>
