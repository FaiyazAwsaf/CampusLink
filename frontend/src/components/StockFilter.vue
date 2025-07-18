<template>
    <div class="mb-8">

          <label for="stock" class="block font-medium mb-1">Stock</label>

              <label
                v-for="option in availabilityOptions"
                :key="option.value"
                class="flex items-center cursor-pointer group"
              >
                <input
                  type="radio"
                  :value="option.value"
                  :checked="modelValue === option.value"
                  @change="$emit('update:modelValue', $event.target.value); $emit('on-filter-change')"
                  class="sr-only"
                />
                <div class="relative">
                  <div class="w-5 h-5 rounded-full border-2 border-gray-300 group-hover:border-blue-400 transition-colors duration-200"
                    :class="modelValue === option.value ? 'border-gray-700 bg-gray-700' : ''"
                  >
                    <div
                      v-if="modelValue === option.value"
                      class="absolute inset-0 flex items-center justify-center">
                        <div class="w-2 h-2 rounded-full bg-white"></div>
                    </div>
                  </div>
                </div>
                <span class="ml-3 text-gray-700 group-hover:text-gray-900 transition-colors duration-200">
                  {{ option.label }}
                </span>
              </label>

        </div>
</template>

<script setup>
defineProps({
    availabilityOptions : {
        type : Array,
        required : true,
    },

    modelValue : {
        type : String,
        default : '',
    }
})

</script>