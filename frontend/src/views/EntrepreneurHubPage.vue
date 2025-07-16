<template>
  <NavBar />

  <div class="container mx-auto px-4 py-8">

    <div class="flex gap-4">
      <div class="mb-8">
        <label for="category" class="block font-medium mb-1">Category:</label>
          <select v-model="selected_category" @change="onFilterChange" class="border p-2 rounded">
            <option value="">All</option>
            <option 
              v-for="category in categories"
                :key="category"
                :value="category"
            >{{ category }}</option>
          </select>
      <!-- Add your categories -->
      </div>

      <div class="mb-8">
        <label for="store" class="block font-medium mb-1">Store</label>
          <select v-model="selected_store" @change="onFilterChange" class="border p-2 rounded">
            <option value="">All Stores</option>
            <option 
              v-for="store in stores"
                :key="store"
                :value="store"
            >{{ store }}</option>
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
              class="mt-2"
              @update:modelValue="onFilterChange"
          />
          <div class="flex justify-between text-sm text-gray-700 mt-2">
            <span>Min: {{ price_range[0] }}</span>
            <span>Max: {{ price_range[1] }}</span>
          </div>
        </div>
    </div>
    
  <div>
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-lg text-gray-600">Loading products...</span>
      </div>
  </div>

    <div v-if="products.length === 0" class="text-center py-12">
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
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6">
        <ProductCard
          v-for="product in products"
            :key="product.id"
            :product="product"
            @add-to-cart="onAddToCart"
            @product-detail="handleProductDetail"
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

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import NavBar from '@/components/NavBar.vue'
import ProductCard from '@/components/ProductCard.vue'
import ProductModal from '@/components/ProductModal.vue'
import '@vueform/slider/themes/default.css'
import Slider from '@vueform/slider'

const products = ref([])
const next_cursor = ref(null)
const selected_category = ref('')
const selected_store = ref('')
const price_range = ref([0,1000])
const loading = ref(false)
const allLoaded = ref(false)
const selectedProduct = ref(null)
const showModal = ref(false)
const categories = ref([])
const stores = ref([])

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

    if(selected_store.value){
      params.append('store', selected_store.value)
    }

    if(price_range.value){
      params.append('min_price', price_range.value[0])
      params.append('max_price', price_range.value[1])
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
    const storeRes = await fetch(`/api/entrepreneurs_hub/products/storefronts/`)
    const categoryRes = await fetch(`/api/entrepreneurs_hub/products/categories/`)

    stores.value = await storeRes.json()
    categories.value = await categoryRes.json()
  }
  catch(err){
    console.log("Cannot fetch categories/store : ", err)
  }
}

const onFilterChange = () => {
  products.value = []
  next_cursor.value = null
  allLoaded.value = false
  loadProducts()
}

const handleScroll = () => {
  const scrollTop = window.scrollY
  const windowHeight = window.innerHeight
  const fullHeight = document.body.offsetHeight

  if(scrollTop + windowHeight >= fullHeight - 200){
    loadProducts()
  }
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

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  loadProducts()
  fetchFilters()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

</script>
