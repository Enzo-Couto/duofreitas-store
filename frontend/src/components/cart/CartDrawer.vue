<script setup lang="ts">
import { X, Trash2 } from 'lucide-vue-next'

import { useCartStore } from '@/stores/cart'

import { useRouter } from 'vue-router'

const router = useRouter()

const cartStore = useCartStore()

function closeCart() {
  cartStore.isOpen = false
}

function formatPrice(value: number) {
  return value.toFixed(2).replace('.', ',')
}

function goToCheckout() {
  closeCart()
  router.push('/checkout')
}
</script>

<template>
  <Teleport to="body">

    <!-- Overlay -->

    <div
      v-if="cartStore.isOpen"
      class="fixed inset-0 z-90 bg-black/40"
      @click="closeCart"
    />

    <!-- Drawer -->

    <aside
      class="fixed top-0 right-0 z-100 flex h-screen w-full max-w-lg flex-col bg-white shadow-2xl transition-transform duration-300"
      :class="
        cartStore.isOpen
          ? 'translate-x-0'
          : 'translate-x-full'
      "
    >
      <!-- Header -->

      <div
        class="flex items-center justify-between border-b p-6"
      >
        <h2 class="text-xl font-bold">
          Carrinho
        </h2>

        <button
          @click="closeCart"
          class="cursor-pointer"
        >
          <X :size="24" />
        </button>
      </div>

      <!-- Produtos -->

      <div class="flex-1 overflow-y-auto p-6">
        <div
          v-if="cartStore.items.length === 0"
          class="mt-20 text-center text-zinc-500"
        >
          Seu carrinho está vazio.
        </div>

        <div
          v-for="item in cartStore.items"
          :key="`${item.id}-${item.size}`"
          class="mb-4 rounded-2xl bg-zinc-50 p-4"
        >
          <div class="flex gap-4">
            <!-- Imagem -->

            <img
              :src="item.image"
              :alt="item.name"
              class="h-24 w-24 rounded-xl object-cover"
            />

            <!-- Conteúdo -->

            <div class="flex flex-1 flex-col justify-between">
              <!-- Topo -->

              <div class="flex items-start justify-between">
                <div>
                  <h3 class="font-semibold">
                    {{ item.name }}
                  </h3>

                  <p class="mt-1 text-sm text-zinc-500">
                    R$ {{ formatPrice(item.price) }} cada
                  </p>
                </div>

                <button
                  @click="
                    cartStore.removeItem(
                      item.id,
                      item.size
                    )
                  "
                  class="cursor-pointer text-zinc-400 transition hover:text-red-500"
                >
                  <Trash2 :size="18" />
                </button>
              </div>

              <!-- Controles -->

              <div
                class="mt-4 flex items-center justify-between"
              >
                <div class="flex items-center gap-3">
                  <!-- Tamanho -->

                  <select
                    :value="item.size"
                    @change="
                      cartStore.updateSize(
                        item.id,
                        item.size,
                        ($event.target as HTMLSelectElement).value
                      )
                    "
                    class="rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm"
                  >
                    <option value="P">P</option>
                    <option value="M">M</option>
                    <option value="G">G</option>
                    <option value="GG">GG</option>
                  </select>

                  <!-- Quantidade -->

                  <div
                    class="flex items-center rounded-lg border border-zinc-200 bg-white"
                  >
                    <button
                      class="cursor-pointer px-3 py-2"
                      @click="
                        cartStore.decreaseQuantity(
                          item.id,
                          item.size
                        )
                      "
                    >
                      −
                    </button>

                    <span class="px-3 text-sm">
                      {{ item.quantity }}
                    </span>

                    <button
                      class="cursor-pointer px-3 py-2"
                      @click="
                        cartStore.increaseQuantity(
                          item.id,
                          item.size
                        )
                      "
                    >
                      +
                    </button>
                  </div>
                </div>

                <!-- Subtotal -->

                <div class="text-right">
                  <p class="text-xs text-zinc-500">
                    Subtotal
                  </p>

                  <p class="text-lg font-bold">
                    R$
                    {{
                      formatPrice(
                        item.price * item.quantity
                      )
                    }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->

      <div class="border-t p-6">
        <div
          class="mb-4 flex items-center justify-between"
        >
          <span class="text-zinc-600">
            Total
          </span>

          <span class="text-xl font-bold">
            R$
            {{
              formatPrice(
                cartStore.totalPrice
              )
            }}
          </span>
        </div>

        <button
          v-if="cartStore.items.length > 0"
          @click="cartStore.clearCart()"
          class="mb-3 w-full cursor-pointer rounded-xl border border-zinc-300 py-3 transition hover:bg-zinc-100"
        >
          Limpar Carrinho
        </button>

        <button
          @click="goToCheckout"
          class="w-full cursor-pointer rounded-xl bg-black py-4 text-white transition hover:bg-zinc-800"
        >
          Finalizar Compra
        </button>
      </div>
    </aside>

  </Teleport>
</template>
