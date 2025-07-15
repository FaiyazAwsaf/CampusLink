<template>

  <div class="fixed inset-0 bg-black bg-opacity-20 z-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg max-w-5xl w-full relative shadow-lg">
      <button class="absolute top-3 right-3 text-gray-500 hover:text-black" @click="$emit('close')">✕</button>
      
      <div class="grid md:grid-cols-2 gap-6">
        <div>
          <img
            v-if="product.image"
            :src="product.image"
            alt="Product Image"
            class="w-full h-auto rounded shadow"
            @error="handleImageError"
          />
        </div>
        <div>
          <h2 class="text-2xl font-bold mb-2">{{ product.name }}</h2>
          <p class="text-gray-700 mb-4">{{ product.description }}</p>
          <div class="text-xl font-semibold text-gray-700 mb-4">৳{{ product.price }}</div>
          
            <div class="mb-4">
              <span
                  v-if="product.availability"
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
              <button
                :disabled="!product.availability"
                :class="[
                    'w-full py-2 px-4 rounded-lg font-semibold transition-all duration-200',
                    product.availability
                    ? 'bg-gray-700 hover:bg-gray-800 text-white hover:shadow-md'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed',
                ]"
                @click="$emit('add-to-cart', product)"
                > 
                  <span v-if="product.availability">Add to Cart</span>
                  <span v-else>Out of Stock</span>
              </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product:{
    type:Object,
    required:true,
  },
})

function handleImageError(event) {
  event.target.src = '/Default.jpg'
}
</script>