<template>
    <div class="mb-8">
        <label for="category" class="block font-medium mb-1">Category:</label>
            <select :value="modelValue" @change="$emit('update:modelValue', $event.target.value); $emit('on-filter-change')" class="border p-2 rounded">
                <option value="">All</option>
                <option 
                    v-for="category in categories"
                    :key="category"
                    :value="category"
                >{{ category }}</option>
            </select>
    </div>
</template>

<script setup>

defineProps({
    categories : {
        type : Array,
        required : true,
    },

    modelValue : {
        type : String,
        default : ''
    }
})

defineEmits(['update:modelValue', 'on-filter-change'])

</script>