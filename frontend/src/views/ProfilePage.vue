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
import { getCurrentUser } from '@/utils/authGuards'
import axios from 'axios'

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
  user.value = getCurrentUser()
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
    const updateData = new FormData()
    updateData.append('name', formData.name)
    updateData.append('phone', formData.phone)
    
    if (formData.image) {
      updateData.append('image', formData.image)
    }

    const response = await axios.post('/api/accounts/update-profile/', updateData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (response.data.success) {
      successMessage.value = 'Profile updated successfully!'
      
      // Update local storage with new user data
      const updatedUser = { ...user.value, ...response.data.user }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      user.value = updatedUser
      
      // Clear form state
      formData.image = null
      imagePreview.value = ''
      if (imageInput.value) {
        imageInput.value.value = ''
      }
    } else {
      if (response.data.errors) {
        errors.value = response.data.errors
      } else {
        errorMessage.value = response.data.error || 'Failed to update profile'
      }
    }
  } catch (error) {
    console.error('Profile update error:', error)
    
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else if (error.response?.data?.error) {
      errorMessage.value = error.response.data.error
    } else {
      errorMessage.value = 'Failed to update profile. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
