import { ref, computed, watch } from 'vue'

const CART_KEY = 'campuslink_cart'

const cart = ref([])

// Load cart from localStorage
function loadCart() {
  const saved = localStorage.getItem(CART_KEY)
  if (saved) {
    try {
      cart.value = JSON.parse(saved)
    } catch {
      cart.value = []
    }
  }
}

// Save cart to localStorage
function saveCart() {
  localStorage.setItem(CART_KEY, JSON.stringify(cart.value))
}

// Add item to cart
function addToCart(item, type) {
  // Prevent duplicates by id+type
  const exists = cart.value.find((i) => i.item_id === item.item_id && i.type === type)
  if (!exists) {
    cart.value.push({ ...item, type })
    saveCart()
  }
}

// Remove item from cart
function removeFromCart(item_id, type) {
  cart.value = cart.value.filter((i) => !(i.item_id === item_id && i.type === type))
  saveCart()
}

// Clear cart
function clearCart() {
  cart.value = []
  saveCart()
}

// Grouped items
const cdsItems = computed(() => cart.value.filter((i) => i.type === 'cds'))
const entrepreneurItems = computed(() => cart.value.filter((i) => i.type === 'entrepreneur'))

// Watch for changes
watch(cart, saveCart, { deep: true })

loadCart()

export default function useCart() {
  return {
    cart,
    addToCart,
    removeFromCart,
    clearCart,
    cdsItems,
    entrepreneurItems,
  }
}
