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
              <div>
                <span class="font-semibold">{{ item.name }}</span>
                <span class="text-gray-500 ml-2">Tk. {{ item.price }}</span>
              </div>
              <button
                @click="removeFromCart(item.item_id, 'cds')"
                class="text-red-500 hover:underline"
              >
                Remove
              </button>
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
            class="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400"
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
import { ref } from 'vue'

const { cart, cdsItems, entrepreneurItems, removeFromCart, clearCart } = useCart()

const showCdsOrder = ref(false)
const showEntOrder = ref(false)
const paymentMethod = ref('cash')

function confirmOrder(type) {
  alert('Order placed! (Demo only)')
  clearCart()
  showCdsOrder.value = false
  showEntOrder.value = false
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
