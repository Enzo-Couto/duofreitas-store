<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import AppNavbar from '@/components/layout/AppNavbar.vue'

import { useCartStore } from '@/stores/cart'
import productService from '@/admin/services/productService'

const route = useRoute()
const cartStore = useCartStore()

const currentProduct = ref<any>(null)

const quantity = ref(1)
const selectedImage = ref('')
const selectedSize = ref('M')

const sizes = ['P', 'M', 'G', 'GG']

const isAnimatingToCart = ref(false)

async function loadProduct() {
  try {
    const response = await productService.getBySlug(
      route.params.slug as string
    )

    currentProduct.value = response.data

    if (
      currentProduct.value.images &&
      currentProduct.value.images.length
    ) {
      selectedImage.value =
        'http://127.0.0.1:8000' +
        currentProduct.value.images[0].image_url
    }
  } catch (error) {
    console.error(error)
  }
}

function addToCart() {
  if (!currentProduct.value) {
    return
  }

  cartStore.addItem({
    id: currentProduct.value.id,
    name: currentProduct.value.name,
    price: currentProduct.value.price,
    size: selectedSize.value,
    quantity: quantity.value,
    image: selectedImage.value
  })

  isAnimatingToCart.value = true

  setTimeout(() => {
    isAnimatingToCart.value = false
  }, 800)
}

onMounted(loadProduct)
</script>

<template>
  <AppNavbar />

  <main
    v-if="currentProduct"
    class="mx-auto max-w-7xl px-6 py-32"
  >
    <div class="grid gap-12 lg:grid-cols-2">

      <!-- Galeria -->

      <div class="grid gap-4 lg:grid-cols-[120px_1fr]">
        <div class="flex gap-3 lg:flex-col">
            <button
              v-for="image in currentProduct.images"
              :key="image.id"
              @click="
                selectedImage =
                  'http://127.0.0.1:8000' +
                  image.image_url
              "
              class="cursor-pointer overflow-hidden rounded-2xl border-2 transition"
              :class="
                selectedImage ===
                'http://127.0.0.1:8000' + image.image_url
                  ? 'border-black'
                  : 'border-zinc-200'
              "
            >
              <img
                :src="
                  'http://127.0.0.1:8000' +
                  image.image_url
                "
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
          R$ {{ Number(currentProduct.price).toFixed(2).replace('.', ',') }}
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
