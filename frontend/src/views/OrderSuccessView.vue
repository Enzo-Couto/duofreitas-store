<script setup lang="ts">
import { useRouter } from 'vue-router'

import AppNavbar from '@/components/layout/AppNavbar.vue'

import { useCheckoutStore } from '@/stores/checkout'

const router = useRouter()

const checkoutStore = useCheckoutStore()

function continueShopping() {
  router.push('/')
}
</script>

<template>
  <AppNavbar />

  <main
    class="mx-auto flex min-h-screen max-w-3xl items-center justify-center px-6 py-32"
  >
    <div
      class="w-full rounded-3xl border border-zinc-200 p-12 text-center"
    >
      <div
        class="mx-auto mb-8 flex h-24 w-24 items-center justify-center rounded-full bg-green-100"
      >
        <svg
          class="h-12 w-12 text-green-600"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M5 13l4 4L19 7"
          />
        </svg>
      </div>

      <h1
        class="mb-4 text-4xl font-bold"
      >
        Pedido Confirmado
      </h1>

      <p
        class="mx-auto mb-8 max-w-xl text-zinc-600"
      >
        Recebemos seu pedido com sucesso.
        Em breve você receberá atualizações
        sobre o pagamento e o envio através
        do seu e-mail.
      </p>

      <div
        class="mb-10 rounded-2xl bg-zinc-50 p-6"
      >
        <p
          class="text-sm uppercase tracking-wider text-zinc-500"
        >
          Número do Pedido
        </p>

        <p
          class="mt-2 text-2xl font-bold"
        >
          #{{ checkoutStore.orderId }}
        </p>
      </div>

      <button
        @click="continueShopping"
        class="rounded-xl bg-black px-8 py-4 text-white transition hover:bg-zinc-800"
      >
        Continuar Comprando
      </button>
    </div>
  </main>
</template>
