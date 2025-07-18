<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Create your account</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
            sign in to your existing account
          </router-link>
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister" enctype="multipart/form-data">
        <div class="rounded-md shadow-sm space-y-3">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
            <input
              id="name"
              name="name"
              type="text"
              required
              v-model="name"
              @blur="validateField('name')"
              :class="[
                'appearance-none relative block w-full px-3 py-2 border placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                errors.name ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Full Name"
            />
            <div v-if="errors.name" class="mt-1 text-sm text-red-600">
              <ul class="list-disc list-inside">
                <li v-for="error in errors.name" :key="error">{{ error }}</li>
              </ul>
            </div>
          </div>
          <div>
            <label for="email-address" class="block text-sm font-medium text-gray-700"
              >Email address</label
            >
            <input
              id="email-address"
              name="email"
              type="email"
              autocomplete="email"
              required
              v-model="email"
              @blur="validateField('email')"
              :class="[
                'appearance-none relative block w-full px-3 py-2 border placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                errors.email ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Email address"
            />
            <div v-if="errors.email" class="mt-1 text-sm text-red-600">
              <ul class="list-disc list-inside">
                <li v-for="error in errors.email" :key="error">{{ error }}</li>
              </ul>
            </div>
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="new-password"
              required
              v-model="password"
              @blur="validateField('password')"
              :class="[
                'appearance-none relative block w-full px-3 py-2 border placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                errors.password ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Password"
            />
            <div v-if="errors.password" class="mt-1 text-sm text-red-600">
              <ul class="list-disc list-inside">
                <li v-for="error in errors.password" :key="error">{{ error }}</li>
              </ul>
            </div>
            <div class="mt-1 text-xs text-gray-500">
              Password must be at least 8 characters with uppercase, lowercase, number, and special character.
            </div>
          </div>
          <div>
            <label for="confirm-password" class="block text-sm font-medium text-gray-700"
              >Confirm Password</label
            >
            <input
              id="confirm-password"
              name="confirm-password"
              type="password"
              autocomplete="new-password"
              required
              v-model="confirmPassword"
              @blur="validateField('confirmPassword')"
              :class="[
                'appearance-none relative block w-full px-3 py-2 border placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                errors.confirmPassword ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Confirm Password"
            />
            <div v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">
              <ul class="list-disc list-inside">
                <li v-for="error in errors.confirmPassword" :key="error">{{ error }}</li>
              </ul>
            </div>
          </div>
          <div>
            <label for="phone" class="block text-sm font-medium text-gray-700">Phone Number</label>
            <input
              id="phone"
              name="phone"
              type="tel"
              v-model="phone"
              @blur="validateField('phone')"
              :class="[
                'appearance-none relative block w-full px-3 py-2 border placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                errors.phone ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Phone Number (Optional)"
            />
            <div v-if="errors.phone" class="mt-1 text-sm text-red-600">
              <ul class="list-disc list-inside">
                <li v-for="error in errors.phone" :key="error">{{ error }}</li>
              </ul>
            </div>
            <div class="mt-1 text-xs text-gray-500">
              Format: +8801XXXXXXXXX or 01XXXXXXXXX
            </div>
          </div>
          <div>
            <label for="profile-image" class="block text-sm font-medium text-gray-700"
              >Profile Image</label
            >
            <input
              id="profile-image"
              name="image"
              type="file"
              accept="image/*"
              @change="handleImageChange"
              :class="[
                'appearance-none relative block w-full px-3 py-2 border text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                errors.image ? 'border-red-500' : 'border-gray-300'
              ]"
            />
            <div v-if="errors.image" class="mt-1 text-sm text-red-600">
              <ul class="list-disc list-inside">
                <li v-for="error in errors.image" :key="error">{{ error }}</li>
              </ul>
            </div>
            <div class="mt-1 text-xs text-gray-500">
              Optional. JPG, PNG, GIF up to 5MB
            </div>
            <!-- Image Preview -->
            <div v-if="imagePreview" class="mt-2">
              <img
                :src="imagePreview"
                alt="Profile Preview"
                class="h-24 w-24 object-cover rounded-full"
              />
            </div>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading || !isFormValid"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400 disabled:cursor-not-allowed"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <!-- Heroicon name: solid/user-add -->
              <svg
                class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"
                />
              </svg>
            </span>
            {{ isLoading ? 'Creating account...' : 'Create account' }}
          </button>
        </div>
      </form>

      <!-- Error Alert -->
      <div
        v-if="error"
        class="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
        role="alert"
      >
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <!-- Field Errors Summary -->
      <div
        v-if="Object.keys(errors).length > 0"
        class="mt-4 bg-red-50 border border-red-200 rounded-md p-4"
      >
        <h3 class="text-sm font-medium text-red-800 mb-2">Please fix the following errors:</h3>
        <div class="text-sm text-red-700">
          <div v-for="(fieldErrors, fieldName) in errors" :key="fieldName" class="mb-2">
            <strong>{{ formatFieldName(fieldName) }}:</strong>
            <ul class="list-disc list-inside ml-4">
              <li v-for="error in fieldErrors" :key="error">{{ error }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Form data
const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const phone = ref('')
const image = ref(null)
const imagePreview = ref('')
const error = ref('')
const errors = ref({})
const isLoading = ref(false)

// Form validation utilities
const validateEmail = (email) => {
  const validationErrors = []
  
  if (!email) {
    validationErrors.push('Email is required')
    return validationErrors
  }
  
  email = email.trim().toLowerCase()
  
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!emailRegex.test(email)) {
    validationErrors.push('Please enter a valid email address')
  }
  
  return validationErrors
}

const validatePassword = (password) => {
  const validationErrors = []
  
  if (!password) {
    validationErrors.push('Password is required')
    return validationErrors
  }
  
  if (password.length < 8) {
    validationErrors.push('Password must be at least 8 characters long')
  }
  
  if (!/[A-Z]/.test(password)) {
    validationErrors.push('Password must contain at least one uppercase letter')
  }
  
  if (!/[a-z]/.test(password)) {
    validationErrors.push('Password must contain at least one lowercase letter')
  }
  
  if (!/\d/.test(password)) {
    validationErrors.push('Password must contain at least one number')
  }
  
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    validationErrors.push('Password must contain at least one special character')
  }
  
  const weakPasswords = ['password', '12345678', 'qwerty', 'abc123', 'password123', '123456789', 'admin', 'user']
  if (weakPasswords.includes(password.toLowerCase())) {
    validationErrors.push('Password is too common. Please choose a stronger password')
  }
  
  return validationErrors
}

const validateName = (name) => {
  const validationErrors = []
  
  if (!name) {
    validationErrors.push('Name is required')
    return validationErrors
  }
  
  name = name.trim()
  
  if (name.length < 2) {
    validationErrors.push('Name must be at least 2 characters long')
  }
  
  if (name.length > 255) {
    validationErrors.push('Name must be less than 255 characters long')
  }
  
  if (!/^[a-zA-Z\s.]+$/.test(name)) {
    validationErrors.push('Name can only contain letters, spaces, and dots')
  }
  
  if (name.includes('  ')) {
    validationErrors.push('Name cannot contain consecutive spaces')
  }
  
  if (name.startsWith('.') || name.endsWith('.')) {
    validationErrors.push('Name cannot start or end with a dot')
  }
  
  return validationErrors
}

const validatePhone = (phone) => {
  const validationErrors = []
  
  if (!phone) {
    return validationErrors // Phone is optional
  }
  
  const phoneClean = phone.replace(/[\s-]/g, '')
  const phoneRegex = /^(\+88)?01[0-9]{9}$/
  
  if (!phoneRegex.test(phoneClean)) {
    validationErrors.push('Phone number must be in the format: +8801XXXXXXXXX or 01XXXXXXXXX')
  }
  
  return validationErrors
}

const validateImage = (file) => {
  const validationErrors = []
  
  if (!file) {
    return validationErrors // Image is optional
  }
  
  const maxSize = 5 * 1024 * 1024 // 5MB
  if (file.size > maxSize) {
    validationErrors.push('Image file size cannot exceed 5MB')
  }
  
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    validationErrors.push('Only JPG, JPEG, PNG, and GIF image files are allowed')
  }
  
  return validationErrors
}

// Validate entire form
const validateForm = () => {
  const formErrors = {}
  
  // Validate email
  const emailErrors = validateEmail(email.value)
  if (emailErrors.length > 0) {
    formErrors.email = emailErrors
  }
  
  // Validate password
  const passwordErrors = validatePassword(password.value)
  if (passwordErrors.length > 0) {
    formErrors.password = passwordErrors
  }
  
  // Validate confirm password
  if (password.value !== confirmPassword.value) {
    formErrors.confirmPassword = ['Passwords do not match']
  }
  
  // Validate name
  const nameErrors = validateName(name.value)
  if (nameErrors.length > 0) {
    formErrors.name = nameErrors
  }
  
  // Validate phone
  const phoneErrors = validatePhone(phone.value)
  if (phoneErrors.length > 0) {
    formErrors.phone = phoneErrors
  }
  
  // Validate image
  const imageErrors = validateImage(image.value)
  if (imageErrors.length > 0) {
    formErrors.image = imageErrors
  }
  
  return formErrors
}

// Form validation computed property
const isFormValid = computed(() => {
  const formErrors = validateForm()
  return Object.keys(formErrors).length === 0 && 
         name.value.trim() !== '' && 
         email.value.trim() !== '' && 
         password.value.trim() !== '' && 
         confirmPassword.value.trim() !== ''
})

// Real-time validation
const validateField = (field) => {
  const currentErrors = { ...errors.value }
  
  switch (field) {
    case 'email':
      const emailErrors = validateEmail(email.value)
      if (emailErrors.length > 0) {
        currentErrors.email = emailErrors
      } else {
        delete currentErrors.email
      }
      break
    case 'password':
      const passwordErrors = validatePassword(password.value)
      if (passwordErrors.length > 0) {
        currentErrors.password = passwordErrors
      } else {
        delete currentErrors.password
      }
      break
    case 'confirmPassword':
      if (password.value !== confirmPassword.value) {
        currentErrors.confirmPassword = ['Passwords do not match']
      } else {
        delete currentErrors.confirmPassword
      }
      break
    case 'name':
      const nameErrors = validateName(name.value)
      if (nameErrors.length > 0) {
        currentErrors.name = nameErrors
      } else {
        delete currentErrors.name
      }
      break
    case 'phone':
      const phoneErrors = validatePhone(phone.value)
      if (phoneErrors.length > 0) {
        currentErrors.phone = phoneErrors
      } else {
        delete currentErrors.phone
      }
      break
  }
  
  errors.value = currentErrors
}

// Helper function to format field names
const formatFieldName = (fieldName) => {
  return fieldName
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .replace('Email', 'Email Address')
    .replace('ConfirmPassword', 'Confirm Password')
    .replace('Phone', 'Phone Number')
    .replace('Image', 'Profile Image')
}

// Handle image upload
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validate image before setting
    const imageErrors = validateImage(file)
    if (imageErrors.length > 0) {
      const currentErrors = { ...errors.value }
      currentErrors.image = imageErrors
      errors.value = currentErrors
      return
    }
    
    // Clear image errors if validation passes
    const currentErrors = { ...errors.value }
    delete currentErrors.image
    errors.value = currentErrors
    
    image.value = file
    // Create preview URL
    imagePreview.value = URL.createObjectURL(file)
  }
}

// Register handler
const handleRegister = async () => {
  // Reset errors
  error.value = ''
  errors.value = {}

  // Validate entire form
  const formErrors = validateForm()
  if (Object.keys(formErrors).length > 0) {
    errors.value = formErrors
    return
  }

  isLoading.value = true

  try {
    // Create form data for file upload
    const formData = new FormData()
    formData.append('name', name.value.trim())
    formData.append('email', email.value.trim().toLowerCase())
    formData.append('password', password.value)
    if (phone.value.trim()) {
      formData.append('phone', phone.value.trim())
    }

    if (image.value) {
      formData.append('image', image.value)
    }

    const response = await axios.post('/api/accounts/register/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (response.data.success) {
      // Store user data in localStorage
      localStorage.setItem('user', JSON.stringify(response.data.user))

      // Redirect to home page
      router.push('/home')
    } else {
      // Handle validation errors from backend
      if (response.data.errors) {
        errors.value = response.data.errors
      } else {
        error.value = response.data.error || 'Registration failed. Please try again.'
      }
    }
  } catch (err) {
    console.error('Registration error:', err)
    
    // Handle backend validation errors
    if (err.response?.data?.errors) {
      errors.value = err.response.data.errors
    } else if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
