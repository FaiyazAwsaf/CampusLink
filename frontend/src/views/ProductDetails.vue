<template>
  <NavBar />

  <div class="container mx-auto px-4 py-8">
    <!-- 1. Loading spinner -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-lg text-gray-600">Loading products...</span>
    </div>

    <!-- 2. Product details (only show when product is ready) -->
    <div
      v-else-if="product"
      class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 items-start"
    >
      <!-- left column: image -->
      <div>
        <img
          v-if="product.image"
          :src="product.image"
          :alt="product.name"
          class="w-full h-auto rounded-xl shadow-md object-cover"
          @error="handleImageError"
        />
      </div>

      <!-- right column: text + actions -->
      <div>
        <h1 class="text-3xl font-bold mb-2">{{ product.name }}</h1>
        <p class="text-gray-600 mb-4">{{ product.description }}</p>

        <div class="text-2xl font-semibold text-green-700 mb-4">
          ৳{{ product.price }}
        </div>

        <div class="mb-4">
          <span
            :class="product.availability ? 'text-green-600' : 'text-red-600'"
            class="text-sm font-medium"
            >{{ product.availability ? 'In Stock' : 'Out of Stock' }}</span
          >
        </div>

        <div class="flex gap-4">
          <button
            :disabled="!product.availability"
            class="px-6 py-2 rounded-lg text-white font-semibold transition
                   disabled:bg-gray-400
                   bg-blue-600 hover:bg-blue-700"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>

    <!-- 3. Error / not found -->
    <div v-else class="text-center text-red-600 py-12">
      Couldn’t load this product.
    </div>
  </div>
</template>


<script setup>
    import {ref, onMounted } from 'vue'
    import { useRoute } from 'vue-router'
    import NavBar from '@/components/NavBar.vue'

    const product = ref(null)
    const loading = ref(true)
    const route = useRoute()

    const fetchProduct = async() => {
        try{
            const res = await fetch(`/api/entrepreneurs_hub/products/${route.params.id}/`)

            if(!res.ok){
                throw new Error('Failed to fetch product')
            }

            product.value = await res.json()
        }
        catch (err) {
            console.log('Error loading product details : ', err)
        }
        finally{
            loading.value = false
        }
    }

    onMounted(()=>{
        fetchProduct()
    })


    const handleImageError = (event) =>{
        event.target.src = '/Default.jpg'
    }
</script>