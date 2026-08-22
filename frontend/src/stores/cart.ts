import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface CartItem {
  id: number
  name: string
  price: number
  size: string
  quantity: number
  image: string
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>(
    JSON.parse(
      localStorage.getItem('duo-freitas-cart') || '[]'
    )
  )

  const isOpen = ref(false)

  const totalItems = computed(() =>
    items.value.reduce(
      (acc, item) => acc + item.quantity,
      0
    )
  )

  const totalPrice = computed(() =>
    items.value.reduce(
      (acc, item) =>
        acc + item.price * item.quantity,
      0
    )
  )

  function saveCart() {
    localStorage.setItem(
      'duo-freitas-cart',
      JSON.stringify(items.value)
    )
  }

  function addItem(item: CartItem) {
    const existing = items.value.find(
      product =>
        product.id === item.id &&
        product.size === item.size
    )

    if (existing) {
      existing.quantity += item.quantity
    }
    else {
      items.value.push(item)
    }

    saveCart()
  }

  function removeItem(
    id: number,
    size: string
  ) {
    items.value = items.value.filter(
      item =>
        !(
          item.id === id &&
          item.size === size
        )
    )

    saveCart()
  }

  function increaseQuantity(
    id: number,
    size: string
  ) {
    const item = items.value.find(
      item =>
        item.id === id &&
        item.size === size
    )

    if (!item) return

    item.quantity += 1

    saveCart()
  }

  function decreaseQuantity(
    id: number,
    size: string
  ) {
    const item = items.value.find(
      item =>
        item.id === id &&
        item.size === size
    )

    if (!item) return

    if (item.quantity > 1) {
      item.quantity -= 1
    }

    saveCart()
  }

  function updateSize(
    id: number,
    oldSize: string,
    newSize: string
  ) {
    const item = items.value.find(
      product =>
        product.id === id &&
        product.size === oldSize
    )

    if (!item) return

    const existing = items.value.find(
      product =>
        product.id === id &&
        product.size === newSize
    )

    if (existing) {
      existing.quantity += item.quantity

      items.value = items.value.filter(
        product =>
          !(
            product.id === id &&
            product.size === oldSize
          )
      )
    }
    else {
      item.size = newSize
    }

    saveCart()
  }

  function clearCart() {
    items.value = []

    saveCart()
  }

  return {
    items,
    isOpen,

    totalItems,
    totalPrice,

    addItem,
    removeItem,

    increaseQuantity,
    decreaseQuantity,

    updateSize,

    clearCart,
  }
})
