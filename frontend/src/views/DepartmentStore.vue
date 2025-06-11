<template>
  <div class="department-store">
    <h1>Central Department Store</h1>
    
    <div v-if="loading" class="loading">
      Loading items...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else class="items-grid">
      <div v-for="item in items" :key="item.item_id" class="item-card">
        <h3>{{ item.name }}</h3>
        <p class="description">{{ item.description }}</p>
        <p class="price">${{ item.price }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// State variables using Composition API
const items = ref([])
const loading = ref(true)
const error = ref(null)

// Fetch data from the backend API
const fetchItems = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/cds/items/')
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    items.value = data.items
  } catch (err) {
    error.value = `Failed to load items: ${err.message}`
    console.error('Error fetching CDS items:', err)
  } finally {
    loading.value = false
  }
}

// Fetch data when component is mounted
onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
.department-store {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  margin: 40px 0;
  font-size: 18px;
}

.error {
  color: #e74c3c;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.item-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.item-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.item-card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.description {
  color: #555;
  margin-bottom: 15px;
}

.price {
  font-weight: bold;
  font-size: 18px;
  color: #124085;
}
</style>