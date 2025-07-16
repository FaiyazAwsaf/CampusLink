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
          </div>

          <div class="mt-auto space-y-3">
            <div>
              <span class="w-full py-3 px-4 rounded-lg font-semibold transition-all duration-200">
                Storefront : {{product.store_name}}
              </span>
            </div>

              <div>
              <span class="w-full py-3 px-4 rounded-lg font-semibold transition-all duration-200">
                Category : {{product.category}}
              </span>

            </div>
            <div>
              <span
                v-if="product.availability"
                class="bg-green-500 text-white text-xs font-semibold px-3 py-1 rounded-full"
              >
                In Stock
              </span>
              <span
                v-else
                class="bg-red-500 text-white text-xs font-semibold px-3 py-1 rounded-full"
              >
                Out of Stock
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