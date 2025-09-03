<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200">
    <NavBar />
    <div class="max-w-4xl mx-auto py-8 px-4">
      <h2 class="text-2xl font-bold mb-6 text-center">Your Cart</h2>
      <div v-if="cart.length === 0" class="text-center py-12">
        <p class="text-gray-500">Your cart is empty.</p>
      </div>
      <div v-else>
        <div v-if="cdsItems.length">
          <h3 class="text-lg font-semibold mb-2">CDS Products</h3>
          <div class="bg-white rounded shadow p-4 mb-6">
            <div
              v-for="item in cdsItems"
              :key="'cds-' + item.item_id"
              class="flex justify-between items-center border-b py-2 last:border-b-0"
            >
              <div class="flex items-center space-x-2">
                <span class="font-semibold">{{ item.name }}</span>
                <span class="text-gray-500 ml-2">Tk. {{ item.price }}</span>
              </div>
              <span class="text-gray-400 ml-2 flex items-center">
                <button
                  @click="updateCartQuantity(item.item_id, 'cds', -1)"
                  class="px-2 py-1 bg-blue-200 rounded-l hover:bg-gray-300"
                  :disabled="item.quantity <= 1"
                >
                  -
                </button>
                <span class="px-2">{{ item.quantity }}</span>
                <button
                  @click="updateCartQuantity(item.item_id, 'cds', 1)"
                  class="px-2 py-1 bg-blue-200 rounded-r hover:bg-gray-300"
                >
                  +
                </button>
              </span>
              <button
                @click="removeFromCart(item.item_id, 'cds')"
                class="text-red-500 hover:underline"
              >
                Remove
              </button>
            </div>
            <div class="flex justify-end mt-2">
              <span class="font-bold text-lg">Total: Tk. {{ cdsTotal.toFixed(2) }}</span>
            </div>
            <div class="mt-4 flex justify-end">
              <button
                @click="showCdsOrder = true"
                class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Confirm Order
              </button>
            </div>
          </div>
        </div>
        <div v-if="entrepreneurItems.length">
          <h3 class="text-lg font-semibold mb-2">Entrepreneur Hub Products</h3>
          <div class="bg-white rounded shadow p-4 mb-6">
            <div
              v-for="item in entrepreneurItems"
              :key="'ent-' + item.item_id"
              class="flex justify-between items-center border-b py-2 last:border-b-0"
            >
              <div>
                <span class="font-semibold">{{ item.name }}</span>
                <span class="text-gray-500 ml-2">Tk. {{ item.price }}</span>
              </div>
              <button
                @click="removeFromCart(item.item_id, 'entrepreneur')"
                class="text-red-500 hover:underline"
              >
                Remove
              </button>
            </div>
            <div class="mt-4 flex justify-end">
              <button
                @click="showEntOrder = true"
                class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Confirm Order
              </button>
            </div>
          </div>
        </div>
        <div class="flex justify-end mt-6">
          <button
            @click="clearCart"
            class="bg-red-500 text-white px-4 py-2 rounded hover:bg-gray-400"
          >
            Clear Cart
          </button>
        </div>
      </div>

      <!-- CDS Order Modal -->
      <div v-if="showCdsOrder" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="absolute inset bg-opacity-40 backdrop-blur-sm"></div>
        <div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full relative z-10">
          <button
            @click="showCdsOrder = false"
            class="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
          >
            &times;
          </button>
          <h3 class="text-lg font-bold mb-4">CDS Order Payment</h3>
          <p class="mb-2">Choose payment method:</p>
          <div class="flex space-x-4 mb-4">
            <button
              @click="paymentMethod = 'cash'"
              :class="paymentMethod === 'cash' ? 'bg-blue-600 text-white' : 'bg-gray-200'"
              class="px-4 py-2 rounded"
            >
              Cash on Pick Up
            </button>
            <button
              @click="paymentMethod = 'bkash'"
              :class="paymentMethod === 'bkash' ? 'bg-blue-600 text-white' : 'bg-gray-200'"
              class="px-4 py-2 rounded"
            >
              bKash
            </button>
          </div>
          <div class="mb-4 flex justify-end">
            <span class="font-bold text-lg">Total: Tk. {{ cdsTotal }}</span>
          </div>

          <div v-if="paymentMethod === 'bkash'" class="mb-4">
            <p class="mb-2">Scan the QR code or use the number below to pay:</p>
            <img src="" alt="bKash QR" class="w-40 h-40 mx-auto mb-2" />
            <p class="text-center font-semibold">bKash Number: 01XXXXXXXXX</p>
          </div>
          <div class="flex justify-end">
            <button
              @click="confirmOrder('cds')"
              class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              Confirm & Place Order
            </button>
          </div>
        </div>
      </div>

      <!-- Entrepreneur Order Modal (simplified) -->
      <div
        v-if="showEntOrder"
        class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
      >
        <div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full relative">
          <button
            @click="showEntOrder = false"
            class="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
          >
            &times;
          </button>
          <h3 class="text-lg font-bold mb-4">Entrepreneur Hub Order</h3>
          <p>Order confirmation for Entrepreneur Hub products coming soon.</p>
          <div class="flex justify-end mt-4">
            <button
              @click="showEntOrder = false"
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import useCart from '@/utils/useCart.js'
import axios from 'axios'
import { ref } from 'vue'
import { computed } from 'vue'

const { cart, cdsItems, entrepreneurItems, removeFromCart, clearCart, updateCartQuantity } =
  useCart()

const showCdsOrder = ref(false)
const showEntOrder = ref(false)
const paymentMethod = ref('cash')
const cdsInvoice = ref(null)

const cdsTotal = computed(() => {
  return cdsItems.value.reduce((sum, item) => sum + item.price * (item.quantity || 1), 0)
})

async function confirmOrder(type) {
  try {
    if (type === 'cds') {
      const orderDetails = {
        items: cdsItems.value.map((item) => ({
          item_id: item.item_id,
          quantity: item.quantity || 1,
        })),
        payment_method: paymentMethod.value,
        delivery_status: 'preparing',
      }
      const response = await axios.post('/api/cds/submit_order/', orderDetails)
      if (response.data.success) {
        // Try to get invoice/order details (if not already in response)
        let invoiceData = response.data.invoice || response.data.order || null
        if (!invoiceData && response.data.order_number) {
          // Try to fetch order details by order_number
          try {
            const detailsResp = await axios.get(
              `/api/cds/orders/${encodeURIComponent(response.data.order_number)}/`,
            )
            invoiceData = detailsResp.data
          } catch (err) {
            // fallback: use what we have
            invoiceData = {
              order_number: response.data.order_number,
              items: cdsItems.value.map((item) => ({
                name: item.name,
                quantity: item.quantity || 1,
                price: item.price,
              })),
              total_amount: response.data.total_amount,
              status: response.data.status || 'preparing',
              created_at: response.data.created_at || new Date().toISOString(),
            }
          }
        }
        cdsInvoice.value = invoiceData
        clearCart()
        showCdsOrder.value = false
      } else {
        // Optionally show error in UI
        cdsInvoice.value = {
          error: response.data.error || 'Unknown error',
        }
      }
    } else if (type === 'entrepreneur') {
      // Handle Entrepreneur Hub order confirmation logic here
      showEntOrder.value = false
    }
  } catch (error) {
    // Optionally show error in UI
    cdsInvoice.value = {
      error: error.response?.data?.error || error.message,
    }
    console.error('Error confirming order:', error)
  }
}
</script>

<style scoped>
.fixed {
  position: fixed;
}
.inset-0 {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
.z-50 {
  z-index: 50;
}
</style>
