<script setup lang="ts">
import image1 from '../../assets/images/collection-1.png'
import image2 from '../../assets/images/collection-2.png'
import image3 from '../../assets/images/collection-3.png'

const collections = [
  {
    title: 'Oversized',
    image: image1,
  },
  {
    title: 'Casual',
    image: image2,
  },
  {
    title: 'Premium',
    image: image3,
  },
]
</script>

<template>
  <section class="py-24">
    <div class="mx-auto max-w-7xl px-6">
      <h2 class="mb-12 text-4xl font-bold">
        Coleções
      </h2>

      <div class="grid gap-6 md:grid-cols-3">
        <article
          v-for="collection in collections"
          :key="collection.title"
          class="group relative h-125 overflow-hidden rounded-2xl"
        >
          <img
            :src="collection.image"
            :alt="collection.title"
            class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
          />

          <div
            class="absolute inset-0 bg-linear-to-t from-black/70 via-black/20 to-transparent"
          />

          <div
            class="absolute bottom-8 left-8 text-white"
          >
            <h3 class="text-3xl font-bold">
              {{ collection.title }}
            </h3>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
