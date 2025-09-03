<template>
  <div class="container mx-auto py-8">
    <div class="mb-6 flex items-center">
      <button @click="navigateToLanding" class="mr-4 p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
      </button>
      <h1 class="text-2xl font-bold">Laundry Staff Dashboard</h1>
    </div>

    <div v-if="error" class="mb-4 text-red-600">{{ error }}</div>
    <div v-if="successMessage" class="mb-4 text-green-600">{{ successMessage }}</div>

    <!-- Navigation Tabs -->
    <div class="mb-6">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button 
            @click="currentView = 'categories'"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
              currentView === 'categories' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Manage Categories
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

    <!-- Categories Management View -->
    <div v-if="currentView === 'categories'">
      <div class="mb-6 flex justify-between items-center">
        <h2 class="text-xl font-semibold">Laundry Categories</h2>
        <button @click="showCreateCategoryForm = true" class="bg-green-600 text-white px-4 py-2 rounded">
          Add New Category
        </button>
      </div>

      <!-- Create Category Form -->
      <div v-if="showCreateCategoryForm" class="mb-8 p-4 border rounded bg-gray-50">
        <h3 class="text-lg font-semibold mb-4">Create New Category</h3>
        <form @submit.prevent="createCategory">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Category Name</label>
              <input v-model="categoryForm.name" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Wash Price (৳)</label>
              <input v-model.number="categoryForm.wash_price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Ironing Price (৳)</label>
              <input v-model.number="categoryForm.ironing_price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
          </div>
          <div class="flex gap-2">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Create Category</button>
            <button type="button" @click="resetCategoryForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>

      <!-- Categories Table -->
      <div v-if="isLoading" class="mb-4">Loading categories...</div>
      <div v-if="categories.length === 0 && !isLoading" class="text-center py-12">
        <div class="text-gray-600 mb-4">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No categories yet</h3>
        <p class="text-gray-600 mb-4">Get started by creating your first laundry category.</p>
        <button @click="showCreateCategoryForm = true" class="bg-green-600 text-white px-6 py-3 rounded-lg">
          Create Your First Category
        </button>
      </div>
      <div v-else>
        <table class="min-w-full border rounded-lg overflow-hidden">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-3 text-left">Category Name</th>
              <th class="px-4 py-3 text-left">Wash Price</th>
              <th class="px-4 py-3 text-left">Ironing Price</th>
              <th class="px-4 py-3 text-left">Created</th>
              <th class="px-4 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="category in categories" :key="category.id" class="border-t">
              <td class="px-4 py-3">{{ category.name }}</td>
              <td class="px-4 py-3">৳{{ category.wash_price }}</td>
              <td class="px-4 py-3">৳{{ category.ironing_price }}</td>
              <td class="px-4 py-3">{{ formatDate(category.created_at) }}</td>
              <td class="px-4 py-3">
                <button @click="editCategory(category)" class="bg-yellow-500 text-white px-3 py-1 rounded mr-2 text-sm">Edit</button>
                <button @click="deleteCategory(category.id)" class="bg-red-600 text-white px-3 py-1 rounded text-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Edit Category Form -->
      <div v-if="showEditCategoryForm" class="mt-8 p-4 border rounded bg-gray-50">
        <h3 class="text-lg font-semibold mb-4">Edit Category</h3>
        <form @submit.prevent="updateCategory">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Category Name</label>
              <input v-model="categoryForm.name" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Wash Price (৳)</label>
              <input v-model.number="categoryForm.wash_price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium mb-2">Ironing Price (৳)</label>
              <input v-model.number="categoryForm.ironing_price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
          </div>
          <div class="flex gap-2">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Update Category</button>
            <button type="button" @click="resetCategoryForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Orders Management View -->
    <div v-if="currentView === 'orders'">
      <div class="mb-6 flex justify-between items-center">
        <h2 class="text-xl font-semibold">All Laundry Orders</h2>
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
              <th class="px-4 py-3 text-left">Invoice #</th>
              <th class="px-4 py-3 text-left">Customer</th>
              <th class="px-4 py-3 text-left">Items</th>
              <th class="px-4 py-3 text-left">Total</th>
              <th class="px-4 py-3 text-left">Status</th>
              <th class="px-4 py-3 text-left">Delivery Date</th>
              <th class="px-4 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id" class="border-t">
              <td class="px-4 py-3">{{ order.invoice_number }}</td>
              <td class="px-4 py-3">
                <div>{{ order.user_name }}</div>
                <div class="text-sm text-gray-500">{{ order.user_email }}</div>
              </td>
              <td class="px-4 py-3">{{ order.total_items }}</td>
              <td class="px-4 py-3">৳{{ order.total_amount }}</td>
              <td class="px-4 py-3">
                <select 
                  :value="order.status" 
                  @change="updateOrderStatus(order.id, $event.target.value)"
                  :class="getStatusColor(order.status)"
                  class="px-3 py-1 rounded text-sm font-medium"
                >
                  <option value="processing">Processing</option>
                  <option value="completed">Completed</option>
                  <option value="delivered">Delivered</option>
                </select>
              </td>
              <td class="px-4 py-3">{{ formatDate(order.estimated_delivery_date) }}</td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button @click="viewOrderDetails(order.id)" class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                    View Details
                  </button>
                  <button @click="deleteOrder(order.id, order.invoice_number)" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">
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
          <h3 class="text-lg font-semibold">Order Details - {{ selectedOrderDetails.invoice_number }}</h3>
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
              <p><strong>Status:</strong> {{ selectedOrderDetails.status }}</p>
            </div>
            <div>
              <p><strong>Total Amount:</strong> ৳{{ selectedOrderDetails.total_amount }}</p>
              <p><strong>Total Items:</strong> {{ selectedOrderDetails.total_items }}</p>
              <p><strong>Delivery Date:</strong> {{ formatDate(selectedOrderDetails.estimated_delivery_date) }}</p>
            </div>
          </div>
          
          <div>
            <h4 class="font-semibold mb-2">Order Items:</h4>
            <table class="min-w-full border rounded">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-3 py-2 text-left">Item</th>
                  <th class="px-3 py-2 text-left">Quantity</th>
                  <th class="px-3 py-2 text-left">Services</th>
                  <th class="px-3 py-2 text-left">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in selectedOrderDetails.items" :key="item.category_name" class="border-t">
                  <td class="px-3 py-2">{{ item.category_name }}</td>
                  <td class="px-3 py-2">{{ item.quantity }}</td>
                  <td class="px-3 py-2">
                    <span v-if="item.wash" class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm mr-1">Wash</span>
                    <span v-if="item.ironing" class="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Ironing</span>
                  </td>
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
const currentView = ref('categories') // 'categories' or 'orders'
const categories = ref([])
const orders = ref([])
const isLoading = ref(false)
const error = ref('')
const successMessage = ref('')

// Form Management
const showCreateCategoryForm = ref(false)
const showEditCategoryForm = ref(false)
const showOrderDetails = ref(false)

// Form Data
const categoryForm = ref({
  name: '',
  wash_price: 0,
  ironing_price: 0,
})

const editCategoryId = ref(null)
const selectedOrderDetails = ref(null)

// API Base URLs
const CATEGORY_API_BASE = '/api/laundry/staff/categories/'
const ORDERS_API_BASE = '/api/laundry/staff/orders/'

const getAuthHeaders = () => {
  const token = TokenManager.getAccessToken()
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
}

// Category Management
const fetchCategories = async () => {
  isLoading.value = true
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(CATEGORY_API_BASE, {
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Failed to fetch categories')
    const data = await res.json()
    categories.value = data
  } catch (e) {
    error.value = 'Failed to load categories.'
    console.error('Category fetch error:', e)
  } finally {
    isLoading.value = false
  }
}

const createCategory = async () => {
  error.value = ''
  try {
    const res = await fetch(CATEGORY_API_BASE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(categoryForm.value)
    })
    if (!res.ok) throw new Error('Create failed')
    resetCategoryForm()
    await fetchCategories()
  } catch (e) {
    error.value = 'Failed to create category.'
    console.error('Category create error:', e)
  }
}

const editCategory = (category) => {
  showEditCategoryForm.value = true
  showCreateCategoryForm.value = false
  editCategoryId.value = category.id
  categoryForm.value = { ...category }
}

const updateCategory = async () => {
  error.value = ''
  try {
    const res = await fetch(`${CATEGORY_API_BASE}${editCategoryId.value}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(categoryForm.value)
    })
    if (!res.ok) throw new Error('Update failed')
    resetCategoryForm()
    await fetchCategories()
  } catch (e) {
    error.value = 'Failed to update category.'
    console.error('Category update error:', e)
  }
}

const deleteCategory = async (id) => {
  if (!confirm('Are you sure you want to delete this category? This action cannot be undone.')) {
    return
  }
  
  error.value = ''
  try {
    const res = await fetch(`${CATEGORY_API_BASE}${id}/`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Delete failed')
    await fetchCategories()
  } catch (e) {
    error.value = 'Failed to delete category.'
    console.error('Category delete error:', e)
  }
}

const resetCategoryForm = () => {
  showCreateCategoryForm.value = false
  showEditCategoryForm.value = false
  editCategoryId.value = null
  categoryForm.value = {
    name: '',
    wash_price: 0,
    ironing_price: 0,
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
      body: JSON.stringify({ status: newStatus })
    })
    if (!res.ok) throw new Error('Status update failed')
    
    // Update the order in the list
    const orderIndex = orders.value.findIndex(order => order.id === orderId)
    if (orderIndex !== -1) {
      orders.value[orderIndex].status = newStatus
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

const deleteOrder = async (orderId, invoiceNumber) => {
  if (!confirm(`Are you sure you want to delete order ${invoiceNumber}? This action cannot be undone.`)) {
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
    
    // Remove the order from the list
    orders.value = orders.value.filter(order => order.id !== orderId)
    
    // Show success message
    successMessage.value = `Order ${invoiceNumber} has been successfully deleted.`
    
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
  
  const orderId = selectedOrderDetails.value.id
  const invoiceNumber = selectedOrderDetails.value.invoice_number
  
  if (!confirm(`Are you sure you want to delete order ${invoiceNumber}? This action cannot be undone.`)) {
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
    
    // Remove the order from the list
    orders.value = orders.value.filter(order => order.id !== orderId)
    
    // Close the modal
    closeOrderDetails()
    
    // Show success message
    successMessage.value = `Order ${invoiceNumber} has been successfully deleted.`
    
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
    day: 'numeric'
  })
}

const getStatusColor = (status) => {
  switch (status) {
    case 'processing':
      return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    case 'completed':
      return 'bg-blue-100 text-blue-800 border-blue-300'
    case 'delivered':
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
  if (currentView.value === 'categories') {
    fetchCategories()
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
  .md\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
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
