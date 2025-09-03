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
        <div class="p-3">
          <div v-if="cds.loading" class="text-gray-500">Loading…</div>
          <div v-else-if="cds.error" class="text-red-600">{{ cds.error }}</div>
          <div v-else-if="!cds.orders.length" class="text-gray-600">No CDS orders yet.</div>
          <div v-else class="grid gap-3">
            <div
              v-for="order in cds.orders"
              :key="order.order_id"
              class="rounded border p-3 hover:bg-gray-50"
            >
              <div class="flex justify-between items-center">
                <div>
                  <div class="font-semibold">Order #{{ order.order_id }}</div>
                  <div class="text-sm text-gray-600">
                    {{ formatDate(order.created_at) }} • {{ order.items.length }} items • Tk.
                    {{ order.total_amount }}
                  </div>
                  <div class="text-xs mt-1">
                    Payment: {{ order.payment_method }} | Status:
                    <span :class="statusClass(order.delivery_status)">{{
                      order.delivery_status
                    }}</span>
                  </div>
                </div>
                <div>
                  <button
                    v-if="canCancelCdsOrder(order)"
                    @click="cancelCdsOrder(order.order_id)"
                    class="bg-red-600 text-white px-3 py-1 rounded text-xs ml-2"
                  >
                    Cancel
                  </button>
                </div>
              </div>
              <ul class="mt-2 ml-2 text-sm text-gray-700">
                <li v-for="item in order.items" :key="item.item_id">
                  {{ item.name }} <span v-if="item.quantity">x{{ item.quantity }}</span> — Tk.
                  {{ item.price }}
                </li>
              </ul>
            </div>
          </div>
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
// Helper to check if CDS order can be cancelled (within 3 mins and not already cancelled)
function canCancelCdsOrder(order) {
  if (!order || order.delivery_status === 'cancelled') return false
  const created = new Date(order.created_at)
  const now = new Date()
  return (now - created) / 1000 < 180 // 3 minutes
}

async function cancelCdsOrder(orderId) {
  if (!confirm('Are you sure you want to cancel this order?')) return
  try {
    const res = await axios.post('/api/cds/cancel_order/', { order_id: orderId })
    if (res.data?.success) {
      await loadCdsOrders()
      alert('Order cancelled.')
    } else {
      alert(res.data?.error || 'Failed to cancel order.')
    }
  } catch (e) {
    alert(e?.response?.data?.error || 'Failed to cancel order.')
  }
}
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { AuthService } from '@/utils/auth.js'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

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
// CDS orders state
const cds = ref({ orders: [], loading: false, error: '' })
async function loadCdsOrders() {
  cds.value.loading = true
  cds.value.error = ''
  try {
    const res = await axios.get('/api/cds/user_orders/')
    cds.value.orders = Array.isArray(res.data.orders) ? res.data.orders : []
  } catch (e) {
    cds.value.error = e?.response?.data?.detail || 'Failed to load CDS orders'
  } finally {
    cds.value.loading = false
  }
}

function statusClass(status) {
  const base = 'px-2 py-1 rounded text-xs capitalize'
  switch ((status || '').toLowerCase()) {
    case 'preparing':
      return base + ' bg-yellow-100 text-yellow-800'
    case 'ready':
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
  const result = await AuthService.getCurrentUser()
  if (!result.success) throw new Error('Not authenticated')
  user.value = result.user
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

    const res = await axios.post('/api/accounts/jwt/update-profile/', data)
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
  } catch (err) {
    router.push({ name: 'login', query: { next: '/profile' } })
    return
  }
  loadLaundryOrders()
  loadCdsOrders()
})
</script>

<style scoped>
details[open] > summary {
  border-bottom: 1px solid #e5e7eb;
}
</style>
