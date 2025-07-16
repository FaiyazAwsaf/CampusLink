<template>
    <button
        :disabled="!product.availability"
        :class="[
            'w-full py-2 px-4 rounded-lg font-semibold transition-all duration-200',
            product.availability
            ? 'bg-gray-700 hover:bg-gray-800 text-white hover:shadow-md'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed',
        ]"
        >
        <span v-if="product.availability">Add to Cart</span>
        <span v-else>Out of Stock</span>
    </button>
</template>


<script setup>
    defineProps({
        product : {
            type : Object,
            required : true,
        },
    })
</script>