<!-- <script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
  </header>

  <RouterView />
</template>


<style scoped>

</style> -->

<template>
  <div id="app">
    <main>
      <router-view /> <!-- Where other pages/components render -->
    </main>
  </div>
</template>

<script setup>
// No or minimal logic here unless global
</script>