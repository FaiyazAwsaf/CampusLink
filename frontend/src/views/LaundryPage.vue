<template>
  <NavBar />
  <div class="max-w-xl mx-auto mt-10 p-6 bg-white rounded-xl shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">Laundry Service</h2>

    <!-- Laundry Form -->
    <form @submit.prevent="generateInvoice" class="space-y-4">
      <!-- Cloth Category -->
      <div>
        <label for="clothType" class="block mb-1 font-medium">Cloth Category</label>
        <select id="clothType" v-model="clothType" class="w-full rounded border-gray-300">
          <option value="" disabled>Select cloth type</option>
          <option value="Shirt">Shirt</option>
          <option value="Pant">Pant</option>
          <option value="Bedsheet">Bedsheet</option>
          <option value="Towel">Towel</option>
          <!-- Add more as needed -->
        </select>
      </div>

      <!-- Quantity -->
      <div>
        <label for="quantity" class="block mb-1 font-medium">Number of Clothes</label>
        <input
          id="quantity"
          v-model.number="quantity"
          type="number"
          min="1"
          class="w-full rounded border-gray-300"
          placeholder="Enter quantity"
        />
      </div>

      <!-- Service Type -->
      <div>
        <span class="block mb-1 font-medium">Service Type</span>
        <label class="inline-flex items-center mr-4">
          <input type="checkbox" value="Wash" v-model="services" class="mr-1" /> Wash
        </label>
        <label class="inline-flex items-center mr-4">
          <input type="checkbox" value="Ironing" v-model="services" class="mr-1" /> Ironing
        </label>
      </div>

      <button
        type="submit"
        class="w-full bg-blue-600 text-white rounded-lg py-2 font-semibold mt-2 hover:bg-blue-700 transition"
      >
        Generate Invoice
      </button>
    </form>

    <!-- Invoice Section -->
    <div v-if="invoiceGenerated" class="mt-6 p-4 rounded bg-blue-50 border border-blue-200">
      <h3 class="text-lg font-semibold mb-2 text-blue-900">Invoice</h3>
      <p><strong>Cloth Category:</strong> {{ clothType }}</p>
      <p><strong>Quantity:</strong> {{ quantity }}</p>
      <p><strong>Service(s):</strong> {{ services.join(', ') }}</p>
      <p><strong>Total:</strong> Tk. {{ totalCost }}</p>
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import { ref } from 'vue'

// State
const clothType = ref('')
const quantity = ref(1)
const services = ref([])
const invoiceGenerated = ref(false)
const totalCost = ref(0)

// Sample pricing logic
const pricing = {
  Shirt: { Wash: 30, Ironing: 20 },
  Pant: { Wash: 35, Ironing: 25 },
  Bedsheet: { Wash: 50, Ironing: 30 },
  Towel: { Wash: 20, Ironing: 10 },
}

function generateInvoice() {
  if (!clothType.value || quantity.value < 1 || services.value.length === 0) {
    alert('Please fill out all fields and select at least one service.')
    return
  }

  let cost = 0
  for (const service of services.value) {
    cost += (pricing[clothType.value][service] || 0) * quantity.value
  }
  totalCost.value = cost
  invoiceGenerated.value = true
}
</script>
