<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <h1 class="text-3xl font-bold text-gray-900">My Profile</h1>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-500">{{ user?.name }}</span>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {{ user?.role }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Profile Information -->
        <div class="bg-white shadow rounded-lg mb-8">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-6">Profile Information</h3>
            
            <form @submit.prevent="updateProfile" class="space-y-6">
              <!-- Profile Image -->
              <div class="flex items-center space-x-6">
                <div class="shrink-0">
                  <img
                    :src="imagePreview || user?.image || '/Default.jpg'"
                    alt="Profile"
                    class="h-20 w-20 object-cover rounded-full border-2 border-gray-300"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Profile Picture
                  </label>
                  <input
                    type="file"
                    ref="imageInput"
                    @change="handleImageChange"
                    accept="image/*"
                    class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                </div>
              </div>

              <!-- Name -->
              <div>
                <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                  Full Name
                </label>
                <input
                  id="name"
                  v-model="formData.name"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  :class="{ 'border-red-500': errors.name }"
                />
                <div v-if="errors.name" class="mt-1 text-sm text-red-600">
                  <ul class="list-disc list-inside">
                    <li v-for="error in errors.name" :key="error">{{ error }}</li>
                  </ul>
                </div>
              </div>

              <!-- Email (Read-only) -->
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  id="email"
                  :value="user?.email"
                  type="email"
                  readonly
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50 text-gray-500 cursor-not-allowed"
                />
                <p class="mt-1 text-sm text-gray-500">Email cannot be changed</p>
              </div>

              <!-- Phone -->
              <div>
                <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <input
                  id="phone"
                  v-model="formData.phone"
                  type="tel"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  :class="{ 'border-red-500': errors.phone }"
                />
                <div v-if="errors.phone" class="mt-1 text-sm text-red-600">
                  <ul class="list-disc list-inside">
                    <li v-for="error in errors.phone" :key="error">{{ error }}</li>
                  </ul>
                </div>
              </div>

              <!-- Role (Read-only) -->
              <div>
                <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
                  Role
                </label>
                <input
                  id="role"
                  :value="user?.role"
                  type="text"
                  readonly
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50 text-gray-500 cursor-not-allowed"
                />
                <p class="mt-1 text-sm text-gray-500">Role is managed by administrators</p>
              </div>

              <!-- Submit Button -->
              <div class="flex justify-end space-x-3">
                <button
                  type="button"
                  @click="resetForm"
                  class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Reset
                </button>
                <button
                  type="submit"
                  :disabled="isLoading"
                  class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400 disabled:cursor-not-allowed"
                >
                  {{ isLoading ? 'Updating...' : 'Update Profile' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Account Security -->
        <div class="bg-white shadow rounded-lg mb-8">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Account Security</h3>
            <div class="space-y-4">
              <div class="flex justify-between items-center py-2">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Password</h4>
                  <p class="text-sm text-gray-500">Last changed 30 days ago</p>
                </div>
                <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                  Change Password
                </button>
              </div>
              <div class="flex justify-between items-center py-2">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Account Status</h4>
                  <p class="text-sm text-gray-500">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Active
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Success/Error Messages -->
        <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {{ successMessage }}
        </div>
        
        <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import jwtAuthService from '@/utils/jwtAuthService.js'

const user = ref(null)
const isLoading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const errors = ref({})
const imagePreview = ref('')
const imageInput = ref(null)

const formData = reactive({
  name: '',
  phone: '',
  image: null
})

onMounted(async () => {
  user.value = jwtAuthService.getCurrentUser()
  if (user.value) {
    formData.name = user.value.name || ''
    formData.phone = user.value.phone || ''
  }
})

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.image = file
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const resetForm = () => {
  if (user.value) {
    formData.name = user.value.name || ''
    formData.phone = user.value.phone || ''
  }
  formData.image = null
  imagePreview.value = ''
  if (imageInput.value) {
    imageInput.value.value = ''
  }
  errors.value = {}
  successMessage.value = ''
  errorMessage.value = ''
}

const updateProfile = async () => {
  isLoading.value = true
  errors.value = {}
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const updateData = {
      name: formData.name,
      phone: formData.phone
    }
    
    if (formData.image) {
      updateData.image = formData.image
    }

    const result = await jwtAuthService.updateProfile(updateData)

    if (result.success) {
      successMessage.value = 'Profile updated successfully!'
      
      // User data is automatically updated in JWT service
      user.value = result.user
      
      // Clear form state
      formData.image = null
      imagePreview.value = ''
      if (imageInput.value) {
        imageInput.value.value = ''
      }
    } else {
      if (result.errors) {
        errors.value = result.errors
      } else {
        errorMessage.value = 'Failed to update profile'
      }
    }
  } catch (error) {
    console.error('Profile update error:', error)
    errorMessage.value = 'Failed to update profile. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <NavBar />
  <div class="max-w-5xl mx-auto mt-8 p-6 bg-white rounded-xl shadow">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Your Profile</h1>
      <div class="space-x-2">
        <button
          v-if="!editing"
          @click="startEdit"
          class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
        >
          Edit Profile
        </button>
        <template v-else>
          <button
            @click="saveProfile"
            :disabled="saving"
            class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
          >
            {{ saving ? 'Saving…' : 'Save' }}
          </button>
          <button
            @click="cancelEdit"
            :disabled="saving"
            class="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 disabled:opacity-50"
          >
            Cancel
          </button>
        </template>
      </div>
    </div>

    <!-- User Info -->
    <section class="mb-8">
      <h2 class="text-xl font-semibold mb-4">Account Information</h2>
      <div class="grid grid-cols-1 md:grid-cols-[auto_1fr] gap-6 items-start">
        <!-- Avatar -->
        <div class="flex flex-col items-center">
          <div class="h-24 w-24 rounded-full bg-gray-100 overflow-hidden ring-2 ring-indigo-100">
            <img
              v-if="previewUrl"
              :src="previewUrl"
              alt="Profile"
              class="h-full w-full object-cover"
            />
            <div v-else class="h-full w-full flex items-center justify-center text-gray-400">
              No Image
            </div>
          </div>
          <label class="mt-3 text-sm text-gray-600">Profile Image</label>
          <input
            type="file"
            accept="image/*"
            @change="onImageChange"
            class="mt-1 w-full"
            :disabled="!editing"
          />
        </div>

        <!-- Fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              :value="user?.email || ''"
              disabled
              class="mt-1 w-full rounded border-gray-300 bg-gray-100"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <input
              type="text"
              v-model="form.name"
              class="mt-1 w-full rounded border-gray-300"
              placeholder="Your name"
              :disabled="!editing"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Phone</label>
            <input
              type="text"
              v-model="form.phone"
              class="mt-1 w-full rounded border-gray-300"
              placeholder="Your phone"
              :disabled="!editing"
            />
          </div>
          <div class="flex items-end">
            <div>
              <p class="text-sm text-gray-600">Role</p>
              <p class="font-medium">{{ user?.role || 'Student' }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-3 min-h-[1.5rem]">
        <p v-if="saveError" class="text-red-600">{{ saveError }}</p>
        <p v-if="saveSuccess" class="text-green-700">Profile updated.</p>
      </div>
    </section>

    <!-- Orders Dropdowns -->
    <section class="space-y-4">
      <!-- Laundry Orders -->
      <details :open="true" class="rounded border">
        <summary class="cursor-pointer list-none p-3 font-semibold bg-gray-50 rounded">
          Laundry Orders
          <span class="ml-2 text-sm text-gray-500">(click to toggle)</span>
        </summary>
        <div class="p-3">
          <div v-if="laundry.loading" class="text-gray-500">Loading…</div>
          <div v-else-if="laundry.error" class="text-red-600">{{ laundry.error }}</div>
          <div v-else-if="!laundry.orders.length" class="text-gray-600">No laundry orders yet.</div>
          <div v-else class="grid gap-3">
            <div
              v-for="order in laundry.orders"
              :key="order.invoice_number"
              class="rounded border p-3 flex justify-between items-center hover:bg-gray-50"
            >
              <div>
                <div class="font-semibold">Invoice #{{ order.invoice_number }}</div>
                <div class="text-sm text-gray-600">
                  {{ formatDate(order.created_at) }} • {{ order.total_items }} items • Tk.
                  {{ order.total_amount }}
                </div>
              </div>
              <span :class="statusClass(order.status)">{{ order.status }}</span>
            </div>
          </div>
        </div>
      </details>

      <!-- CDS Orders -->
      <details class="rounded border">
        <summary class="cursor-pointer list-none p-3 font-semibold bg-gray-50 rounded">
          CDS Orders
          <span class="ml-2 text-sm text-gray-500">(click to toggle)</span>
        </summary>
        <div class="p-3 text-gray-600">
          No CDS order API found yet. We can wire this to your CDS orders endpoint when available.
        </div>
      </details>

      <!-- Entrepreneurs Hub Orders -->
      <details class="rounded border">
        <summary class="cursor-pointer list-none p-3 font-semibold bg-gray-50 rounded">
          Entrepreneurs Hub Orders
          <span class="ml-2 text-sm text-gray-500">(click to toggle)</span>
        </summary>
        <div class="p-3 text-gray-600">
          No Entrepreneurs Hub order API found yet. We can wire this once the endpoint exists.
        </div>
      </details>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// User state
const user = ref(null)
const form = ref({ name: '', phone: '' })
const imageFile = ref(null)
const previewUrl = ref('')
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)
const editing = ref(false)

// Laundry orders state
const laundry = ref({ orders: [], loading: false, error: '' })

function statusClass(status) {
  const base = 'px-2 py-1 rounded text-xs capitalize'
  switch ((status || '').toLowerCase()) {
    case 'pending':
      return base + ' bg-yellow-100 text-yellow-800'
    case 'processing':
      return base + ' bg-blue-100 text-blue-800'
    case 'completed':
      return base + ' bg-green-100 text-green-800'
    case 'cancelled':
      return base + ' bg-red-100 text-red-800'
    default:
      return base + ' bg-gray-100 text-gray-800'
  }
}

function formatDate(date) {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleString()
}

async function loadCurrentUser() {
  const res = await axios.get('/api/accounts/current-user/')
  if (!res.data?.success) throw new Error('Not authenticated')
  user.value = res.data.user
  form.value.name = user.value?.name || ''
  form.value.phone = user.value?.phone || ''
  previewUrl.value = user.value?.image || ''
}

async function loadLaundryOrders() {
  laundry.value.loading = true
  laundry.value.error = ''
  try {
    const res = await axios.get('/api/laundry/orders/')
    // Expecting array of orders per laundry views
    laundry.value.orders = Array.isArray(res.data) ? res.data : []
  } catch (e) {
    laundry.value.error = e?.response?.data?.detail || 'Failed to load laundry orders'
  } finally {
    laundry.value.loading = false
  }
}

function onImageChange(e) {
  const file = e.target.files?.[0]
  imageFile.value = file || null
  if (file) {
    previewUrl.value = URL.createObjectURL(file)
  }
}

async function saveProfile() {
  saveError.value = ''
  saveSuccess.value = false
  saving.value = true

  try {
    const data = new FormData()
    data.append('name', form.value.name || '')
    data.append('phone', form.value.phone || '')
    if (imageFile.value) data.append('image', imageFile.value)

    const res = await axios.post('/api/accounts/update-profile/', data)
    if (res.data?.success) {
      saveSuccess.value = true
      await loadCurrentUser()
      editing.value = false
    } else {
      saveError.value = res.data?.error || 'Failed to update profile'
    }
  } catch (e) {
    saveError.value = e?.response?.data?.error || 'Failed to update profile'
  } finally {
    saving.value = false
  }
}

function startEdit() {
  saveError.value = ''
  saveSuccess.value = false
  editing.value = true
}

function cancelEdit() {
  // Revert form values to current user
  form.value.name = user.value?.name || ''
  form.value.phone = user.value?.phone || ''
  previewUrl.value = user.value?.image || ''
  imageFile.value = null
  editing.value = false
}

onMounted(async () => {
  try {
    await loadCurrentUser()
  } catch (_) {
    router.push({ name: 'login', query: { next: '/profile' } })
    return
  }
  loadLaundryOrders()
})
</script>

<style scoped>
details[open] > summary {
  border-bottom: 1px solid #e5e7eb;
}
</style>
