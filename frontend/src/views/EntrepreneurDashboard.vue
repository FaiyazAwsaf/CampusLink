<template>
  <div class="container mx-auto py-8">
    <div class="mb-6 flex items-center">
      <button @click="navigateToLanding" class="mr-4 p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
      </button>
      <h1 class="text-2xl font-bold">Entrepreneur Dashboard</h1>
    </div>
    <div v-if="error" class="mb-4 text-red-600">{{ error }}</div>

    <!-- Storefront Selection View -->
    <div v-if="currentView === 'storefronts'">
      <div class="mb-6 flex justify-between items-center">
        <h2 class="text-xl font-semibold">My Storefronts</h2>
        <button @click="showCreateStorefrontForm = true" class="bg-green-600 text-white px-4 py-2 rounded">
          Create New Storefront
        </button>
      </div>

      <!-- Create Storefront Form -->
      <div v-if="showCreateStorefrontForm" class="mb-8 p-4 border rounded bg-gray-50">
        <h3 class="text-lg font-semibold mb-4">Create New Storefront</h3>
        <form @submit.prevent="createStorefront">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Storefront Name</label>
            <input v-model="storefrontForm.name" class="border px-3 py-2 w-full rounded" required />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Image URL</label>
            <input v-model="storefrontForm.image" class="border px-3 py-2 w-full rounded" />
          </div>
          <div class="flex gap-2">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Create Storefront</button>
            <button type="button" @click="resetStorefrontForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>

      <!-- No Storefronts Message -->
      <div v-if="storefronts.length === 0 && !isLoading" class="text-center py-12">
        <div class="text-gray-600 mb-4">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No storefronts yet</h3>
        <p class="text-gray-600 mb-4">Get started by creating your first storefront to sell products.</p>
        <button @click="showCreateStorefrontForm = true" class="bg-green-600 text-white px-6 py-3 rounded-lg">
          Create Your First Storefront
        </button>
      </div>

      <!-- Storefronts Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="storefront in storefronts" :key="storefront.store_id" 
             class="border rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow cursor-pointer"
             @click="selectStorefront(storefront)">
          <img :src="storefront.image" :alt="storefront.name" class="w-full h-48 object-cover">
          <div class="p-4">
            <h3 class="text-lg font-semibold mb-2">{{ storefront.name }}</h3>
            <div class="flex justify-between items-center">
              <button @click.stop="selectStorefront(storefront)" class="bg-blue-600 text-white px-4 py-2 rounded text-sm">
                Manage Products
              </button>
              <div class="flex gap-2">
                <button @click.stop="editStorefront(storefront)" class="bg-yellow-500 text-white px-3 py-1 rounded text-sm">
                  Edit
                </button>
                <button @click.stop="deleteStorefront(storefront.store_id)" class="bg-red-600 text-white px-3 py-1 rounded text-sm">
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Management View -->
    <div v-if="currentView === 'products'">
      <div class="mb-6 flex justify-between items-center">
        <div>
          <button @click="backToStorefronts" class="bg-gray-500 text-white px-4 py-2 rounded mr-4">
            ← Back to Storefronts
          </button>
          <h2 class="text-xl font-semibold inline">Products for {{ selectedStorefront.name }}</h2>
        </div>
        <button @click="showCreateForm = true" class="bg-green-600 text-white px-4 py-2 rounded">Add Product</button>
      </div>

      <!-- Create Product Form -->
      <div v-if="showCreateForm" class="mb-8 p-4 border rounded bg-gray-50">
        <h3 class="text-lg font-semibold mb-2">Create New Product</h3>
        <form @submit.prevent="createProduct">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Name</label>
              <input v-model="productForm.name" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Category</label>
              <input v-model="productForm.category" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Price</label>
              <input v-model.number="productForm.price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Availability</label>
              <select v-model="productForm.availability" class="border px-3 py-2 w-full rounded">
                <option :value="true">Available</option>
                <option :value="false">Unavailable</option>
              </select>
            </div>
          </div>
          <div class="mb-2">
            <label class="block text-sm font-medium mb-1">Description</label>
            <textarea v-model="productForm.description" class="border px-3 py-2 w-full rounded" rows="3" required></textarea>
          </div>
          <div class="mb-2">
            <label class="block text-sm font-medium mb-1">Image URL</label>
            <input v-model="productForm.image" class="border px-3 py-2 w-full rounded" />
          </div>
          <div class="flex gap-2 mt-4">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Create Product</button>
            <button type="button" @click="resetProductForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>

      <!-- Products Table -->
      <div v-if="isLoading" class="mb-4">Loading...</div>
      <div v-if="products.length === 0 && !isLoading" class="text-center py-8">
        <p class="text-gray-600 mb-4">No products in this storefront yet.</p>
        <button @click="showCreateForm = true" class="bg-green-600 text-white px-6 py-3 rounded-lg">
          Add Your First Product
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
            <tr v-for="product in products" :key="product.product_id" class="border-t">
              <td class="px-4 py-3">{{ product.name }}</td>
              <td class="px-4 py-3">{{ product.category }}</td>
              <td class="px-4 py-3">৳{{ product.price }}</td>
              <td class="px-4 py-3">
                <span :class="product.availability ? 'text-green-600' : 'text-red-600'">
                  {{ product.availability ? 'Available' : 'Unavailable' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <button @click="editProduct(product)" class="bg-yellow-500 text-white px-3 py-1 rounded mr-2 text-sm">Edit</button>
                <button @click="deleteProduct(product.product_id)" class="bg-red-600 text-white px-3 py-1 rounded text-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Edit Product Form -->
      <div v-if="showEditForm" class="mt-8 p-4 border rounded bg-gray-50">
        <h3 class="text-lg font-semibold mb-2">Edit Product</h3>
        <form @submit.prevent="updateProduct">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Name</label>
              <input v-model="productForm.name" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Category</label>
              <input v-model="productForm.category" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Price</label>
              <input v-model.number="productForm.price" type="number" min="0" step="0.01" class="border px-3 py-2 w-full rounded" required />
            </div>
            <div class="mb-2">
              <label class="block text-sm font-medium mb-1">Availability</label>
              <select v-model="productForm.availability" class="border px-3 py-2 w-full rounded">
                <option :value="true">Available</option>
                <option :value="false">Unavailable</option>
              </select>
            </div>
          </div>
          <div class="mb-2">
            <label class="block text-sm font-medium mb-1">Description</label>
            <textarea v-model="productForm.description" class="border px-3 py-2 w-full rounded" rows="3" required></textarea>
          </div>
          <div class="mb-2">
            <label class="block text-sm font-medium mb-1">Image URL</label>
            <input v-model="productForm.image" class="border px-3 py-2 w-full rounded" />
          </div>
          <div class="flex gap-2 mt-4">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Update Product</button>
            <button type="button" @click="resetProductForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Storefront Form -->
    <div v-if="showEditStorefrontForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold mb-4">Edit Storefront</h3>
        <form @submit.prevent="updateStorefront">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Storefront Name</label>
            <input v-model="storefrontForm.name" class="border px-3 py-2 w-full rounded" required />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Image URL</label>
            <input v-model="storefrontForm.image" class="border px-3 py-2 w-full rounded" />
          </div>
          <div class="flex gap-2">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Update Storefront</button>
            <button type="button" @click="resetStorefrontForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { TokenManager } from '@/utils/auth.js'

const router = useRouter()

// State Management
const currentView = ref('storefronts') // 'storefronts' or 'products'
const storefronts = ref([])
const products = ref([])
const selectedStorefront = ref(null)
const isLoading = ref(false)
const error = ref('')

// Form Management
const showCreateStorefrontForm = ref(false)
const showEditStorefrontForm = ref(false)
const showCreateForm = ref(false)
const showEditForm = ref(false)

// Form Data
const storefrontForm = ref({
  name: '',
  image: '',
})

const productForm = ref({
  name: '',
  category: '',
  description: '',
  price: 0,
  image: '',
  availability: true,
})

const editStorefrontId = ref(null)
const editProductId = ref(null)

// API Base URLs
const STOREFRONT_API_BASE = '/api/entrepreneurs_hub/manage/storefronts/'
const PRODUCT_API_BASE = '/api/entrepreneurs_hub/products/manage/'

const getAuthHeaders = () => {
  const token = TokenManager.getAccessToken()
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
}

// Storefront Management
const fetchStorefronts = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const res = await fetch(STOREFRONT_API_BASE, {
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Failed to fetch storefronts')
    const data = await res.json()
    storefronts.value = data
  } catch (e) {
    error.value = 'Failed to load storefronts.'
    console.error('Storefront fetch error:', e)
  } finally {
    isLoading.value = false
  }
}

const createStorefront = async () => {
  error.value = ''
  try {
    const res = await fetch(STOREFRONT_API_BASE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(storefrontForm.value)
    })
    if (!res.ok) throw new Error('Create failed')
    resetStorefrontForm()
    await fetchStorefronts()
  } catch (e) {
    error.value = 'Failed to create storefront.'
    console.error('Storefront create error:', e)
  }
}

const editStorefront = (storefront) => {
  showEditStorefrontForm.value = true
  editStorefrontId.value = storefront.store_id
  storefrontForm.value = { ...storefront }
}

const updateStorefront = async () => {
  error.value = ''
  try {
    const res = await fetch(`${STOREFRONT_API_BASE}${editStorefrontId.value}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(storefrontForm.value)
    })
    if (!res.ok) throw new Error('Update failed')
    resetStorefrontForm()
    await fetchStorefronts()
  } catch (e) {
    error.value = 'Failed to update storefront.'
    console.error('Storefront update error:', e)
  }
}

const deleteStorefront = async (id) => {
  if (!confirm('Are you sure you want to delete this storefront? All products in this storefront will also be deleted.')) {
    return
  }
  
  error.value = ''
  try {
    const res = await fetch(`${STOREFRONT_API_BASE}${id}/`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Delete failed')
    await fetchStorefronts()
  } catch (e) {
    error.value = 'Failed to delete storefront.'
    console.error('Storefront delete error:', e)
  }
}

const resetStorefrontForm = () => {
  showCreateStorefrontForm.value = false
  showEditStorefrontForm.value = false
  editStorefrontId.value = null
  storefrontForm.value = {
    name: '',
    image: '',
  }
}

// Navigation
const selectStorefront = (storefront) => {
  selectedStorefront.value = storefront
  currentView.value = 'products'
  fetchProducts()
}

const backToStorefronts = () => {
  currentView.value = 'storefronts'
  selectedStorefront.value = null
  products.value = []
  resetProductForm()
}

// Product Management
const fetchProducts = async () => {
  if (!selectedStorefront.value) return
  
  isLoading.value = true
  error.value = ''
  try {
    const res = await fetch(`${PRODUCT_API_BASE}?storefront_id=${selectedStorefront.value.store_id}`, {
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Failed to fetch products')
    const data = await res.json()
    products.value = data
  } catch (e) {
    error.value = 'Failed to load products.'
    console.error('Product fetch error:', e)
  } finally {
    isLoading.value = false
  }
}

const createProduct = async () => {
  if (!selectedStorefront.value) return
  
  error.value = ''
  try {
    const productData = {
      ...productForm.value,
      storefront_id: selectedStorefront.value.store_id
    }
    
    const res = await fetch(PRODUCT_API_BASE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(productData)
    })
    if (!res.ok) throw new Error('Create failed')
    resetProductForm()
    await fetchProducts()
  } catch (e) {
    error.value = 'Failed to create product.'
    console.error('Product create error:', e)
  }
}

const editProduct = (product) => {
  showEditForm.value = true
  showCreateForm.value = false
  editProductId.value = product.product_id
  productForm.value = { ...product }
}

const updateProduct = async () => {
  if (!selectedStorefront.value) return
  
  error.value = ''
  try {
    const productData = {
      ...productForm.value,
      storefront_id: selectedStorefront.value.store_id
    }
    
    const res = await fetch(`${PRODUCT_API_BASE}${editProductId.value}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(productData)
    })
    if (!res.ok) throw new Error('Update failed')
    resetProductForm()
    await fetchProducts()
  } catch (e) {
    error.value = 'Failed to update product.'
    console.error('Product update error:', e)
  }
}

const deleteProduct = async (id) => {
  if (!confirm('Are you sure you want to delete this product?')) {
    return
  }
  
  error.value = ''
  try {
    const res = await fetch(`${PRODUCT_API_BASE}${id}/`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    if (!res.ok) throw new Error('Delete failed')
    await fetchProducts()
  } catch (e) {
    error.value = 'Failed to delete product.'
    console.error('Product delete error:', e)
  }
}

const resetProductForm = () => {
  showCreateForm.value = false
  showEditForm.value = false
  editProductId.value = null
  productForm.value = {
    name: '',
    category: '',
    description: '',
    price: 0,
    image: '',
    availability: true,
  }
}

// Navigation
const navigateToLanding = () => {
  router.push('/')
}

onMounted(fetchStorefronts)
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

@media (min-width: 1024px) {
  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.transition-shadow {
  transition: box-shadow 0.15s ease-in-out;
}

.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.object-cover {
  object-fit: cover;
}

.cursor-pointer {
  cursor: pointer;
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

.overflow-hidden {
  overflow: hidden;
}
</style>
