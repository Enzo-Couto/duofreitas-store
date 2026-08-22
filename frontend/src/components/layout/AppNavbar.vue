<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Search, ShoppingBag, Menu } from 'lucide-vue-next'
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()

const links = [
  {
    label: 'Catálogo',
    path: '/catalog',
  },
  {
    label: 'Feminino',
    path: '/catalog?category=feminino',
  },
  {
    label: 'Premium',
    path: '/catalog?category=premium',
  },
]

function openCart() {
  cartStore.isOpen = true
}
</script>

<template>
  <header
    class="fixed top-0 left-0 z-50 w-full border-b border-zinc-200 bg-white/80 backdrop-blur-md"
  >
    <div
      class="mx-auto flex h-20 max-w-7xl items-center justify-between px-6"
    >
      <!-- Logo -->
      <RouterLink
        to="/"
        class="text-xl font-bold tracking-[0.3em]"
      >
        DUO FREITAS
      </RouterLink>

      <!-- Menu Desktop -->
      <nav class="hidden items-center gap-8 lg:flex">
        <RouterLink
          v-for="link in links"
          :key="link.path"
          :to="link.path"
          class="text-sm font-medium uppercase tracking-wider transition hover:opacity-60"
        >
          {{ link.label }}
        </RouterLink>
      </nav>

      <!-- Ações -->
      <div class="flex items-center gap-5">
        <button
          class="cursor-pointer transition hover:opacity-60"
          aria-label="Pesquisar"
        >
          <Search :size="20" />
        </button>

        <button
          @click="openCart"
          class="cursor-pointer relative transition hover:opacity-60"
          aria-label="Carrinho"
        >
          <ShoppingBag :size="20" />

          <span
            v-if="cartStore.totalItems > 0"
            class="absolute -right-2 -top-2 flex h-5 w-5 items-center justify-center rounded-full bg-black text-[10px] font-medium text-white"
          >
            {{ cartStore.totalItems }}
          </span>
        </button>

        <button
          class="lg:hidden transition hover:opacity-60"
          aria-label="Menu"
        >
          <Menu :size="20" />
        </button>
      </div>
    </div>
  </header>
</template>
