<template>
    <div class="mb-8">
        <label for="pricefilter" class="block front-medium mb-1">Price</label>
            <select 
                :value="modelValue" 
                @change="$emit('update:modelValue', $event.target.value);
                         $emit('on-filter-change')"
                class="border p-2 rounded">
                <option value="">Default (Newest First)</option>
                <option value="-price">High to Low</option>
                <option value="price">Low to high</option>
            </select>

    </div>
</template>

<script setup>
defineProps({
    modelValue : {
        type : String,
        default : '',
    }
})


defineEmits(['update:modelValue', 'on-filter-change'])
</script>
