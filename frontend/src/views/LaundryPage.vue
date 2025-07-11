<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-indigo-800 mb-2">
          <i class="fas fa-tshirt mr-3"></i>
          Laundry Service
        </h1>
        <p class="text-indigo-600">Professional cleaning at your fingertips</p>
      </div>

      <!-- Step Indicator -->
      <div class="flex justify-center mb-8">
        <div class="flex items-center space-x-4">
          <div class="flex items-center">
            <div
              :class="[
                'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium',
                currentStep.value === 'selection'
                  ? 'bg-indigo-600 text-white'
                  : currentStep.value === 'confirmation' || currentStep.value === 'invoice'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-300 text-gray-600',
              ]"
            >1</div>
            <span class="ml-2 text-sm font-medium text-gray-700">Select Items</span>
          </div>
          <div class="w-12 h-1 bg-gray-300 rounded"></div>
          <div class="flex items-center">
            <div
              :class="[
                'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium',
                currentStep.value === 'confirmation'
                  ? 'bg-indigo-600 text-white'
                  : currentStep.value === 'invoice'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-300 text-gray-600',
              ]"
            >2</div>
            <span class="ml-2 text-sm font-medium text-gray-700">Confirm Order</span>
          </div>
          <div class="w-12 h-1 bg-gray-300 rounded"></div>
          <div class="flex items-center">
            <div
              :class="[
                'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium',
                currentStep.value === 'invoice'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-300 text-gray-600',
              ]"
            >3</div>
            <span class="ml-2 text-sm font-medium text-gray-700">Invoice</span>
          </div>
        </div>
      </div>

      <!-- Item Selection Step -->
      <div v-if="currentStep.value === 'selection'" class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <i class="fas fa-list-ul mr-3 text-indigo-600"></i>
          Select Your Laundry Items
        </h2>

        <div v-if="categories.value.length === 0" class="text-center text-red-600 font-semibold">
          Loading categories from server...
        </div>

        <div class="space-y-4 mb-6" v-else>
          <div
            v-for="(item, index) in laundryItems.value"
            :key="item.id"
            class="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl p-4 border border-indigo-200"
          >
            <div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-center">
              <!-- Category -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
                <select
                  v-model="item.category"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white"
                >
                  <option v-for="category in categories.value" :key="category.name" :value="category.name">
                    {{ category.name }}
                  </option>
                </select>
              </div>

              <!-- Quantity -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Quantity</label>
                <input
                  type="number"
                  v-model.number="item.quantity"
                  min="1"
                  max="50"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>

              <!-- Services -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">Services</label>
                <div class="flex flex-col space-y-2">
                  <label class="flex items-center">
                    <input
                      type="checkbox"
                      v-model="item.wash"
                      class="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                    />
                    <span class="ml-2 text-sm text-gray-700">
                      Wash (Tk. {{ getPrice(item.category, 'wash') }} per item)
                    </span>
                  </label>
                  <label class="flex items-center">
                    <input
                      type="checkbox"
                      v-model="item.iron"
                      class="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                    />
                    <span class="ml-2 text-sm text-gray-700">
                      Iron (Tk. {{ getPrice(item.category, 'iron') }} per item)
                    </span>
                  </label>
                </div>
              </div>

              <!-- Remove Button -->
              <div class="flex justify-center">
                <button
                  @click="removeItem(item.id)"
                  v-if="laundryItems.value.length > 1"
                  class="bg-red-500 hover:bg-red-600 text-white p-2 rounded-lg transition-colors duration-200"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Item Button -->
        <button
          @click="addItem"
          class="w-full bg-gradient-to-r from-indigo-500 to-blue-600 hover:from-indigo-600 hover:to-blue-700 text-white py-3 px-4 rounded-lg font-medium transition-all duration-200 mb-6 flex items-center justify-center"
        >
          <i class="fas fa-plus mr-2"></i>
          Add Another Item
        </button>

        <!-- Notice -->
        <div
          class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 border border-green-200 mb-6 text-green-700"
        >
          <span>Final cost will be calculated after order confirmation.</span>
        </div>

        <!-- Continue Button -->
        <button
          @click="proceedToConfirmation"
          :disabled="!hasValidItems.value"
          class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 text-white py-3 px-4 rounded-lg font-medium transition-all duration-200"
        >
          Proceed to Confirmation
        </button>
      </div>

      <!-- Confirmation Step -->
      <div v-if="currentStep.value === 'confirmation'" class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <i class="fas fa-check-circle mr-3 text-green-600"></i>
          Confirm Your Order
        </h2>

        <div class="space-y-4 mb-6">
          <div v-for="item in laundryItems.value" :key="item.id" class="bg-gray-50 rounded-lg p-4 border">
            <div class="flex justify-between items-center">
              <div>
                <span class="font-medium text-gray-800">{{ item.category }}</span>
                <span class="text-gray-600 ml-2">x{{ item.quantity }}</span>
              </div>
              <div class="text-right">
                <div class="text-sm text-gray-600">
                  <span v-if="item.wash">Wash</span>
                  <span v-if="item.wash && item.iron"> + </span>
                  <span v-if="item.iron">Iron</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-indigo-50 rounded-lg p-4 mb-6 border border-indigo-200">
          <div class="flex justify-between items-center text-sm text-indigo-600 mt-1">
            <span>Estimated Delivery:</span>
            <span>{{ formatDeliveryDate() }}</span>
          </div>
        </div>

        <div class="flex space-x-4">
          <button
            @click="() => (currentStep.value = 'selection')"
            class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 px-4 rounded-lg font-medium transition-colors duration-200"
          >
            Back to Edit
          </button>
          <button
            @click="confirmOrder"
            class="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white py-3 px-4 rounded-lg font-medium transition-all duration-200"
            :disabled="submitting.value"
          >
            {{ submitting.value ? 'Submitting...' : 'Confirm Order' }}
          </button>
        </div>
      </div>

      <!-- Invoice Step -->
      <div v-if="currentStep.value === 'invoice'" class="bg-white rounded-xl shadow-lg p-6">
        <div class="text-center mb-6">
          <div
            class="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4"
          >
            <i class="fas fa-check text-2xl text-green-600"></i>
          </div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Order Confirmed!</h2>
          <p class="text-gray-600">Your laundry order has been successfully placed.</p>
        </div>

        <!-- Invoice -->
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 mb-6">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h3 class="text-xl font-bold text-gray-800">INVOICE</h3>
              <p class="text-gray-600">{{ invoiceData.value.invoiceNumber }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-600">Order Date</p>
              <p class="font-medium">{{ invoiceData.value.orderDate }}</p>
            </div>
          </div>

          <div class="border-t border-gray-200 pt-4 mb-4">
            <h4 class="font-semibold text-gray-800 mb-3">Items Ordered:</h4>
            <div class="space-y-2">
              <div
                v-for="item in invoiceData.value.items"
                :key="item.category + item.wash + item.iron"
                class="flex justify-between items-center py-2 border-b border-gray-100"
              >
                <div>
                  <span class="font-medium">{{ item.category }}</span>
                  <span class="text-gray-600 ml-2">x{{ item.quantity }}</span>
                  <div class="text-sm text-gray-500">
                    <span v-if="item.wash">Wash</span>
                    <span v-if="item.wash && item.iron"> + </span>
                    <span v-if="item.iron">Iron</span>
                  </div>
                </div>
                <span class="font-medium">Tk. {{ item.item_total }}</span>
              </div>
            </div>
          </div>

          <div class="border-t border-gray-200 pt-4">
            <div class="flex justify-between items-center text-lg font-bold">
              <span>Total Amount:</span>
              <span>Tk. {{ invoiceData.value.total }}</span>
            </div>
            <div class="flex justify-between items-center text-sm text-gray-600 mt-2">
              <span>Estimated Delivery Date:</span>
              <span class="font-medium text-indigo-600">{{ invoiceData.value.deliveryDate }}</span>
            </div>
          </div>
        </div>

        <div class="flex space-x-4">
          <button
            @click="printInvoice"
            class="flex-1 bg-indigo-500 hover:bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium transition-colors duration-200"
          >
            <i class="fas fa-print mr-2"></i>
            Print Invoice
          </button>
          <button
            @click="newOrder"
            class="flex-1 bg-green-500 hover:bg-green-600 text-white py-3 px-4 rounded-lg font-medium transition-colors duration-200"
          >
            <i class="fas fa-plus mr-2"></i>
            New Order
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const currentStep = ref('selection') // selection, confirmation, invoice
const laundryItems = ref([
  {
    id: 1,
    category: '',
    quantity: 1,
    wash: true,
    iron: false,
  },
])
const categories = ref([])
const invoiceData = ref(null)
const submitting = ref(false)

const fetchCategories = async () => {
  try {
    const resp = await axios.get('http://127.0.0.1:8000/api/laundry/categories/')
    // This is IMPORTANT: resp.data should be an array!
    // If your backend sends {categories: [...]}, use resp.data.categories
    categories.value = Array.isArray(resp.data) ? resp.data : resp.data.categories
    if (categories.value.length && !laundryItems.value[0].category) {
      laundryItems.value[0].category = categories.value[0].name
    }
  } catch (e) {
    categories.value = []
    alert('Failed to fetch laundry categories from server.')
  }
}

const addItem = () => {
  const defaultCategory = categories.value.length > 0 ? categories.value[0].name : ''
  const newItem = {
    id: Date.now(),
    category: defaultCategory,
    quantity: 1,
    wash: true,
    iron: false,
  }
  laundryItems.value.push(newItem)
}

const removeItem = (id) => {
  laundryItems.value = laundryItems.value.filter((item) => item.id !== id)
}

const formatDeliveryDate = () => {
  const deliveryDate = new Date()
  deliveryDate.setDate(deliveryDate.getDate() + 3)
  return deliveryDate.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const proceedToConfirmation = () => {
  if (hasValidItems.value) {
    currentStep.value = 'confirmation'
  }
}

const getPrice = (category, type) => {
  const cat = categories.value.find((c) => c.name === category)
  if (!cat) return 0
  return type === 'wash' ? cat.wash_price : cat.iron_price
}

const confirmOrder = async () => {
  submitting.value = true
  try {
    const orderData = {
      items: laundryItems.value.map((item) => ({
        category: item.category,
        quantity: item.quantity,
        wash: item.wash,
        iron: item.iron,
      })),
    }
    const response = await axios.post(
      'http://127.0.0.1:8000/api/laundry/orders/',
      orderData,
      { withCredentials: true }
    )
    invoiceData.value = {
      invoiceNumber: response.data.id ? 'LND-' + response.data.id : '',
      items: response.data.items,
      total: response.data.total_cost,
      deliveryDate: response.data.delivery_date,
      orderDate: response.data.order_date,
    }
    currentStep.value = 'invoice'
  } catch (error) {
    alert('Failed to place order! Please try again.')
    console.error('Error confirming order:', error)
  }
  submitting.value = false
}

const printInvoice = () => {
  window.print()
}

const newOrder = () => {
  currentStep.value = 'selection'
  laundryItems.value = [
    {
      id: Date.now(),
      category: categories.value.length > 0 ? categories.value[0].name : '',
      quantity: 1,
      wash: true,
      iron: false,
    },
  ]
  invoiceData.value = null
}

const hasValidItems = computed(() => {
  return (
    laundryItems.value.length > 0 &&
    laundryItems.value.every(
      (item) =>
        item.quantity > 0 &&
        (item.wash || item.iron) &&
        !!item.category
    )
  )
})

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
@media print {
  .min-h-screen {
    min-height: auto;
  }
  body * {
    visibility: hidden;
  }
  .invoice-section,
  .invoice-section * {
    visibility: visible;
  }
  .invoice-section {
    position: absolute;
    left: 0;
    top: 0;
  }
}
</style>
