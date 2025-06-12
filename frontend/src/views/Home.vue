<template>
  <TitleBar />
  <div class="min-h-screen bg-[#e5f3ff] flex flex-col items-center justify-center py-8">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-5xl">
      <!-- Card Example Start -->
      <div class="bg-white rounded-2xl shadow-lg hover:shadow-2xl hover:ring-4 hover:ring-blue-400/40 transition-all duration-300 p-6 flex flex-col items-center m-4" @click="$router.push('/cds')">
        <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-4">
          <span class="text-3xl text-blue-600">🏪</span>
        </div>
        <h2 class="text-xl font-bold mb-2 text-gray-800 text-center">Central Departmental Store (CDS)</h2>
        <p class="text-gray-500 mb-4 text-center">Shop daily essentials and more.</p>
        <button class="mt-auto px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition">Explore</button>
      </div>
      <!-- Card Example End -->

      <div class="bg-white rounded-2xl shadow-lg hover:shadow-2xl hover:ring-4 hover:ring-green-400/40 transition-all duration-300 p-6 flex flex-col items-center m-4">
        <div class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-4">
          <span class="text-3xl text-green-600">🧺</span>
        </div>
        <h2 class="text-xl font-bold mb-2 text-gray-800">Laundry Service</h2>
        <p class="text-gray-500 mb-4 text-center">Laundry made easy.</p>
        <button class="mt-auto px-4 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 transition">Order Now</button>
      </div>

      <div class="bg-white rounded-2xl shadow-lg hover:shadow-2xl hover:ring-4 hover:ring-yellow-400/40 transition-all duration-300 p-6 flex flex-col items-center m-4">
        <div class="w-16 h-16 rounded-full bg-yellow-100 flex items-center justify-center mb-4">
          <span class="text-3xl text-yellow-600">💡</span>
        </div>
        <h2 class="text-xl font-bold mb-2 text-gray-800">Entrepreneur Hub</h2>
        <p class="text-gray-500 mb-4 text-center">Discover student businesses on campus.</p>
        <button class="mt-auto px-4 py-2 bg-yellow-500 text-white rounded-xl hover:bg-yellow-600 transition">Browse Stores</button>
      </div>
    </div>
  </div>
</template>


<script setup>
  import TitleBar from '@/components/TitleBar.vue'
</script>

<!-- <style scoped>
.service-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style> -->