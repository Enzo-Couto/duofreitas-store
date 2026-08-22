<script setup lang="ts">
import heroImage from '@/assets/images/hero.jpg'
</script>

<template>
  <section
    class="relative flex min-h-screen items-center justify-center overflow-hidden"
  >
    <img
      :src="heroImage"
      alt="Duo Freitas"
      class="absolute inset-0 h-full w-full object-cover"
    />

    <div class="absolute inset-0 bg-black/40" />

    <div
      class="relative z-10 mx-auto max-w-4xl px-6 text-center text-white"
    >
      <span
        class="mb-4 block text-sm uppercase tracking-[0.5em]"
      >
        Nova Coleção
      </span>

      <h1
        class="mb-6 text-6xl font-extrabold uppercase md:text-8xl"
      >
        Duo Freitas
      </h1>

      <p
        class="mx-auto mb-8 max-w-xl text-lg text-zinc-200"
      >
        Moda feminina para quem busca estilo e identidade.
      </p>

      <button
        class="cursor-pointer rounded-none bg-white px-8 py-4 font-semibold text-black transition hover:scale-105"
      >
        Comprar Agora
      </button>
    </div>
  </section>
</template>
