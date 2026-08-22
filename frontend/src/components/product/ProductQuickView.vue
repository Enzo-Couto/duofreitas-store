<script setup lang="ts">
import { ref, watch } from 'vue'
import { X } from 'lucide-vue-next'

import { useCartStore } from '@/stores/cart'

interface Product {
  id: number
  name: string
  price: number
  frontImage: string
  backImage: string
}

const props = defineProps<{
  product: Product
}>()

const emit = defineEmits<{
  close: []
}>()

const cartStore = useCartStore()

const selectedSize = ref('M')
const quantity = ref(1)
const selectedImage = ref('')

watch(
  () => props.product,
  (product) => {
    if (product) {
      selectedImage.value = product.frontImage
      selectedSize.value = 'M'
      quantity.value = 1
    }
  },
  { immediate: true }
)

function addToCart() {
  cartStore.addItem({
    id: props.product.id,
    name: props.product.name,
    price: props.product.price,
    size: selectedSize.value,
    quantity: quantity.value,
    image: props.product.frontImage,
  })

  emit('close')
}
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed inset-0 z-999 flex items-center justify-center bg-black/60 p-4"
      @click.self="emit('close')"
    >
      <div
        class="relative max-h-[90vh] w-full max-w-5xl overflow-y-auto rounded-3xl bg-white"
      >
        <!-- Fechar -->

        <button
          class="cursor-pointer absolute top-5 right-5 z-10 rounded-full p-2 transition hover:bg-zinc-100"
          @click="emit('close')"
        >
          <X :size="24" />
        </button>

        <div
          class="grid gap-8 p-8 lg:grid-cols-2"
        >
          <!-- Imagens -->

          <div>
            <div
              class="overflow-hidden rounded-3xl bg-zinc-100"
            >
              <img
                :src="selectedImage"
                :alt="product.name"
                class="w-full"
              />
            </div>

            <div class="mt-4 flex gap-3">
              <button
                class="overflow-hidden rounded-xl border-2"
                :class="
                  selectedImage === product.frontImage
                    ? 'border-black'
                    : 'border-zinc-200'
                "
                @click="selectedImage = product.frontImage"
              >
                <img
                  :src="product.frontImage"
                  alt="Frente"
                  class="h-24 w-24 object-cover"
                />
              </button>

              <button
                class="overflow-hidden rounded-xl border-2"
                :class="
                  selectedImage === product.backImage
                    ? 'border-black'
                    : 'border-zinc-200'
                "
                @click="selectedImage = product.backImage"
              >
                <img
                  :src="product.backImage"
                  alt="Costas"
                  class="h-24 w-24 object-cover"
                />
              </button>
            </div>
          </div>

          <!-- Informações -->

          <div>
            <h2
              class="text-4xl font-bold"
            >
              {{ product.name }}
            </h2>

            <p
              class="mt-4 text-3xl font-semibold"
            >
                R$ {{ product.price.toFixed(2).replace('.', ',') }}
            </p>

            <!-- Tamanhos -->

            <div class="mt-10">
              <h3
                class="mb-4 font-medium"
              >
                Tamanho
              </h3>

              <div class="flex gap-3">
                <button
                  v-for="size in ['P', 'M', 'G', 'GG']"
                  :key="size"
                  class="cursor-pointer h-12 w-12 rounded-xl border transition"
                  :class="
                    selectedSize === size
                      ? 'border-black bg-black text-white'
                      : 'border-zinc-300'
                  "
                  @click="selectedSize = size"
                >
                  {{ size }}
                </button>
              </div>
            </div>

            <!-- Quantidade -->

            <div class="mt-8">
              <h3
                class="mb-4 font-medium"
              >
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

            <!-- Benefícios -->

            <div
              class="mt-8 space-y-2 text-sm text-zinc-500"
            >
              <p>✓ Frete grátis acima de R$299</p>
              <p>✓ Envio para todo Brasil</p>
              <p>✓ Troca facilitada em até 7 dias</p>
              <p>✓ Pagamento seguro</p>
            </div>

            <!-- Botão -->

            <button
              class="cursor-pointer mt-10 w-full rounded-xl bg-black py-4 text-white transition hover:bg-zinc-800"
              @click="addToCart"
            >
              Adicionar ao Carrinho
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
