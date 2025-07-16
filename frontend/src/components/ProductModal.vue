<template>

  <div class="fixed inset-0 bg-black/50 z-60 flex items-center justify-center">

    <div class="bg-white p-6 rounded-xl max-w-5xl w-full relative shadow-xl animate-fadeIn">
      

      <button
        class="absolute top-4 right-4 text-gray-500 hover:text-black text-2xl"
        @click="$emit('close')"
      >
        ✕
      </button>


      <div class="grid md:grid-cols-2 gap-8 m-4">

        <div>
          <img
            v-if="product.image"
            :src="product.image"
            alt="Product Image"
            class="w-full h-full rounded-lg shadow-md"
            @error="handleImageError"
          />
        </div>

        <div class="flex flex-col h-full">
          <div class="flex-1">
            <h2 class="text-3xl font-bold mb-3">{{ product.name }}</h2>
            <p class="text-gray-700 mb-4">{{ product.description }}</p>
            <div class="text-2xl font-semibold text-gray-800 mb-4">৳{{ product.price }}</div>
            <div class="text-xl font-medium text-gray-800 mb-4">
              <span
                v-if="product.availability"
              >
                In Stock
              </span>
              <span
                v-else
              >
                Out of Stock
              </span>
            </div>
          </div>

          <div class="mt-auto space-y-3">
            <div class="bg-gray-100 rounded-lg px-4 py-3 text-gray-800 font-medium shadow-sm border border-gray-200">
              <span class="block">
                <span class="font-semibold text-gray-600">Storefront:</span> {{ product.store_name }}
              </span>
            </div>

            <div class="bg-gray-100 rounded-lg px-4 py-3 text-gray-800 font-medium shadow-sm border border-gray-200">
              <span class="block">
                <span class="font-semibold text-gray-600">Category:</span> {{ product.category }}
              </span>
            </div>

            <button
              :disabled="!product.availability"
              :class="[ 
                'w-full py-3 px-4 rounded-lg font-semibold transition-all duration-200',
                product.availability
                  ? 'bg-gray-800 hover:bg-gray-900 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
              @click="$emit('add-to-cart', product)"
            >
              {{ product.availability ? 'Add to Cart' : 'Out of Stock' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  product: Object,
})

function handleImageError(event) {
  event.target.src = '/Default.jpg'
}
</script>

<style scoped>
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}
</style>