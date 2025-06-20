<template>
  <NavBar />

  <div class="container mx-auto px-4 py-8">

    <div class="mb-4">
      <label for="category" class="block font-medium mb-1">Category:</label>
        <select v-model="selected_category" @change="onFilterChange" class="border p-2 rounded">
          <option value="">All</option>
          <option value="Clothing">Clothing</option>
          <option value="Gadgets">Gadgets</option>
          <option value="Food">Food</option>
    <!-- Add your categories -->
        </select>
    </div>

    <div v-if="products.length === 0" class="text-gray-500">No products available.</div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6">
      <div
        v-for="product in products"
        :key="product.product_id"
        class="bg-white rounded-xl shadow-xl hover:shadow-2xl p-4 transition-all duration-300"
      >
        <div class="mb-4">
            <img
                :src = "product.image || '/Default.jpg'"
                alt = "Product Image"
                class = "w-full h-48 object-cover rounded-lg mb-4"
            />
          <h2 class="text-xl font-semibold text-gray-900">{{ product.name }}</h2>
          <p class="text-gray-600 text-sm">{{ product.description }}</p>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-gray-700 font-bold">BDT {{ product.price }}</span>
          <span
            class="text-sm font-medium"
            :class="product.availability ? 'text-green-600' : 'text-red-500'"
          >
            {{ product.availability ? 'Available' : 'Out of Stock' }}
          </span>
        </div>
      </div>
    </div>
  </div>

  <div class="text-center mt-6">
    <span v-if="loading" class="text-gray-500">Loading more products...</span>
    <span v-else-if="allLoaded" class="text-gray-400">No more products.</span>
  </div>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import NavBar from '@/components/NavBar.vue'

const products = ref([])
const page = ref(1)
const selected_category = ref("")
const limit = 10
const loading = ref(false)
const all_loaded = ref(false)

const loadProducts = async () => {

  if(loading.value || all_loaded.value) 
    return loading.value = true

  try {

    const params = new URLSearchParams({
      page : page.value,
      limit : limit
    })

    if(selected_category.value){
      params.append('category', selected_category.value)
    }

    const res = await fetch(`/api/entrepreneurs_hub/products/?${params.toString()}`)
    const data = await res.json()

    if (data.success) {
      if(data.items.length < limit){
        all_loaded.value = true
      }

      products.value.push(...data.items)
      page.value += 1
    } 
    else {
      console.error('Error fetching products:', data.error)
    }
  } catch (err) {
    console.error('Network/API error:', err)
  }
}

const onFilterChange = () => {
  page.value = 1
  products.value = []
  all_loaded.value = false
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

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  loadProducts()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

</script>
