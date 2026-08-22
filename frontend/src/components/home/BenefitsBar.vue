<script setup lang="ts">
import {
  Truck,
  CreditCard,
  ShieldCheck,
  RefreshCw,
} from 'lucide-vue-next'

const benefits = [
  {
    icon: Truck,
    title: 'Frete Grátis',
    subtitle: 'Acima de R$299',
  },
  {
    icon: CreditCard,
    title: 'Até 6x sem juros',
    subtitle: 'No cartão',
  },
  {
    icon: ShieldCheck,
    title: 'Compra Segura',
    subtitle: 'Dados protegidos',
  },
  {
    icon: RefreshCw,
    title: 'Troca Fácil',
    subtitle: 'Até 7 dias',
  },
]
</script>

<template>
  <section class="border-y border-zinc-200 bg-white">
    <div
      class="mx-auto grid max-w-7xl gap-8 px-6 py-6 md:grid-cols-4"
    >
      <div
        v-for="benefit in benefits"
        :key="benefit.title"
        class="flex items-center gap-4"
      >
        <component
          :is="benefit.icon"
          :size="24"
        />

        <div>
          <p class="font-medium">
            {{ benefit.title }}
          </p>

          <p class="text-sm text-zinc-500">
            {{ benefit.subtitle }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
