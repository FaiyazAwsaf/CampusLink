<template>
<div
    @click="$emit('product-detail', product)"
    class = "cursor-pointer"
>
    <div class="bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 flex flex-col h-full">
        <!-- Image Section (Top Half) -->
        <div class="relative h-48 bg-gray-100">
            <img
                v-if="product.image"
                :src="product.image"
                :alt="product.name"
                class="w-full h-full object-cover"
                @error="$emit('handle-image-error', product)"
            />
        <div
            v-else
            class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200"
        >
        <svg
            class="w-16 h-16 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
        >
            <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            ></path>
        </svg>
        </div>

        <!-- Availability Badge -->
        <div class="absolute top-3 right-3">
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
    </div>
        <!-- Product Info Section -->
        <div class="p-4 flex flex-col flex-1">
        <div class="flex-1">
            <!-- Product Name -->
            <h3 class="font-semibold text-gray-900 text-lg mb-2 line-clamp-2">
            {{ product.name }}
            </h3>

            <p class="text-gray-600 text-sm mb-3 line-clamp-2">
            {{ product.description }}
            </p>
        </div>

        <div>
            <!-- Price and Stock Info -->
            <div class="flex justify-between items-center mb-4">
            <span class="text-xl font-semibold text-gray-700">৳{{ product.price }}</span>
            </div>

            <!-- Add to Cart Button -->
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

</script>