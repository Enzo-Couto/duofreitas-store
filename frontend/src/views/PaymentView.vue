<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { createOrder } from '@/services/orders'

import AppNavbar from '@/components/layout/AppNavbar.vue'

import { useCartStore } from '@/stores/cart'
import { useCheckoutStore } from '@/stores/checkout'

const router = useRouter()

const cartStore = useCartStore()
const checkoutStore = useCheckoutStore()

const subtotal = computed(() =>
  cartStore.totalPrice
)

const shipping = computed(() => 0)

const total = computed(() =>
  subtotal.value + shipping.value
)

function formatPrice(value: number) {
  return value.toFixed(2).replace('.', ',')
}

async function proceedPayment() {

  const payload = {
    customer_name:
      checkoutStore.customer.name,

    customer_email:
      checkoutStore.customer.email,

    customer_phone:
      checkoutStore.customer.phone,

    customer_cpf:
      checkoutStore.customer.cpf,

    cep:
      checkoutStore.address.cep,

    street:
      checkoutStore.address.street,

    number:
      checkoutStore.address.number,

    complement:
      checkoutStore.address.complement,

    neighborhood:
      checkoutStore.address.neighborhood,

    city:
      checkoutStore.address.city,

    state:
      checkoutStore.address.state,

    items: cartStore.items.map(
      item => ({
        product_id: item.id,
        quantity: item.quantity
      })
    )
  }

  try {

    const order =
      await createOrder(payload)

    checkoutStore.orderId =
      order.id

    cartStore.clearCart()

    router.push('/order-success')

  } catch (error) {

    console.error(error)

    alert(
      'Erro ao criar pedido'
    )

  }
}

if (
  !checkoutStore.customer.name ||
  cartStore.items.length === 0
) {
  router.push('/checkout')
}
</script>

<template>
  <AppNavbar />

  <main
    class="mx-auto max-w-7xl px-6 py-32"
  >
    <h1
      class="mb-12 text-5xl font-bold"
    >
      Pagamento
    </h1>

    <div
      class="grid gap-12 lg:grid-cols-[1fr_420px]"
    >
      <!-- Dados -->

      <section class="space-y-8">

        <div
          class="rounded-3xl border border-zinc-200 p-8"
        >
          <h2
            class="mb-6 text-2xl font-semibold"
          >
            Dados do Cliente
          </h2>

          <div class="space-y-3">

            <p>
              <strong>Nome:</strong>
              {{ checkoutStore.customer.name }}
            </p>

            <p>
              <strong>CPF:</strong>
              {{ checkoutStore.customer.cpf }}
            </p>

            <p>
              <strong>E-mail:</strong>
              {{ checkoutStore.customer.email }}
            </p>

            <p>
              <strong>Telefone:</strong>
              {{ checkoutStore.customer.phone }}
            </p>

          </div>
        </div>

        <div
          class="rounded-3xl border border-zinc-200 p-8"
        >
          <h2
            class="mb-6 text-2xl font-semibold"
          >
            Endereço de Entrega
          </h2>

          <div class="space-y-3">

            <p>
              <strong>CEP:</strong>
              {{ checkoutStore.address.cep }}
            </p>

            <p>
              <strong>Rua:</strong>
              {{ checkoutStore.address.street }}
            </p>

            <p>
              <strong>Número:</strong>
              {{ checkoutStore.address.number }}
            </p>

            <p
              v-if="
                checkoutStore.address.complement
              "
            >
              <strong>Complemento:</strong>
              {{ checkoutStore.address.complement }}
            </p>

            <p>
              <strong>Bairro:</strong>
              {{ checkoutStore.address.neighborhood }}
            </p>

            <p>
              <strong>Cidade:</strong>
              {{ checkoutStore.address.city }}
            </p>

            <p>
              <strong>Estado:</strong>
              {{ checkoutStore.address.state }}
            </p>

          </div>
        </div>

        <div
          class="rounded-3xl border border-zinc-200 p-8"
        >
          <h2
            class="mb-6 text-2xl font-semibold"
          >
            Método de Pagamento
          </h2>

          <div class="grid gap-4">

            <button
              class="rounded-xl border border-zinc-300 p-4 text-left transition hover:border-black"
            >
              PIX
            </button>

            <button
              class="rounded-xl border border-zinc-300 p-4 text-left transition hover:border-black"
            >
              Cartão de Crédito
            </button>

            <button
              class="rounded-xl border border-zinc-300 p-4 text-left transition hover:border-black"
            >
              Boleto
            </button>

          </div>
        </div>

      </section>

      <!-- Resumo -->

      <aside>
        <div
          class="sticky top-32 rounded-3xl border border-zinc-200 p-8"
        >
          <h2
            class="mb-8 text-2xl font-semibold"
          >
            Resumo do Pedido
          </h2>

          <div class="space-y-5">

            <div
              v-for="item in cartStore.items"
              :key="`${item.id}-${item.size}`"
              class="flex gap-4"
            >
              <img
                :src="item.image"
                :alt="item.name"
                class="h-20 w-20 rounded-xl object-cover"
              />

              <div class="flex-1">
                <h3 class="font-medium">
                  {{ item.name }}
                </h3>

                <p
                  class="text-sm text-zinc-500"
                >
                  Tamanho {{ item.size }}
                </p>

                <p
                  class="text-sm text-zinc-500"
                >
                  Quantidade {{ item.quantity }}
                </p>
              </div>

              <div class="font-semibold">
                R$
                {{
                  formatPrice(
                    item.price *
                    item.quantity
                  )
                }}
              </div>

            </div>

          </div>

          <div
            class="my-8 border-t"
          />

          <div class="space-y-4">

            <div
              class="flex justify-between"
            >
              <span>Subtotal</span>

              <span>
                R$
                {{ formatPrice(subtotal) }}
              </span>
            </div>

            <div
              class="flex justify-between"
            >
              <span>Frete</span>

              <span>
                R$
                {{ formatPrice(shipping) }}
              </span>
            </div>

            <div
              class="flex justify-between text-xl font-bold"
            >
              <span>Total</span>

              <span>
                R$
                {{ formatPrice(total) }}
              </span>
            </div>

          </div>

          <button
            @click="proceedPayment"
            class="cursor-pointer mt-8 w-full rounded-xl bg-black py-4 text-white transition hover:bg-zinc-800"
          >
            Finalizar Pedido
          </button>

        </div>
      </aside>

    </div>
  </main>
</template>
