<template>
  <div class="home">
    <h1>CampusLink</h1>
    <div class="service-cards">
      <div class="card" @click="$router.push('/entrepreneur-hub')">
        <h3>Entrepreneur Hub</h3>
        <p>Student-run businesses</p>
      </div>
      <div class="card" @click="$router.push('/department-store')">
        <h3>Department Store</h3>
        <p>Campus store items</p>
      </div>
      <div class="card" @click="$router.push('/laundry')">
        <h3>Laundry Service</h3>
        <p>Book laundry services</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
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
</style>