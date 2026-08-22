<script setup lang="ts">
defineProps<{
  frontImage: string
  backImage: string
  name: string
  price: string
}>()

defineEmits<{
  quickView: []
}>()
</script>

<template>
  <article class="group cursor-pointer">
    <div
      class="relative overflow-hidden rounded-3xl bg-zinc-100"
    >
      <!-- Frente -->
      <img
        :src="frontImage"
        :alt="name"
        class="aspect-square w-full object-cover transition-all duration-500 group-hover:opacity-0"
      />

      <!-- Costas -->
      <img
        :src="backImage"
        :alt="`${name} costas`"
        class="absolute inset-0 aspect-square w-full object-cover opacity-0 transition-all duration-500 group-hover:opacity-100"
      />
    </div>

    <div class="mt-4">
      <h3 class="font-medium text-zinc-900">
        {{ name }}
      </h3>

      <p class="mt-1 text-zinc-500">
        {{ price }}
      </p>

      <button
        @click.stop="$emit('quickView')"
        class="cursor-pointer mt-4 w-full rounded-xl bg-black py-3 text-sm font-medium text-white transition hover:bg-zinc-800"
      >
          Comprar agora
      </button>
    </div>
  </article>
</template>
