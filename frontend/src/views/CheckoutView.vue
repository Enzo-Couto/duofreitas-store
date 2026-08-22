<script setup lang="ts">
import { reactive, computed, ref, watch } from 'vue'

import AppNavbar from '@/components/layout/AppNavbar.vue'
import { useCartStore } from '@/stores/cart'
import { getAddressByCep } from '@/services/viacep'

import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

const loadingCep = ref(false)

const cartError = ref('')

const form = reactive({
  name: '',
  cpf: '',
  email: '',
  phone: '',

  cep: '',
  street: '',
  number: '',
  complement: '',
  neighborhood: '',
  city: '',
  state: '',
})

const brazilianStates = [
  { sigla: 'AC', nome: 'Acre' },
  { sigla: 'AL', nome: 'Alagoas' },
  { sigla: 'AP', nome: 'Amapá' },
  { sigla: 'AM', nome: 'Amazonas' },
  { sigla: 'BA', nome: 'Bahia' },
  { sigla: 'CE', nome: 'Ceará' },
  { sigla: 'DF', nome: 'Distrito Federal' },
  { sigla: 'ES', nome: 'Espírito Santo' },
  { sigla: 'GO', nome: 'Goiás' },
  { sigla: 'MA', nome: 'Maranhão' },
  { sigla: 'MT', nome: 'Mato Grosso' },
  { sigla: 'MS', nome: 'Mato Grosso do Sul' },
  { sigla: 'MG', nome: 'Minas Gerais' },
  { sigla: 'PA', nome: 'Pará' },
  { sigla: 'PB', nome: 'Paraíba' },
  { sigla: 'PR', nome: 'Paraná' },
  { sigla: 'PE', nome: 'Pernambuco' },
  { sigla: 'PI', nome: 'Piauí' },
  { sigla: 'RJ', nome: 'Rio de Janeiro' },
  { sigla: 'RN', nome: 'Rio Grande do Norte' },
  { sigla: 'RS', nome: 'Rio Grande do Sul' },
  { sigla: 'RO', nome: 'Rondônia' },
  { sigla: 'RR', nome: 'Roraima' },
  { sigla: 'SC', nome: 'Santa Catarina' },
  { sigla: 'SP', nome: 'São Paulo' },
  { sigla: 'SE', nome: 'Sergipe' },
  { sigla: 'TO', nome: 'Tocantins' },
]

const isSubmitting = ref(false)

const errors = reactive({
  name: '',
  email: '',
  phone: '',
  cpf: '',
  cep: '',
  number: '',
  street: '',
  neighborhood: '',
  city: '',
  state: '',
})

function clearErrors() {
  cartError.value = ''

  errors.name = ''
  errors.email = ''
  errors.phone = ''
  errors.cpf = ''
  errors.cep = ''
  errors.number = ''
  errors.street = ''
  errors.neighborhood = ''
  errors.city = ''
  errors.state = ''
}

const errorMessages = computed(() =>
  Object.values(errors).filter(Boolean)
)

function validateForm() {
  clearErrors()

  if (cartStore.items.length === 0) {
    cartError.value = 'Seu carrinho está vazio'
    return false
  }

  if (!form.name.trim()) {
    errors.name = 'Informe seu nome'
  }

  if (!form.cpf.trim()) {
    errors.cpf = 'Informe seu CPF'
  } else if (!validateCPF(form.cpf)) {
    errors.cpf = 'CPF inválido'
  }

  const emailRegex =
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!form.email.trim()) {
    errors.email = 'Informe seu e-mail'
  } else if (!emailRegex.test(form.email)) {
    errors.email = 'E-mail inválido'
  }

  if (
    form.phone.replace(/\D/g, '').length !== 11
  ) {
    errors.phone = 'Telefone inválido'
  }

  if (
    form.cep.replace(/\D/g, '').length !== 8
  ) {
    errors.cep = 'CEP inválido'
  }

  if (
    !form.number.trim() ||
    Number(form.number) <= 0
  ) {
    errors.number = 'Número inválido'
  }

  if (!form.street.trim()) {
    errors.street = 'Informe a rua'
  }

  if (!form.neighborhood.trim()) {
    errors.neighborhood = 'Informe o bairro'
  }

  if (!form.city.trim()) {
    errors.city = 'Informe a cidade'
  }

  if (!form.state.trim()) {
    errors.state = 'Selecione um estado'
  }

  return (
    Object.values(errors).filter(Boolean)
      .length === 0
  )
}

watch(
  () => form.cep,
  async (value) => {
    const cep = value.replace(/\D/g, '')

    if (cep.length !== 8) {
      form.street = ''
      form.neighborhood = ''
      form.city = ''
      form.state = ''

      return
    }

    loadingCep.value = true

    const address = await getAddressByCep(cep)

    loadingCep.value = false

    if (!address) {
      errors.cep = 'CEP não encontrado'

      form.street = ''
      form.neighborhood = ''
      form.city = ''
      form.state = ''

      return
    }

    form.street = address.logradouro
    form.neighborhood = address.bairro
    form.city = address.localidade
    form.state = address.uf
    errors.cep = ''
  }
)

watch(
  () => form.number,
  value => {
    form.number = value.replace(/\D/g, '')
  }
)

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

function validateCPF(cpf: string): boolean {
  cpf = cpf.replace(/\D/g, '')

  if (cpf.length !== 11) {
    return false
  }

  if (/^(\d)\1+$/.test(cpf)) {
    return false
  }

  let sum = 0

  for (let i = 0; i < 9; i++) {
    sum += Number(cpf.charAt(i)) * (10 - i)
  }

  let remainder = (sum * 10) % 11

  if (remainder === 10) {
    remainder = 0
  }

  if (remainder !== Number(cpf.charAt(9))) {
    return false
  }

  sum = 0

  for (let i = 0; i < 10; i++) {
    sum += Number(cpf.charAt(i)) * (11 - i)
  }

  remainder = (sum * 10) % 11

  if (remainder === 10) {
    remainder = 0
  }

  return remainder === Number(cpf.charAt(10))
}

import { useCheckoutStore } from '@/stores/checkout'

const checkoutStore = useCheckoutStore()

function finishOrder() {
  if (!validateForm()) return

  checkoutStore.customer = {
    name: form.name,
    cpf: form.cpf,
    email: form.email,
    phone: form.phone,
  }

  checkoutStore.address = {
    cep: form.cep,
    street: form.street,
    number: form.number,
    complement: form.complement,
    neighborhood: form.neighborhood,
    city: form.city,
    state: form.state,
  }

  router.push('/payment')
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
      Checkout
    </h1>

    <div
      class="grid gap-12 lg:grid-cols-[1fr_420px]"
    >
      <!-- Formulário -->

      <section>
        <div
          class="rounded-3xl border border-zinc-200 p-8"
        >
          <h2
            class="mb-8 text-2xl font-semibold"
          >
            Informações de Entrega
          </h2>

          <div
            v-if="errorMessages.length"
            class="mb-6 rounded-2xl border border-red-200 bg-red-50 p-4"
          >
            <p class="font-medium text-red-700">
              Corrija os campos abaixo:
            </p>

            <ul class="mt-2 list-disc pl-5 text-sm text-red-600">
              <li
                v-for="error in errorMessages"
                :key="error"
              >
                {{ error }}
              </li>
            </ul>
          </div>

          <div class="grid gap-5">
            <input
              v-model="form.name"
              type="text"
              placeholder="Nome completo"
              :class="[
                'rounded-xl border p-4 outline-none',
                errors.name
                  ? 'border-red-500'
                  : 'border-zinc-300 focus:border-black'
              ]"
            />

            <input
              v-model="form.cpf"
              v-maska="'###.###.###-##'"
              maxlength="14"
              type="text"
              placeholder="CPF"
              inputmode="numeric"
              :class="[
                'rounded-xl border p-4 outline-none',
                errors.cpf
                  ? 'border-red-500'
                  : 'border-zinc-300 focus:border-black'
              ]"
            />

            <input
              v-model="form.email"
              type="email"
              placeholder="E-mail"
              :class="[
                'rounded-xl border p-4 outline-none',
                errors.email
                  ? 'border-red-500'
                  : 'border-zinc-300 focus:border-black'
              ]"
            />

            <input
              v-model="form.phone"
              v-maska="'(##) #####-####'"
              maxlength="15"
              type="text"
              placeholder="Telefone"
              inputmode="numeric"
              :class="[
                'rounded-xl border p-4 outline-none',
                errors.phone
                  ? 'border-red-500'
                  : 'border-zinc-300 focus:border-black'
              ]"
            />

            <div
              class="grid gap-4 md:grid-cols-2"
            >
              <div class="relative">
                  <input
                    v-model="form.cep"
                    v-maska="'#####-###'"
                    maxlength="9"
                    type="text"
                    placeholder="CEP"
                    inputmode="numeric"
                    :class="[
                      'rounded-xl border p-4 outline-none',
                      errors.cep
                        ? 'border-red-500'
                        : 'border-zinc-300 focus:border-black'
                    ]"
                  />

                <span
                  v-if="loadingCep"
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-zinc-500"
                >
                  Buscando...
                </span>
              </div>

              <input
                v-model="form.number"
                maxlength="10"
                type="text"
                placeholder="Número"
                inputmode="numeric"
                :class="[
                  'rounded-xl border p-4 outline-none',
                  errors.number
                    ? 'border-red-500'
                    : 'border-zinc-300 focus:border-black'
                ]"
              />
            </div>

            <input
              v-model="form.street"
              type="text"
              placeholder="Rua"
              inputmode="text"
              :class="[
                'rounded-xl border p-4 outline-none',
                errors.street
                  ? 'border-red-500'
                  : 'border-zinc-300 focus:border-black'
              ]"
            />

            <input
              v-model="form.complement"
              type="text"
              placeholder="Complemento"
              inputmode="text"
              class="rounded-xl border border-zinc-300 p-4 outline-none focus:border-black"
            />

            <input
              v-model="form.neighborhood"
              type="text"
              placeholder="Bairro"
              inputmode="text"
              :class="[
                'rounded-xl border p-4 outline-none',
                errors.neighborhood
                  ? 'border-red-500'
                  : 'border-zinc-300 focus:border-black'
              ]"
            />

            <div
              class="grid gap-4 md:grid-cols-2"
            >
              <input
                v-model="form.city"
                type="text"
                placeholder="Cidade"
                inputmode="text"
                :class="[
                  'rounded-xl border p-4 outline-none',
                  errors.city
                    ? 'border-red-500'
                    : 'border-zinc-300 focus:border-black'
                ]"
              />

              <select
                v-model="form.state"
                :class="[
                  'rounded-xl border p-4 outline-none',
                  errors.state
                    ? 'border-red-500'
                    : 'border-zinc-300 focus:border-black'
                ]"
              >
                <option value="">
                  Selecione um estado
                </option>

                <option
                  v-for="state in brazilianStates"
                  :key="state.sigla"
                  :value="state.sigla"
                >
                  {{ state.nome }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </section>

      <!-- Resumo -->

      <aside>
        <div
          class="sticky top-32 rounded-3xl border border-zinc-200 p-8"
        >

          <div
            v-if="cartError"
            class="mb-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
            >
              {{ cartError }}
          </div>

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
                R$ {{ formatPrice(subtotal) }}
              </span>
            </div>

            <div
              class="flex justify-between"
            >
              <span>Frete</span>

              <span>
                R$ {{ formatPrice(shipping) }}
              </span>
            </div>

            <div
              class="flex justify-between text-xl font-bold"
            >
              <span>Total</span>

              <span>
                R$ {{ formatPrice(total) }}
              </span>
            </div>
          </div>

          <button
            :disabled="isSubmitting"
            @click="finishOrder"
            :class="[
              'mt-8 w-full rounded-xl py-4 text-white transition',
              isSubmitting
                ? 'cursor-not-allowed bg-zinc-400'
                : 'cursor-pointer bg-black hover:bg-zinc-800'
            ]"
          >
            Continuar para Pagamento
          </button>
        </div>
      </aside>
    </div>
  </main>
</template>
