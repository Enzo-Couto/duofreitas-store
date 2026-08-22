<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import ProductCard from '@/components/product/ProductCard.vue'
import ProductQuickView from '@/components/product/ProductQuickView.vue'

import { products } from '@/data/products'

const router = useRouter()

const selectedProduct = ref<any>(null)

function openProduct(productId: number) {
  router.push(`/product/${productId}`)
}

function openQuickView(product: any) {
  selectedProduct.value = product
}

function closeQuickView() {
  selectedProduct.value = null
}
</script>

<template>
  <section class="py-24">
    <div class="mx-auto max-w-7xl px-6">
      <div
        class="mb-12 flex items-center justify-between"
      >
        <h2 class="text-4xl font-bold">
          Destaques
        </h2>

        <button
          class="text-sm uppercase tracking-widest text-zinc-500"
        >
          Ver todos
        </button>
      </div>

      <div
        class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4"
      >
        <div
          v-for="product in products"
          :key="product.id"
          @click="openProduct(product.id)"
          class="cursor-pointer"
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
    </div>

    <ProductQuickView
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="closeQuickView"
    />
  </section>
</template>
