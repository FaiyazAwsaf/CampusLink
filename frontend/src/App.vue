<template>
  <div id="app">
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth.js'

const authStore = useAuthStore()

onMounted(() => {
  // Initialize authentication state on app startup
  authStore.initializeAuth()
})
</script>
