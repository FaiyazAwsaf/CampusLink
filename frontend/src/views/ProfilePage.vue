<template>
  <NavBar />
  <div class="max-w-4xl mx-auto mt-8 p-6 bg-white rounded-xl shadow">
    <h1 class="text-2xl font-bold mb-6">Your Profile</h1>

    <!-- User Info -->
    <section class="mb-8">
      <h2 class="text-xl font-semibold mb-4">Account Information</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Phone</label>
          <input
            type="text"
            v-model="form.phone"
            class="mt-1 w-full rounded border-gray-300"
            placeholder="Your phone"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Profile Image</label>
          <input type="file" accept="image/*" @change="onImageChange" class="mt-1 w-full" />
          <div v-if="previewUrl" class="mt-2">
            <img :src="previewUrl" alt="Preview" class="h-16 w-16 rounded-full object-cover" />
          </div>
        </div>
      </div>

      <div class="mt-4 flex gap-3">
        <button
          @click="saveProfile"
          :disabled="saving"
          class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
        >
          {{ saving ? 'Saving…' : 'Save Changes' }}
        </button>
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
          <ul v-else class="divide-y">
            <li
              v-for="order in laundry.orders"
              :key="order.invoice_number"
              class="py-3 flex justify-between items-center"
            >
              <div>
                <div class="font-medium">Invoice: {{ order.invoice_number }}</div>
                <div class="text-sm text-gray-600">
                  {{ formatDate(order.created_at) }} • {{ order.total_items }} items • Tk.
                  {{ order.total_amount }}
                </div>
              </div>
              <span :class="statusClass(order.status)">{{ order.status }}</span>
            </li>
          </ul>
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
    } else {
      saveError.value = res.data?.error || 'Failed to update profile'
    }
  } catch (e) {
    saveError.value = e?.response?.data?.error || 'Failed to update profile'
  } finally {
    saving.value = false
  }
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
