<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import AppNavbar from '@/components/layout/AppNavbar.vue'
import ProductCard from '@/components/product/ProductCard.vue'

import { useCartStore } from '@/stores/cart'
import { products } from '@/data/products'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()

const product = products.find(
  p => p.id === Number(route.params.id)
)

if (!product) {
  throw new Error('Produto não encontrado')
}

const currentProduct = product

const relatedProducts = products
  .filter(p => p.id !== currentProduct.id)
  .slice(0, 4)

const quantity = ref(1)

const selectedImage = ref(currentProduct.frontImage)

const sizes = ['P', 'M', 'G', 'GG']

const selectedSize = ref('M')

const isAnimatingToCart = ref(false)

function openProduct(productId: number) {
  router.push(`/product/${productId}`)
}

function addToCart() {
  cartStore.addItem({
    id: currentProduct.id,
    name: currentProduct.name,
    price: currentProduct.price,
    size: selectedSize.value,
    quantity: quantity.value,
    image: currentProduct.frontImage,
  })

  isAnimatingToCart.value = true

  setTimeout(() => {
    isAnimatingToCart.value = false
  }, 800)
}
</script>

<template>
  <AppNavbar />

  <main class="mx-auto max-w-7xl px-6 py-32">
    <div class="grid gap-12 lg:grid-cols-2">

      <!-- Galeria -->

      <div class="grid gap-4 lg:grid-cols-[120px_1fr]">
        <div class="flex gap-3 lg:flex-col">
          <button
            @click="selectedImage = currentProduct.frontImage"
            class="cursor-pointer overflow-hidden rounded-2xl border-2 transition"
            :class="
              selectedImage === currentProduct.frontImage
                ? 'border-black'
                : 'border-zinc-200'
            "
          >
            <img
              :src="currentProduct.frontImage"
              alt="Frente"
              class="h-28 w-28 object-cover"
            />
          </button>

          <button
            @click="selectedImage = currentProduct.backImage"
            class="cursor-pointer overflow-hidden rounded-2xl border-2 transition"
            :class="
              selectedImage === currentProduct.backImage
                ? 'border-black'
                : 'border-zinc-200'
            "
          >
            <img
              :src="currentProduct.backImage"
              alt="Costas"
              class="h-28 w-28 object-cover"
            />
          </button>
        </div>

        <div
          class="overflow-hidden rounded-3xl bg-zinc-100"
        >
          <img
            :src="selectedImage"
            :alt="currentProduct.name"
            class="w-full transition duration-500 hover:scale-105"
          />
        </div>
      </div>

      <!-- Informações -->

      <div>
        <h1 class="text-5xl font-bold">
          {{ currentProduct.name }}
        </h1>

        <p class="mt-4 text-3xl font-semibold">
          R$ {{ currentProduct.price.toFixed(2).replace('.', ',') }}
        </p>

        <div class="mt-10">
          <h3 class="mb-4 font-medium">
            Tamanho
          </h3>

          <div class="flex gap-3">
            <button
              v-for="size in sizes"
              :key="size"
              @click="selectedSize = size"
              class="h-12 w-12 cursor-pointer rounded-xl border"
              :class="{
                'border-black bg-black text-white':
                  selectedSize === size,
              }"
            >
              {{ size }}
            </button>
          </div>

          <div class="mt-8">
            <h3 class="mb-4 font-medium">
              Quantidade
            </h3>

            <div
              class="flex w-fit items-center rounded-xl border border-zinc-200"
            >
              <button
                class="cursor-pointer px-4 py-3"
                @click="quantity > 1 && quantity--"
              >
                −
              </button>

              <span class="px-6">
                {{ quantity }}
              </span>

              <button
                class="cursor-pointer px-4 py-3"
                @click="quantity++"
              >
                +
              </button>
            </div>
          </div>
        </div>

        <button
          @click="addToCart"
          class="mt-10 w-full cursor-pointer rounded-xl bg-black py-4 text-white transition hover:bg-zinc-800"
        >
          Adicionar ao Carrinho
        </button>

        <div class="mt-8 space-y-3 text-sm text-zinc-600">
          <p>✓ Frete grátis acima de R$299</p>
          <p>✓ Envio para todo Brasil</p>
          <p>✓ Troca facilitada em até 7 dias</p>
          <p>✓ Pagamento seguro</p>
        </div>

        <div
          class="mt-12 border-t pt-8 text-zinc-600"
        >
          <p>
            {{ currentProduct.description }}
          </p>
        </div>
      </div>
    </div>

    <!-- Produtos Relacionados -->

    <section class="mt-32">
      <div class="mb-10">
        <h2 class="text-4xl font-bold">
          Você também pode gostar
        </h2>

        <p class="mt-2 text-zinc-500">
          Descubra outros produtos da coleção Duo Freitas.
        </p>
      </div>

      <div
        class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4"
      >
        <div
          v-for="relatedProduct in relatedProducts"
          :key="relatedProduct.id"
          class="cursor-pointer"
          @click="openProduct(relatedProduct.id)"
        >
          <ProductCard
            :front-image="relatedProduct.frontImage"
            :back-image="relatedProduct.backImage"
            :name="relatedProduct.name"
            :price="`R$ ${relatedProduct.price.toFixed(2).replace('.', ',')}`"
          />
        </div>
      </div>
    </section>

    <!-- Animação -->

    <Transition name="fly-to-cart">
      <img
        v-if="isAnimatingToCart"
        :src="selectedImage"
        :alt="currentProduct.name"
        class="pointer-events-none fixed top-1/2 left-1/2 z-999 h-32 w-32 -translate-x-1/2 -translate-y-1/2 rounded-2xl object-cover"
      />
    </Transition>
  </main>
</template>

<style scoped>
.fly-to-cart-enter-active {
  animation: flyToCart 0.8s ease-in-out;
}

@keyframes flyToCart {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }

  100% {
    transform: translate(500px, -400px) scale(0.1);
    opacity: 0;
  }
}
</style>
