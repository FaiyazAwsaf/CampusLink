<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-200"
  >
    <div
      class="max-w-lg w-full mx-auto bg-white rounded-3xl shadow-2xl p-10 flex flex-col items-center space-y-8"
    >
      <!-- Logo & Title -->
      <div class="flex flex-col items-center">
        <div
          class="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-400 to-blue-600 flex items-center justify-center mb-4 shadow-lg"
        >
          <span class="text-3xl font-bold text-white">CL</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-bold text-indigo-800 tracking-tight mb-2">
          Welcome to CampusLink
        </h1>
        <p class="text-lg text-indigo-600 text-center">
          Discover, Shop, and Connect with all Campus Businesses!
        </p>
      </div>

      <!-- Buttons -->
      <div class="w-full flex flex-col md:flex-row md:space-x-6 space-y-4 md:space-y-0 mt-4">
        <button
          @click="goToLogin"
          class="flex-1 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-blue-600 text-white font-semibold text-lg shadow hover:from-indigo-600 hover:to-blue-700 transition"
        >
          Login
        </button>
        <button
          @click="goToSignup"
          class="flex-1 py-3 rounded-xl border border-indigo-400 text-indigo-700 font-semibold text-lg bg-white shadow hover:bg-indigo-50 hover:text-indigo-900 transition"
        >
          Create Account
        </button>
      </div>

      <!-- Optional: Divider -->
      <div class="flex items-center justify-center w-full mt-6">
        <span class="h-px flex-1 bg-gray-200"></span>
        <span class="px-4 text-gray-400 font-semibold">or</span>
        <span class="h-px flex-1 bg-gray-200"></span>
      </div>

      <!-- Demo Info / Marketing (optional) -->
      <div class="w-full text-center text-gray-500 text-sm mt-2">
        <span>New to CampusLink? Join today and unlock exclusive campus deals!</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push('/login')
}

const goToSignup = () => {
  router.push('/register')
}
</script>
