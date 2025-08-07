<template>
  <NavBar />
  <div class="bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200">
    <div class="container mx-auto px-4 py-8 ">

    <div class="flex gap-4">
      <CategoryFilter
        v-model="selected_category"
        @on-filter-change="onFilterChange"
        :categories="categories"
      >        
      </CategoryFilter>

      <div class="mb-8">
        <label for="store" class="block font-medium mb-1">Store</label>
          <select v-model="selectedStore" @change="onFilterChange" class="border p-2 rounded">
            <option value="">All Stores</option>
            <option 
              v-for="storefront in storefronts"
                :key="storefront.store_id"
                :value="storefront.name"
            >{{ storefront.name }}</option>
          </select>
      </div>

      <div class="mb-8">
        <label for="price_range" class="block font-medium mb-1">Price Range</label>
          
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
          <div class="flex justify-between text-sm text-gray-700 mt-2">
            <span>Min: {{ price_range[0] }}</span>
            <span>Max: {{ price_range[1] }}</span>
          </div>
        </div>

        <StockFilter
          v-model="selectedAvailability"
          @on-filter-change="onFilterChange"
          :availabilityOptions="availabilityOptions"
        >
        </StockFilter>

        <div class="mb-8">
          <label for="search" class="block font-medium mb-1">Search Products</label>
          <input
            v-model="queryProducts"
            @input="fetchSearchQuery"
            type="text"
            placeholder="Enter product name or related keywords..."
            class="border p-2 rounded w-full"
          />
        </div>


    </div>
    
  <div>
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-lg text-gray-600">Loading products...</span>
      </div>
  </div>

    <div v-if="products.length === 0 && !loading" class="text-center py-12">
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

    <div v-else>
      <div class="relative">

      <button
        @click="scrollLeft"
        class="absolute left-2 top-1/2 -translate-y-1/2 z-10 bg-white/80 hover:bg-white backdrop-blur-sm p-3 rounded-full shadow-lg border border-gray-200 transition-all duration-200 hover:scale-105"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      
        <div class="font-semibold text-xl text-gray-700">
          Check out our storefronts
        </div>

        <div 
          ref="carousel"
          class="overflow-x-hidden whitespace-nowrap pl-4 pr-4 pb-8">

          <div class="flex justify-center min-w-full p-4">
            <div class="inline-flex space-x-4">
              <div v-for="storefront in storefronts" 
                :key="storefront.store_id" 
                class="relative flex-col flex-shrink-0 justify-center w-40 m-4 bg-gray-100 rounded-lg text-center">
                  <img
                    :src="storefront.image"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
                  />

                  <h3 class="font-semibold text-lg text-gray-700 p-2">
                      {{ storefront.name }}
                  </h3>
              </div>
            </div>
          </div>
        </div>

      <button
        @click="scrollRight"
        class="absolute right-2 top-1/2 -translate-y-1/2 z-10 bg-white/80 hover:bg-white backdrop-blur-sm p-3 rounded-full shadow-lg border border-gray-200 transition-all duration-200 hover:scale-105"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6">
        <ProductCard
          v-for="product in products"
            :key="product.id"
            :product="product"
            @add-to-cart="onAddToCart"
            @product-detail="handleProductDetail"
            @handle-image-error="handleImageError"
        />
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

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import NavBar from '@/components/NavBar.vue'
import ProductCard from '@/components/ProductCard.vue'
import ProductModal from '@/components/ProductModal.vue'
import CategoryFilter from '@/components/CategoryFilter.vue'
import StockFilter from '@/components/StockFilter.vue'
import '@vueform/slider/themes/default.css'
import Slider from '@vueform/slider'
import debounce from 'lodash.debounce'

const products = ref([])
const next_cursor = ref(null)
const selected_category = ref('')
const selectedStore = ref('')
const price_range = ref([0,1000])
const loading = ref(false)
const allLoaded = ref(false)
const selectedProduct = ref(null)
const showModal = ref(false)
const categories = ref([])
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

const loadProducts = async () => {

  if(loading.value || allLoaded.value) {
    return 
  }

  loading.value = true

  try {

    const params = new URLSearchParams()

    if(next_cursor.value){
      params.append('cursor', next_cursor.value)
    }

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

    if(selectedAvailability.value){
      params.append('availability', selectedAvailability.value)
    }
    
    const res = await fetch(`/api/entrepreneurs_hub/products/?${params.toString()}`)
    const data = await res.json()

    products.value.push(...data.results)

    next_cursor.value = data.next
      ? new URL(data.next, window.location.origin).searchParams.get("cursor")
      : null

    if(!data.next){
      allLoaded.value = true
    }

    } catch (err) {
    console.error('Cursor loading failed', err)
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
    products.value = []
    next_cursor.value = null
    allLoaded.value = false
    loadProducts()
    return
  }

  const query = queryProducts.value.trim()

  try{
    const searchRes = await fetch(`/api/entrepreneurs_hub/search/?query=${encodeURIComponent(query)}`)
    const searchResults = await searchRes.json()
    
    products.value = searchResults
    allLoaded.value = true
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
  products.value = []
  next_cursor.value = null
  allLoaded.value = false
  loadProducts()
}

const debouncedFilterChnage = debounce(onFilterChange, 300)

const handleScroll = () => {
  const scrollTop = window.scrollY
  const windowHeight = window.innerHeight
  const fullHeight = document.body.offsetHeight

  if(scrollTop + windowHeight >= fullHeight - 200){
    loadProducts()
  }
}

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
  window.addEventListener('scroll', handleScroll)
  loadProducts()
  fetchFilters()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
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
