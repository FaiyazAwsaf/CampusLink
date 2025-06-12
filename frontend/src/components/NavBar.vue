<template>
  <nav
    class="sticky top-0 z-50 bg-gradient-to-r from-blue-800 to-indigo-900 shadow flex items-center px-6 py-4"
  >
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between py-4">
        <!-- Back Button -->
        <button
          class="text-white font-semibold mr-4 hover:underline focus:outline-none"
          @click="$router.push('/')"
        >
          ← Back to Home
        </button>

        <!-- Title -->
        <div class="hidden sm:flex sm:items-center">
          <h1 class="text-2xl font-bold text-white">Central Departmental Store</h1>
        </div>
        <!-- Profile and Settings -->
        <div class="hidden sm:flex sm:items-center">
          <a
            href="#"
            class="bg-blue-100 text-black text-sm font-semibold px-4 py-2 rounded-lg mr-4 transition-colors duration-200 hover:bg-blue-500 hover:text-white active:bg-blue-700 active:text-white"
          >
            Profile
          </a>
          <a
            href="#"
            class="bg-blue-100 text-black text-sm font-semibold px-4 py-2 rounded-lg mr-4 transition-colors duration-200 hover:bg-blue-500 hover:text-white active:bg-blue-700 active:text-white"
          >
            Settings
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<!-- Header -->
<!-- <div class="bg-gradient-to-r from-blue-800 to-indigo-900 shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="$router.push('/')"
              class="flex items-center text-white hover:text-gray-900 transition-colors"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              Back to Home
            </button>
          </div>
          <h1 class="text-2xl font-bold text-white">Central Departmental Store</h1>
          <div class="w-24"></div> 
        </div>
      </div>
    </div> -->
