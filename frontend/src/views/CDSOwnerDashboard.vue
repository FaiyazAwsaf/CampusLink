<template>
  <div class="container mx-auto py-8">
    <div class="mb-6 flex items-center">
      <button @click="navigateToLanding" class="mr-4 p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
      </button>
      <h1 class="text-2xl font-bold">CDS Owner Dashboard</h1>
    </div>

    <div v-if="error" class="mb-4 text-red-600">{{ error }}</div>
    <div v-if="successMessage" class="mb-4 text-green-600">{{ successMessage }}</div>

    <!-- Navigation Tabs -->
    <div class="mb-6">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button 
            @click="currentView = 'items'"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
              currentView === 'items' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Manage Items
          </button>
          <button 
            @click="currentView = 'orders'"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
              currentView === 'orders' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            View Orders
          </button>
        </nav>
      </div>
    </div>

    <!-- Items Management View -->
    <div v-if="currentView === 'items'">
      <div class="mb-6 flex justify-between items-center">
        <h2 class="text-xl font-semibold">CDS Items</h2>
        <button @click="showCreateItemForm = true" class="bg-green-600 text-white px-4 py-2 rounded">
          Add New Item
        </button>
      </div>

      <!-- Create Item Form -->
      <div v-if="showCreateItemForm" class="mb-8 p-4 border rounded bg-gray-50">
        <h3 class="text-lg font-semibold mb-4">Create New Item</h3>
        <form @submit.prevent="createItem">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Item Name (max 100 characters)</label>
              <input v-model="itemForm.name" maxlength="100" class="border px-3 py-2 w-full rounded" required />
              <div class="text-xs text-gray-500 mt-1">{{ itemForm.name.length }}/100 characters</div>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Category (max 100 characters)</label>
              <input v-model="itemForm.category" maxlength="100" class="border px-3 py-2 w-full rounded" required />
              <div class="text-xs text-gray-500 mt-1">{{ itemForm.category.length }}/100 characters</div>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Price (৳)</label>
              <input v-model.number="itemForm.price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Availability</label>
              <select v-model="itemForm.availability" class="border px-3 py-2 w-full rounded">
                <option :value="true">Available</option>
                <option :value="false">Unavailable</option>
              </select>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Description (max 500 characters)</label>
            <textarea v-model="itemForm.description" maxlength="500" class="border px-3 py-2 w-full rounded" rows="3" required></textarea>
            <div class="text-xs text-gray-500 mt-1">{{ itemForm.description.length }}/500 characters</div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Image URL</label>
            <input v-model="itemForm.image" class="border px-3 py-2 w-full rounded" />
          </div>
          <div class="flex gap-2">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Create Item</button>
            <button type="button" @click="resetItemForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>

      <!-- Edit Item Form -->
      <div v-if="showEditItemForm" class="mb-8 p-4 border rounded bg-yellow-50 edit-item-form">
        <h3 class="text-lg font-semibold mb-4 text-yellow-800">Edit Item</h3>
        <form @submit.prevent="updateItem">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Item Name (max 100 characters)</label>
              <input v-model="itemForm.name" maxlength="100" class="border px-3 py-2 w-full rounded" required />
              <div class="text-xs text-gray-500 mt-1">{{ itemForm.name.length }}/100 characters</div>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Category (max 100 characters)</label>
              <input v-model="itemForm.category" maxlength="100" class="border px-3 py-2 w-full rounded" required />
              <div class="text-xs text-gray-500 mt-1">{{ itemForm.category.length }}/100 characters</div>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Price (৳)</label>
              <input v-model.number="itemForm.price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Availability</label>
              <select v-model="itemForm.availability" class="border px-3 py-2 w-full rounded">
                <option :value="true">Available</option>
                <option :value="false">Unavailable</option>
              </select>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Description (max 500 characters)</label>
            <textarea v-model="itemForm.description" maxlength="500" class="border px-3 py-2 w-full rounded" rows="3" required></textarea>
            <div class="text-xs text-gray-500 mt-1">{{ itemForm.description.length }}/500 characters</div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Image URL</label>
            <input v-model="itemForm.image" class="border px-3 py-2 w-full rounded" />
          </div>
          <div class="flex gap-2">
            <button type="submit" class="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700">Update Item</button>
            <button type="button" @click="resetItemForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>

      <!-- Items Table -->
      <div v-if="isLoading" class="mb-4">Loading items...</div>
      <div v-if="items.length === 0 && !isLoading" class="text-center py-12">
        <div class="text-gray-600 mb-4">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No items yet</h3>
        <p class="text-gray-600 mb-4">Get started by creating your first CDS item.</p>
        <button @click="showCreateItemForm = true" class="bg-green-600 text-white px-6 py-3 rounded-lg">
          Create Your First Item
        </button>
      </div>
      <div v-else>
        <table class="min-w-full border rounded-lg overflow-hidden">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-3 text-left">Name</th>
              <th class="px-4 py-3 text-left">Category</th>
              <th class="px-4 py-3 text-left">Price</th>
              <th class="px-4 py-3 text-left">Availability</th>
              <th class="px-4 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.item_id" class="border-t">
              <td class="px-4 py-3">{{ item.name }}</td>
              <td class="px-4 py-3">{{ item.category }}</td>
              <td class="px-4 py-3">৳{{ item.price }}</td>
              <td class="px-4 py-3">
                <span :class="item.availability ? 'text-green-600' : 'text-red-600'">
                  {{ item.availability ? 'Available' : 'Unavailable' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button @click="editItem(item)" class="bg-yellow-500 text-white px-3 py-1 rounded text-sm hover:bg-yellow-600">Edit</button>
                  <button @click="deleteItem(item.item_id, item.name)" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Orders Management View -->
    <div v-if="currentView === 'orders'">
      <div class="mb-6 flex justify-between items-center">
        <h2 class="text-xl font-semibold">All CDS Orders</h2>
        <button @click="fetchOrders" class="bg-blue-600 text-white px-4 py-2 rounded">
          Refresh Orders
        </button>
      </div>

      <!-- Orders Table -->
      <div v-if="isLoading" class="mb-4">Loading orders...</div>
      <div v-if="orders.length === 0 && !isLoading" class="text-center py-12">
        <div class="text-gray-600 mb-4">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No orders yet</h3>
        <p class="text-gray-600">Orders placed by customers will appear here.</p>
      </div>
      <div v-else>
        <table class="min-w-full border rounded-lg overflow-hidden">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-3 text-left">Order #</th>
              <th class="px-4 py-3 text-left">Customer</th>
              <th class="px-4 py-3 text-left">Items</th>
              <th class="px-4 py-3 text-left">Total</th>
              <th class="px-4 py-3 text-left">Payment</th>
              <th class="px-4 py-3 text-left">Status</th>
              <th class="px-4 py-3 text-left">Order Date</th>
              <th class="px-4 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.order_id" class="border-t">
              <td class="px-4 py-3">#{{ order.order_id }}</td>
              <td class="px-4 py-3">
                <div>{{ order.user_name }}</div>
                <div class="text-sm text-gray-500">{{ order.user_email }}</div>
              </td>
              <td class="px-4 py-3">{{ order.items_count }}</td>
              <td class="px-4 py-3">৳{{ order.total_amount }}</td>
              <td class="px-4 py-3">
                <span class="capitalize">{{ order.payment_method }}</span>
              </td>
              <td class="px-4 py-3">
                <select 
                  :value="order.delivery_status" 
                  @change="updateOrderStatus(order.order_id, $event.target.value)"
                  :class="getStatusColor(order.delivery_status)"
                  class="px-3 py-1 rounded text-sm font-medium"
                >
                  <option value="preparing">Preparing</option>
                  <option value="ready">Ready</option>
                </select>
              </td>
              <td class="px-4 py-3">{{ formatDate(order.created_at) }}</td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button @click="viewOrderDetails(order.order_id)" class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                    View Details
                  </button>
                  <button @click="deleteOrder(order.order_id)" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Order Details Modal -->
    <div v-if="showOrderDetails" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg max-w-4xl w-full mx-4 max-h-96 overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Order Details - #{{ selectedOrderDetails.order_id }}</h3>
          <div class="flex gap-2">
            <button @click="deleteOrderFromModal" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">
              Delete Order
            </button>
            <button @click="closeOrderDetails" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <div v-if="selectedOrderDetails" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p><strong>Customer:</strong> {{ selectedOrderDetails.user_name }}</p>
              <p><strong>Email:</strong> {{ selectedOrderDetails.user_email }}</p>
              <p><strong>Payment Method:</strong> {{ selectedOrderDetails.payment_method }}</p>
            </div>
            <div>
              <p><strong>Total Amount:</strong> ৳{{ selectedOrderDetails.total_amount }}</p>
              <p><strong>Delivery Status:</strong> {{ selectedOrderDetails.delivery_status }}</p>
              <p><strong>Order Date:</strong> {{ formatDate(selectedOrderDetails.created_at) }}</p>
            </div>
          </div>
          
          <div>
            <h4 class="font-semibold mb-2">Order Items:</h4>
            <table class="min-w-full border rounded">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-3 py-2 text-left">Item</th>
                  <th class="px-3 py-2 text-left">Quantity</th>
                  <th class="px-3 py-2 text-left">Unit Price</th>
                  <th class="px-3 py-2 text-left">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in selectedOrderDetails.items" :key="item.item_name" class="border-t">
                  <td class="px-3 py-2">{{ item.item_name }}</td>
                  <td class="px-3 py-2">{{ item.quantity }}</td>
                  <td class="px-3 py-2">৳{{ item.unit_price }}</td>
                  <td class="px-3 py-2">৳{{ item.subtotal }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { TokenManager } from '@/utils/auth.js'

const router = useRouter()

// State Management
const currentView = ref('items') // 'items' or 'orders'
const items = ref([])
const orders = ref([])
const isLoading = ref(false)
const error = ref('')
const successMessage = ref('')

// Form Management
const showCreateItemForm = ref(false)
const showEditItemForm = ref(false)
const showOrderDetails = ref(false)

// Form Data
const itemForm = ref({
  name: '',
  category: '',
  description: '',
  price: 0,
  image: '',
  availability: true,
})

const editItemId = ref(null)
const selectedOrderDetails = ref(null)

// API Base URLs
const ITEMS_API_BASE = '/api/cds/owner/items/'
const ORDERS_API_BASE = '/api/cds/owner/orders/'

const getAuthHeaders = () => {
  const token = TokenManager.getAccessToken()
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
}

// Item Management
const fetchItems = async () => {
  isLoading.value = true
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(ITEMS_API_BASE, {
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Failed to fetch items')
    const data = await res.json()
    items.value = data
  } catch (e) {
    error.value = 'Failed to load items.'
    console.error('Items fetch error:', e)
  } finally {
    isLoading.value = false
  }
}

const createItem = async () => {
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(ITEMS_API_BASE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(itemForm.value)
    })
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      throw new Error(errorData.error || 'Create failed')
    }
    
    const newItem = await res.json()
    
    resetItemForm()
    await fetchItems()
    
    // Show success message
    successMessage.value = `Item "${newItem.name}" created successfully.`
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
    
  } catch (e) {
    error.value = 'Failed to create item.'
    console.error('Item create error:', e)
  }
}

const editItem = (item) => {
  console.log('Edit item clicked:', item)
  showEditItemForm.value = true
  showCreateItemForm.value = false
  editItemId.value = item.item_id
  itemForm.value = { ...item }
  
  // Scroll to the edit form after a short delay to ensure it's rendered
  setTimeout(() => {
    const editForm = document.querySelector('.edit-item-form')
    if (editForm) {
      editForm.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, 100)
}

const updateItem = async () => {
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(`${ITEMS_API_BASE}${editItemId.value}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(itemForm.value)
    })
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      throw new Error(errorData.error || 'Update failed')
    }
    
    const updatedItem = await res.json()
    
    resetItemForm()
    await fetchItems()
    
    // Show success message
    successMessage.value = `Item "${updatedItem.name}" updated successfully.`
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
    
  } catch (e) {
    error.value = 'Failed to update item.'
    console.error('Item update error:', e)
  }
}

const deleteItem = async (itemId, itemName) => {
  if (!confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`)) {
    return
  }
  
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(`${ITEMS_API_BASE}${itemId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      throw new Error(errorData.error || 'Delete failed')
    }
    
    // Parse the success response
    const data = await res.json().catch(() => ({}))
    
    // Remove the item from the list immediately
    items.value = items.value.filter(item => item.item_id !== itemId)
    
    // Show success message
    successMessage.value = data.message || `Item "${itemName}" deleted successfully.`
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
    
  } catch (e) {
    error.value = 'Failed to delete item.'
    console.error('Item delete error:', e)
  }
}

const resetItemForm = () => {
  showCreateItemForm.value = false
  showEditItemForm.value = false
  editItemId.value = null
  itemForm.value = {
    name: '',
    category: '',
    description: '',
    price: 0,
    image: '',
    availability: true,
  }
}

// Orders Management
const fetchOrders = async () => {
  isLoading.value = true
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(ORDERS_API_BASE, {
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Failed to fetch orders')
    const data = await res.json()
    orders.value = data
  } catch (e) {
    error.value = 'Failed to load orders.'
    console.error('Orders fetch error:', e)
  } finally {
    isLoading.value = false
  }
}

const updateOrderStatus = async (orderId, newStatus) => {
  error.value = ''
  try {
    const res = await fetch(`${ORDERS_API_BASE}${orderId}/status/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ delivery_status: newStatus })
    })
    if (!res.ok) throw new Error('Status update failed')
    
    // Update the order in the list
    const orderIndex = orders.value.findIndex(order => order.order_id === orderId)
    if (orderIndex !== -1) {
      orders.value[orderIndex].delivery_status = newStatus
    }
  } catch (e) {
    error.value = 'Failed to update order status.'
    console.error('Status update error:', e)
    // Refresh orders to revert any UI changes
    await fetchOrders()
  }
}

const viewOrderDetails = async (orderId) => {
  error.value = ''
  try {
    const res = await fetch(`${ORDERS_API_BASE}${orderId}/`, {
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Failed to fetch order details')
    const data = await res.json()
    selectedOrderDetails.value = data
    showOrderDetails.value = true
  } catch (e) {
    error.value = 'Failed to load order details.'
    console.error('Order details fetch error:', e)
  }
}

const closeOrderDetails = () => {
  showOrderDetails.value = false
  selectedOrderDetails.value = null
}

const deleteOrder = async (orderId) => {
  if (!confirm(`Are you sure you want to delete Order #${orderId}? This action cannot be undone.`)) {
    return
  }
  
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(`${ORDERS_API_BASE}${orderId}/delete/`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    
    if (!res.ok) throw new Error('Failed to delete order')
    
    const data = await res.json()
    
    // Remove the order from the list
    orders.value = orders.value.filter(order => order.order_id !== orderId)
    
    // Show success message
    successMessage.value = data.message || `Order #${orderId} has been successfully deleted.`
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
    
  } catch (e) {
    error.value = 'Failed to delete order.'
    console.error('Order delete error:', e)
  }
}

const deleteOrderFromModal = async () => {
  if (!selectedOrderDetails.value) return
  
  const orderId = selectedOrderDetails.value.order_id
  
  if (!confirm(`Are you sure you want to delete Order #${orderId}? This action cannot be undone.`)) {
    return
  }
  
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(`${ORDERS_API_BASE}${orderId}/delete/`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    
    if (!res.ok) throw new Error('Failed to delete order')
    
    const data = await res.json()
    
    // Remove the order from the list
    orders.value = orders.value.filter(order => order.order_id !== orderId)
    
    // Close the modal
    closeOrderDetails()
    
    // Show success message
    successMessage.value = data.message || `Order #${orderId} has been successfully deleted.`
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
    
  } catch (e) {
    error.value = 'Failed to delete order.'
    console.error('Order delete error:', e)
  }
}

// Utility Functions
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusColor = (status) => {
  switch (status) {
    case 'preparing':
      return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    case 'ready':
      return 'bg-green-100 text-green-800 border-green-300'
    default:
      return 'bg-gray-100 text-gray-800 border-gray-300'
  }
}

// Navigation
const navigateToLanding = () => {
  router.push('/')
}

// Load data when view changes
const loadCurrentViewData = () => {
  if (currentView.value === 'items') {
    fetchItems()
  } else if (currentView.value === 'orders') {
    fetchOrders()
  }
}

// Initialize on mount
onMounted(() => {
  loadCurrentViewData()
})

// Watch for view changes
watch(currentView, () => {
  loadCurrentViewData()
})
</script>

<style scoped>
.container { 
  max-width: 1200px; 
}

.grid {
  display: grid;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

@media (min-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.transition-colors {
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out;
}

.fixed {
  position: fixed;
}

.inset-0 {
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.bg-opacity-50 {
  background-color: rgba(0, 0, 0, 0.5);
}

.z-50 {
  z-index: 50;
}

.max-h-96 {
  max-height: 24rem;
}

.overflow-y-auto {
  overflow-y: auto;
}
</style>
