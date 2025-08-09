<template>
  <nav
    class="sticky top-0 z-50 bg-gradient-to-r from-blue-200 to-indigo-500 shadow flex items-center px-6 py-1"
  >
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between py-4">
        <!-- Back Button -->
        <button
          v-if="showBackButton"
          class="text-gray-900 font-semibold mr-4 hover:underline focus:outline-none"
          @click="router.push('/')"
        >
          ← Back to Home
        </button>

        <!-- Title -->
        <div class="hidden sm:flex sm:items-center">
          <div class="flex items-center space-x-3">
            <img
              v-if="showLogo"
              class="w-10 h-10 rounded-2xl"
              src="https://w1.pngwing.com/pngs/614/143/png-transparent-cloud-symbol-logo-internet-cloud-computing-computer-network-campus-service-provider-recruitment.png"
              alt=""
            />
            <span class="font-bold text-lg text-slate-800 tracking-tight">{{ pageTitle }}</span>
          </div>
        </div>

        <!-- Profile and Cart -->
        <div class="hidden md:block">
          <div class="ml-4 flex items-center md:ml-6">
            <!-- Cart Button -->
            <button v-if="isLoggedIn">
              <a
                href="#"
                class="bg-blue-100 text-black text-sm font-semibold px-4 py-2 rounded-lg mr-4 transition-colors duration-200 hover:bg-blue-500 hover:text-white active:bg-blue-700 active:text-white"
              >
                View Cart
              </a>
            </button>

            <div v-if="!isLoggedIn && showAccountButtons" class="flex space-x-2">
              <router-link
                to="/login"
                class="bg-blue-100 text-black text-sm font-semibold px-4 py-2 rounded-lg transition-colors duration-200 hover:bg-blue-500 hover:text-white active:bg-blue-700 active:text-white"
              >
                Login
              </router-link>
              <router-link
                to="/register"
                class="bg-indigo-800 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors duration-200 hover:bg-indigo-700 active:bg-indigo-800"
              >
                Create Account
              </router-link>
            </div>

            <!-- Profile dropdown (when logged in) -->
            <Menu v-if="isLoggedIn" as="div" class="relative ml-3">
              <div>
                <MenuButton class="flex items-center px-4 py-2 rounded-lg">
                  <img
                    v-if="currentUser.image"
                    class="size-12 rounded-full border-2 border-white transition-colors duration-200 hover:border-black"
                    :src="getProfileImage(currentUser)"
                    alt="Profile"
                  />

                  <div
                    v-else
                    class="size-12 rounded-full border-2 border-white bg-indigo-300 flex items-center justify-center text-xl font-bold text-indigo-800"
                  >
                    {{ currentUser.name ? currentUser.name.charAt(0).toUpperCase() : 'U' }}
                  </div>
                </MenuButton>
              </div>
              <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <MenuItems
                  class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5 focus:outline-hidden"
                >
                  <p class="px-4 py-2 text-m text-gray-900">Hello {{ currentUser.name }}!</p>

                  <MenuItem v-for="item in userNavigation" :key="item.name" v-slot="{ active }">
                    <a
                      :href="item.href"
                      @click.prevent="item.action && item.action()"
                      :class="[
                        active ? 'bg-gray-100 outline-hidden' : '',
                        'block px-4 py-2 text-sm text-gray-700',
                      ]"
                      >{{ item.name }}</a
                    >
                  </MenuItem>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

// Authentication state
const isLoggedIn = ref(false)
const currentUser = ref({})

// Check if user is logged in on component mount
onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    currentUser.value = JSON.parse(storedUser)
    isLoggedIn.value = true
  }
})

// Handle logout
const handleLogout = async () => {
  try {
    await axios.post('/api/accounts/logout/')
    localStorage.removeItem('user')
    isLoggedIn.value = false
    currentUser.value = {}
    router.push('/')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

const getProfilePage = () => {
  router.push('/profile')
}

const userNavigation = [
  { name: 'Your Profile', action: getProfilePage },
  { name: 'Sign out', action: handleLogout },
]

function getProfileImage(user) {
  if (user?.image) {
    return user.image.startsWith('http') ? user.image : `http://127.0.0.1:8000${user.image}`
  }
}

// --- Dynamic Title ---
const pageTitles = {
  '/': 'CampusLink',
  '/login': 'Welcome to Campuslink',
  '/register': 'Welcome to Campuslink',
  '/cds': 'Central Departmental Store',
  '/laundry': 'Laundry',
  '/entrepreneur-hub': 'Entrepreneur Hub',
}
const pageTitle = computed(() => pageTitles[route.path] || 'CampusLink')

// Back button visibility based on route
const showBackButton = computed(() => route.path !== '/')

const showLogo = computed(
  () => route.path === '/' && route.path !== '/login' && route.path !== '/register',
)
const showAccountButtons = computed(() => route.path !== '/login' && route.path !== '/register')
</script>
