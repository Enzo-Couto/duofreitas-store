<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from 'lucide-vue-next'

import AppNavbar from '@/components/layout/AppNavbar.vue'
import ProductCard from '@/components/product/ProductCard.vue'
import ProductQuickView from '@/components/product/ProductQuickView.vue'

import { products } from '@/data/products'

const router = useRouter()

const search = ref('')

const selectedProduct = ref(null)

const filteredProducts = computed(() => {
  if (!search.value.trim()) {
    return products
  }

  return products.filter(product =>
    product.name
      .toLowerCase()
      .includes(search.value.toLowerCase())
  )
})

function openProduct(id: number) {
  router.push(`/product/${id}`)
}

function openQuickView(product: any) {
  selectedProduct.value = product
}

function closeQuickView() {
  selectedProduct.value = null
}
</script>

<template>
  <AppNavbar />

  <main class="mx-auto max-w-7xl px-6 py-32">
    <!-- Cabeçalho -->

    <div class="mb-12">
      <h1 class="text-5xl font-bold">
        Catálogo
      </h1>

      <p class="mt-3 text-zinc-500">
        Explore todos os produtos da Duo Freitas.
      </p>
    </div>

    <!-- Busca -->

    <div
      class="mb-12 flex items-center gap-3 rounded-2xl border border-zinc-200 px-4 py-4"
    >
      <Search :size="20" />

      <input
        v-model="search"
        type="text"
        placeholder="Buscar produtos..."
        class="w-full outline-none"
      />
    </div>

    <!-- Resultado -->

    <div class="mb-8">
      <p class="text-sm text-zinc-500">
        {{ filteredProducts.length }} produto(s)
      </p>
    </div>

    <!-- Produtos -->

    <div
      class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4"
    >
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="cursor-pointer"
        @click="openProduct(product.id)"
      >
          <ProductCard
            :front-image="product.frontImage"
            :back-image="product.backImage"
            :name="product.name"
            :price="`R$ ${product.price.toFixed(2).replace('.', ',')}`"
            @quick-view="openQuickView(product)"
          />
      </div>
    </div>

    <!-- Nenhum produto -->

    <div
      v-if="filteredProducts.length === 0"
      class="py-24 text-center"
    >
      <h2 class="text-2xl font-semibold">
        Nenhum produto encontrado
      </h2>

      <p class="mt-3 text-zinc-500">
        Tente outro termo de busca.
      </p>
    </div>

    <ProductQuickView
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="closeQuickView"
    />
  </main>
</template>
