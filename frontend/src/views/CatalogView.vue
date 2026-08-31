<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from 'lucide-vue-next'

import AppNavbar from '@/components/layout/AppNavbar.vue'
import ProductCard from '@/components/product/ProductCard.vue'
import ProductQuickView from '@/components/product/ProductQuickView.vue'

import productService from '@/admin/services/productService'

const router = useRouter()

const search = ref('')

const selectedProduct = ref<any>(null)

const products = ref<any[]>([])

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

const filteredProducts = computed(() => {
  if (!search.value.trim()) {
    return products.value
  }

  return products.value.filter(product =>
    product.name
      .toLowerCase()
      .includes(
        search.value.toLowerCase()
      )
  )
})

const productsByCategory = computed(() => {
  const groups: Record<
    string,
    any[]
  > = {}

  filteredProducts.value.forEach(
    product => {

      const category =
        product.category?.name ||
        'Sem categoria'

      if (!groups[category]) {
        groups[category] = []
      }

      groups[category].push(
        product
      )
    }
  )

  return groups
})

function getFrontImage(
  product: any
) {
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

function getBackImage(
  product: any
) {
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

function openProduct(
  product: any
) {
  router.push(
    `/product/${product.slug}`
  )
}

function openQuickView(
  product: any
) {
  selectedProduct.value =
    product
}

function closeQuickView() {
  selectedProduct.value =
    null
}

onMounted(
  loadProducts
)
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
      v-for="(categoryProducts, categoryName) in productsByCategory"
      :key="categoryName"
      class="mb-20"
    >
      <h2
        class="mb-8 border-b pb-3 text-3xl font-bold"
      >
        {{ categoryName }}
      </h2>

      <div
        class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4"
      >
        <div
          v-for="product in categoryProducts"
          :key="product.id"
          class="cursor-pointer"
          @click="openProduct(product)"
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
