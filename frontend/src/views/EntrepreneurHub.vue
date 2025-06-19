<template>
  <NavBar />

  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-semibold text-gray-800 mb-6">Entrepreneur Hub</h1>

    <div v-if="products.length === 0" class="text-gray-500">No products available.</div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div
        v-for="product in products"
        :key="product.product_id"
        class="bg-white rounded-xl shadow hover:shadow-md p-4 transition-all duration-300"
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
          <span class="text-gray-700 font-bold">${{ product.price }}</span>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'

const products = ref([])

onMounted(async () => {
  try {
    const res = await fetch('/api/entrepreneurs_hub/products/')
    const data = await res.json()
    if (data.success) {
      products.value = data.items
    } else {
      console.error('Error fetching products:', data.error)
    }
  } catch (err) {
    console.error('Network/API error:', err)
  }
})
</script>
