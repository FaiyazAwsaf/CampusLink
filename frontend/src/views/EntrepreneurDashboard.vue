<template>
  <div class="container mx-auto py-8">
    <h1 class="text-2xl font-bold mb-6">Entrepreneur Dashboard</h1>
    <div v-if="error" class="mb-4 text-red-600">{{ error }}</div>
    <div class="mb-6">
      <button @click="showCreateForm = true" class="bg-green-600 text-white px-4 py-2 rounded">Add Product</button>
    </div>
    <div v-if="showCreateForm" class="mb-8 p-4 border rounded bg-gray-50">
      <h2 class="text-lg font-semibold mb-2">Create New Product</h2>
      <form @submit.prevent="createProduct">
        <div class="mb-2">
          <label class="block">Name</label>
          <input v-model="form.name" class="border px-2 py-1 w-full" required />
        </div>
        <div class="mb-2">
          <label class="block">Category</label>
          <input v-model="form.category" class="border px-2 py-1 w-full" required />
        </div>
        <div class="mb-2">
          <label class="block">Description</label>
          <textarea v-model="form.description" class="border px-2 py-1 w-full" required></textarea>
        </div>
        <div class="mb-2">
          <label class="block">Price</label>
          <input v-model.number="form.price" type="number" min="0" step="0.01" class="border px-2 py-1 w-full" required />
        </div>
        <div class="mb-2">
          <label class="block">Image URL</label>
          <input v-model="form.image" class="border px-2 py-1 w-full" />
        </div>
        <div class="mb-2">
          <label class="block">Availability</label>
          <select v-model="form.availability" class="border px-2 py-1 w-full">
            <option :value="true">Available</option>
            <option :value="false">Unavailable</option>
          </select>
        </div>
        <div class="flex gap-2 mt-4">
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Create</button>
          <button type="button" @click="resetForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
        </div>
      </form>
    </div>
    <h2 class="text-xl font-semibold mb-4">My Products</h2>
    <div v-if="isLoading" class="mb-4">Loading...</div>
    <div v-if="products.length === 0 && !isLoading" class="mb-4">No products found.</div>
    <div v-else>
      <table class="min-w-full border">
        <thead>
          <tr class="bg-gray-100">
            <th class="px-4 py-2">Name</th>
            <th class="px-4 py-2">Category</th>
            <th class="px-4 py-2">Price</th>
            <th class="px-4 py-2">Availability</th>
            <th class="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.product_id">
            <td class="border px-4 py-2">{{ product.name }}</td>
            <td class="border px-4 py-2">{{ product.category }}</td>
            <td class="border px-4 py-2">{{ product.price }}</td>
            <td class="border px-4 py-2">{{ product.availability ? 'Available' : 'Unavailable' }}</td>
            <td class="border px-4 py-2">
              <button @click="editProduct(product)" class="bg-yellow-500 text-white px-2 py-1 rounded mr-2">Edit</button>
              <button @click="deleteProduct(product.product_id)" class="bg-red-600 text-white px-2 py-1 rounded">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="showEditForm" class="mt-8 p-4 border rounded bg-gray-50">
      <h2 class="text-lg font-semibold mb-2">Edit Product</h2>
      <form @submit.prevent="updateProduct">
        <div class="mb-2">
          <label class="block">Name</label>
          <input v-model="form.name" class="border px-2 py-1 w-full" required />
        </div>
        <div class="mb-2">
          <label class="block">Category</label>
          <input v-model="form.category" class="border px-2 py-1 w-full" required />
        </div>
        <div class="mb-2">
          <label class="block">Description</label>
          <textarea v-model="form.description" class="border px-2 py-1 w-full" required></textarea>
        </div>
        <div class="mb-2">
          <label class="block">Price</label>
          <input v-model.number="form.price" type="number" min="0" step="0.01" class="border px-2 py-1 w-full" required />
        </div>
        <div class="mb-2">
          <label class="block">Image URL</label>
          <input v-model="form.image" class="border px-2 py-1 w-full" />
        </div>
        <div class="mb-2">
          <label class="block">Availability</label>
          <select v-model="form.availability" class="border px-2 py-1 w-full">
            <option :value="true">Available</option>
            <option :value="false">Unavailable</option>
          </select>
        </div>
        <div class="flex gap-2 mt-4">
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Update</button>
          <button type="button" @click="resetForm" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const products = ref([])
const isLoading = ref(false)
const error = ref('')
const showCreateForm = ref(false)
const showEditForm = ref(false)
const form = ref({
  name: '',
  category: '',
  description: '',
  price: 0,
  image: '',
  availability: true,
})
const editProductId = ref(null)

const API_BASE = '/api/entrepreneurs_hub/products/manage/'

const fetchProducts = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const res = await fetch(API_BASE)
    const data = await res.json()
    products.value = data
  } catch (e) {
    error.value = 'Failed to load products.'
  } finally {
    isLoading.value = false
  }
}

const createProduct = async () => {
  error.value = ''
  try {
    const res = await fetch(API_BASE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    if (!res.ok) throw new Error('Create failed')
    resetForm()
    fetchProducts()
  } catch (e) {
    error.value = 'Failed to create product.'
  }
}

const editProduct = (product) => {
  showEditForm.value = true
  showCreateForm.value = false
  editProductId.value = product.product_id
  form.value = { ...product }
}

const updateProduct = async () => {
  error.value = ''
  try {
    const res = await fetch(`${API_BASE}${editProductId.value}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    if (!res.ok) throw new Error('Update failed')
    resetForm()
    fetchProducts()
  } catch (e) {
    error.value = 'Failed to update product.'
  }
}

const deleteProduct = async (id) => {
  error.value = ''
  try {
    const res = await fetch(`${API_BASE}${id}/`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error('Delete failed')
    fetchProducts()
  } catch (e) {
    error.value = 'Failed to delete product.'
  }
}

const resetForm = () => {
  showCreateForm.value = false
  showEditForm.value = false
  editProductId.value = null
  form.value = {
    name: '',
    category: '',
    description: '',
    price: 0,
    image: '',
    availability: true,
  }
}

onMounted(fetchProducts)
</script>

<style scoped>
.container { max-width: 900px; }
</style>
