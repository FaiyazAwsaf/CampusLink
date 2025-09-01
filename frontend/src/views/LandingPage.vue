<template>
  <NavBar />

  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-blue-50 to-purple-50">
    <!-- Hero -->
    <section class="relative overflow-hidden">
      <div aria-hidden="true" class="absolute inset-0">
        <div
          class="absolute -top-24 -right-16 w-72 h-72 rounded-full bg-indigo-300/30 blur-3xl"
        ></div>
        <div
          class="absolute -bottom-24 -left-16 w-72 h-72 rounded-full bg-blue-300/30 blur-3xl"
        ></div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 relative">
        <div class="grid md:grid-cols-2 gap-10 items-center">
          <div>
            <h1 class="text-4xl md:text-5xl font-extrabold leading-tight text-slate-900">
              All your
              <span
                class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-600"
                >campus services</span
              >
              in one place
            </h1>
            <p class="mt-4 text-lg text-slate-600">
              Discover, manage, and track campus facilities like the Entrepreneur Hub, Laundry, and
              the Central Departmental Store—fast, simple, and seamless.
            </p>

            <div class="mt-6 flex flex-col sm:flex-row gap-3">
              <button
                @click="goToSignup"
                class="px-5 py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 shadow transition"
              >
                Get started
              </button>
              <button
                @click="scrollTo('modules')"
                class="px-5 py-3 rounded-xl font-semibold text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-50 transition"
              >
                Explore modules
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modules -->
    <section id="modules" class="py-12 md:py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-2xl md:text-3xl font-bold text-slate-900">Jump in quickly</h2>
        <p class="text-slate-600 mt-1">Choose a module to get started.</p>

        <div class="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- CDS - Hidden for entrepreneurs -->
          <div
            v-if="!isEntrepreneur"
            class="starting:opacity-0 transition-all duration-500 bg-white rounded-2xl shadow-lg hover:shadow-2xl hover:ring-4 hover:ring-blue-400/40 p-6 flex flex-col items-center m-4"
            @click="$router.push('/cds')"
          >
            <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-4">
              <span class="text-3xl text-blue-600">🏪</span>
            </div>
            <h2 class="text-xl font-bold mb-2 text-gray-800 text-center">
              Central Departmental Store (CDS)
            </h2>
            <p class="text-gray-500 mb-4 text-center">Shop daily essentials and more.</p>
            <button
              class="mt-auto px-4 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-700 transition"
            >
              Explore
            </button>
          </div>

          <!-- Laundry - Hidden for entrepreneurs -->
          <div
            v-if="!isEntrepreneur"
            class="starting:opacity-0 transition-all duration-500 bg-white rounded-2xl shadow-lg hover:shadow-2xl hover:ring-4 hover:ring-green-400/40 p-6 flex flex-col items-center m-4"
            @click="$router.push('/laundry')"
          >
            <div class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <span class="text-3xl text-green-600">🧺</span>
            </div>
            <h2 class="text-xl font-bold mb-2 text-gray-800">Laundry Service</h2>
            <p class="text-gray-500 mb-4 text-center">Laundry made easy.</p>
            <button
              class="mt-auto px-4 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 transition"
            >
              Order Now
            </button>
          </div>

          <!-- Entrepreneur Dashboard - Only for entrepreneurs -->
          <div
            v-if="isEntrepreneur"
            class="starting:opacity-0 transition-all duration-500 bg-white rounded-2xl shadow-lg hover:shadow-2xl hover:ring-4 hover:ring-purple-400/40 p-6 flex flex-col items-center m-4"
            @click="$router.push('/entrepreneur/dashboard')"
          >
            <div class="w-16 h-16 rounded-full bg-purple-100 flex items-center justify-center mb-4">
              <span class="text-3xl text-purple-600">📊</span>
            </div>
            <h2 class="text-xl font-bold mb-2 text-gray-800">My Dashboard</h2>
            <p class="text-gray-500 mb-4 text-center">Manage your storefronts and products.</p>
            <button
              class="mt-auto px-4 py-2 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition"
            >
              Go to Dashboard
            </button>
          </div>

          <!-- E-Hub - Hidden for entrepreneurs, only shown to other users -->
          <div
            v-if="!isEntrepreneur"
            class="starting:opacity-0 transition-all duration-500 bg-white rounded-2xl shadow-lg hover:shadow-2xl hover:ring-4 hover:ring-yellow-400/40 p-6 flex flex-col items-center m-4"
            @click="handleEntrepreneurHubClick"
          >
            <div class="w-16 h-16 rounded-full bg-yellow-100 flex items-center justify-center mb-4">
              <span class="text-3xl text-yellow-600">💡</span>
            </div>
            <h2 class="text-xl font-bold mb-2 text-gray-800">Entrepreneur Hub</h2>
            <p class="text-gray-500 mb-4 text-center">Discover student businesses on campus</p>
            <button
              class="mt-auto px-4 py-2 bg-yellow-500 text-white rounded-xl hover:bg-yellow-600 transition"
            >
              Browse Stores
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section id="features" class="py-12 md:py-16 bg-white/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-2xl md:text-3xl font-bold text-slate-900">Why CampusLink?</h2>
        <p class="text-slate-600 mt-1">Built for students, optimized for campus life.</p>

        <div class="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            class="p-6 rounded-2xl bg-cyan-100 border border-gray-300 hover:shadow-md transition"
          >
            <h3 class="font-semibold text-slate-900">Single Sign-On</h3>
            <p class="text-slate-600 mt-2">One account for all campus modules.</p>
          </div>
          <div
            class="p-6 rounded-2xl bg-cyan-100 border border-gray-300 hover:shadow-md transition"
          >
            <h3 class="font-semibold text-slate-900">Fast & Lightweight</h3>
            <p class="text-slate-600 mt-2">Snappy UI with real-time updates.</p>
          </div>
          <div
            class="p-6 rounded-2xl bg-cyan-100 border border-gray-300 hover:shadow-md transition"
          >
            <h3 class="font-semibold text-slate-900">Admin Friendly</h3>
            <p class="text-slate-600 mt-2">Category & price management in admin.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section id="how" class="py-12 md:py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-2xl md:3xl font-bold text-slate-900">How it works</h2>
        <div class="mt-8 grid md:grid-cols-3 gap-6">
          <div class="p-6 rounded-2xl bg-white border border-slate-100 hover:shadow-md transition">
            <div
              class="size-8 rounded-lg bg-indigo-600 text-white grid place-items-center font-bold"
            >
              1
            </div>
            <h3 class="mt-4 font-semibold text-slate-900">Create your account</h3>
            <p class="text-slate-600 mt-1">Sign up in seconds and keep everything in sync.</p>
          </div>
          <div class="p-6 rounded-2xl bg-white border border-slate-100 hover:shadow-md transition">
            <div
              class="size-8 rounded-lg bg-indigo-600 text-white grid place-items-center font-bold"
            >
              2
            </div>
            <h3 class="mt-4 font-semibold text-slate-900">Pick a service</h3>
            <p class="text-slate-600 mt-1">
              CDS, Laundry, or Entrepreneur Hub—start where you need.
            </p>
          </div>
          <div class="p-6 rounded-2xl bg-white border border-slate-100 hover:shadow-md transition">
            <div
              class="size-8 rounded-lg bg-indigo-600 text-white grid place-items-center font-bold"
            >
              3
            </div>
            <h3 class="mt-4 font-semibold text-slate-900">Track & manage</h3>
            <p class="text-slate-600 mt-1">
              Place orders, view ETAs/invoices, and pick up on time.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="mt-10 border-t bg-white/70">
      <div
        class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-sm text-slate-600 flex flex-col md:flex-row items-center justify-between gap-3"
      >
        <p>© {{ year }} CampusLink. All rights reserved.</p>
        <div class="flex items-center gap-4">
          <a class="hover:text-slate-900 cursor-pointer" @click.prevent="goToLogin">Login</a>
          <a class="hover:text-slate-900 cursor-pointer" @click.prevent="goToSignup"
            >Create account</a
          >
          <a class="hover:text-slate-900 cursor-pointer" @click.prevent="scrollTo('modules')"
            >Modules</a
          >
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const authStore = useAuthStore()
const year = computed(() => new Date().getFullYear())

// Check if user is entrepreneur
const isEntrepreneur = computed(() => authStore.user?.role === 'entrepreneur')

const goToLogin = () => router.push('/login')
const goToSignup = () => router.push('/register')
const goTo = (path) => router.push(path)
const scrollTo = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const handleEntrepreneurHubClick = () => {
  // Entrepreneurs can still view the public entrepreneur hub
  router.push('/entrepreneur-hub')
}
</script>
