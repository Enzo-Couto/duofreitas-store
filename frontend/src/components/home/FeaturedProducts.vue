<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import ProductCard from '@/components/product/ProductCard.vue'
import ProductQuickView from '@/components/product/ProductQuickView.vue'

import productService from '@/admin/services/productService'

const router = useRouter()

interface Product {
  id: number
  name: string
  price: number
}

const products = ref<Product[]>([])
const selectedProduct = ref<any>(null)

async function loadProducts() {
  try {
    const response =
      await productService.getAll()

    products.value =
      response.data
  } catch (error) {
    console.error(error)
  }
}

function getFrontImage(product: any) {
  const image =
    product.images?.find(
      (img: any) =>
        img.image_type === 'front'
    )

  return image
    ? 'http://127.0.0.1:8000' +
        image.image_url
    : ''
}

function getBackImage(product: any) {
  const image =
    product.images?.find(
      (img: any) =>
        img.image_type === 'back'
    )

  return image
    ? 'http://127.0.0.1:8000' +
        image.image_url
    : getFrontImage(product)
}

function openProduct(product: any) {
  router.push(
    `/product/${product.slug}`
  )
}

function openQuickView(product: any) {
  selectedProduct.value = product
}

function closeQuickView() {
  selectedProduct.value = null
}

onMounted(loadProducts)
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
          @click="openProduct(product)"
          class="cursor-pointer"
        >
            <ProductCard
              :front-image="getFrontImage(product)"
              :back-image="getBackImage(product)"
              :name="product.name"
              :price="`R$ ${Number(product.price).toFixed(2).replace('.', ',')}`"
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
