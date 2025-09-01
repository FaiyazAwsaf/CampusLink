<template>
  <NavBar />
  <div
    class="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-xl shadow bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200"
  >
    <h2 class="text-2xl font-bold mb-4 text-center text-indigo-800">Laundry Service</h2>

    <!-- Add Item Form -->
    <div class="bg-indigo-50 p-4 rounded-lg mb-6">
      <h3 class="text-lg font-semibold mb-3 text-indigo-700">Add Laundry Item</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Cloth Category -->
        <div>
          <label for="clothType" class="block mb-1 font-medium">Cloth Category</label>
          <select
            id="clothType"
            v-model="currentItem.category"
            class="w-full rounded border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200"
          >
            <option value="" disabled>Select cloth type</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <!-- Quantity -->
        <div>
          <label for="quantity" class="block mb-1 font-medium">Quantity</label>
          <input
            id="quantity"
            v-model.number="currentItem.quantity"
            type="number"
            min="1"
            class="w-full rounded border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200"
            placeholder="Enter quantity"
          />
        </div>

        <!-- Service Type -->
        <div>
          <span class="block mb-1 font-medium">Service Type</span>
          <div class="flex items-center space-x-4">
            <label class="inline-flex items-center">
              <input type="checkbox" v-model="currentItem.wash" class="text-indigo-600" />
              <span class="ml-1">Wash</span>
            </label>
            <label class="inline-flex items-center">
              <input type="checkbox" v-model="currentItem.ironing" class="text-indigo-600" />
              <span class="ml-1">Ironing</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Add Item Button -->
      <button
        @click="addItemToOrder"
        type="button"
        class="mt-4 bg-indigo-600 text-white rounded-lg py-2 px-4 font-semibold hover:bg-indigo-700 transition"
        :disabled="!isValidItem"
      >
        Add to Order
      </button>
    </div>

    <!-- Order Items List -->
    <div v-if="orderItems.length > 0" class="mb-6">
      <h3 class="text-lg font-semibold mb-3 text-indigo-700">Order Items</h3>
      <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Item
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Quantity
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Services
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Price
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(item, index) in orderItems" :key="index">
              <td class="px-6 py-4 whitespace-nowrap">{{ getCategoryName(item.category) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ item.quantity }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="item.wash && item.ironing">Wash & Ironing</span>
                <span v-else-if="item.wash">Wash</span>
                <span v-else-if="item.ironing">Ironing</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">Tk. {{ item.subtotal }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button @click="removeItem(index)" class="text-red-600 hover:text-red-900">
                  Remove
                </button>
              </td>
            </tr>
          </tbody>
          <tfoot class="bg-gray-50">
            <tr>
              <td colspan="3" class="px-6 py-3 text-right font-medium">Total:</td>
              <td class="px-6 py-3 font-bold">Tk. {{ totalOrderAmount }}</td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>

      <!-- Generate Invoice Button -->
      <button
        @click="generateInvoice"
        class="mt-4 w-full bg-green-600 text-white rounded-lg py-2 font-semibold hover:bg-green-700 transition"
      >
        Confirm Order & Generate Invoice
      </button>
    </div>

    <!-- Invoice Section -->
    <div v-if="invoiceGenerated" class="mt-6 p-6 rounded-lg bg-blue-50 border border-blue-200">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-bold text-blue-900">Invoice</h3>
        <span class="text-sm bg-blue-200 text-blue-800 py-1 px-3 rounded-full">
          {{ invoice.invoice_number }}
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <p class="text-sm text-gray-600">Order Date</p>
          <p class="font-medium">{{ formatDate(invoice.created_at) }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-600">Estimated Delivery Date</p>
          <p class="font-medium">{{ formatDate(invoice.estimated_delivery_date) }}</p>
        </div>
      </div>

      <div class="border-t border-b border-gray-200 py-4 my-4">
        <h4 class="font-semibold mb-2">Order Items</h4>
        <div v-for="(item, index) in invoice.items" :key="index" class="flex justify-between py-2">
          <div>
            <span class="font-medium">{{ getCategoryName(item.category) }}</span>
            <span class="text-gray-600 ml-2">
              ({{ item.quantity }} ×
              <span v-if="item.wash && item.ironing">Wash & Ironing</span>
              <span v-else-if="item.wash">Wash</span>
              <span v-else-if="item.ironing">Ironing</span>)
            </span>
          </div>
          <span>Tk. {{ item.subtotal }}</span>
        </div>
      </div>

      <div class="flex justify-between font-bold text-lg mt-4">
        <span>Total Amount:</span>
        <span>Tk. {{ invoice.total_amount }}</span>
      </div>

      <div class="mt-6 text-center">
        <p class="text-gray-600">Thank you for using our laundry service!</p>
        <p class="text-sm text-gray-500 mt-1">Your order status: {{ invoice.status }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { AuthService } from '@/utils/auth.js'

const router = useRouter()

const categories = ref([])
const currentItem = ref({})
const orderItems = ref([])
const invoiceGenerated = ref(false)
const invoice = ref(null)

// Computed properties
const isValidItem = computed(() => {
  return (
    currentItem.value.category &&
    currentItem.value.quantity > 0 &&
    (currentItem.value.wash || currentItem.value.ironing)
  )
})

const totalOrderAmount = computed(() => {
  return orderItems.value.reduce((total, item) => total + item.subtotal, 0)
})

// Methods
async function fetchCategories() {
  try {
    const response = await axios.get('/api/laundry/categories/')
    categories.value = response.data
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}
const categoryNameById = computed(() => {
  const map = Object.create(null)
  for (const c of categories?.value || []) {
    if (c && c.id != null) map[c.id] = c.name || ''
  }
  return map
})

function getCategoryName(categoryValue) {
  if (categoryValue === undefined || categoryValue === null || categoryValue === '') return ''
  if (typeof categoryValue === 'string') return categoryValue
  return categoryNameById.value[categoryValue] || ''
}

function calculateItemSubtotal(item) {
  const category = categories.value.find((c) => c.id === item.category)
  if (!category) return 0

  let subtotal = 0
  if (item.wash) subtotal += category.wash_price * item.quantity
  if (item.ironing) subtotal += category.ironing_price * item.quantity

  return subtotal
}

function addItemToOrder() {
  if (!isValidItem.value) return

  const newItem = { ...currentItem.value }
  newItem.subtotal = calculateItemSubtotal(newItem)

  orderItems.value.push(newItem)

  // Reset current item
  currentItem.value = {
    category: '',
    quantity: 1,
    wash: false,
    ironing: false,
    subtotal: 0,
  }
}

function removeItem(index) {
  orderItems.value.splice(index, 1)
}

function generateInvoice() {
  if (orderItems.value.length === 0) {
    alert('Please add at least one item to your order.')
    return
  }

  try {
    const orderData = {
      items: orderItems.value.map((item) => ({
        category: item.category,
        quantity: item.quantity,
        wash: item.wash,
        ironing: item.ironing,
        subtotal: item.subtotal,
      })),
      total_amount: totalOrderAmount.value,
    }

    axios
      .post('/api/laundry/orders/create/', orderData)
      .then(async (response) => {
        const created = response.data || {}
        // Fetch full order details (includes items)
        try {
          const detailsResp = await axios.get(
            `/api/laundry/orders/${encodeURIComponent(created.invoice_number)}/`,
          )
          const details = detailsResp.data || {}

          invoice.value = {
            invoice_number: created.invoice_number,
            items: details.items || [],
            total_amount: created.total_amount,
            total_items: created.total_items,
            status: created.status,
            estimated_delivery_date: created.estimated_delivery_date,
            created_at: created.created_at,
          }

          invoiceGenerated.value = true
          orderItems.value = []
        } catch (err) {
          console.error('Error fetching order details:', err)
          alert('Order created, but failed to load details. Please refresh and try again.')
        }
      })
      .catch((error) => {
        console.error('Error generating invoice:', error)
        alert('Failed to generate invoice. Please try again.')
      })
  } catch (error) {
    console.error('Error generating invoice:', error)
  }
}

function formatDate(date) {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
onMounted(async () => {
  // Verify auth; if not logged in, send to login page
  try {
    if (!AuthService.isAuthenticated()) {
      router.push({ name: 'login', query: { next: '/laundry' } })
      return
    }
    await fetchCategories()
  } catch (error) {
    router.push({ name: 'login', query: { next: '/laundry' } })
  }
})
</script>
