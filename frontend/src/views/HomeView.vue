<script setup lang="ts">
import AppNavbar from '../components/layout/AppNavbar.vue'
import AppFooter from '../components/layout/AppFooter.vue'

import HeroSection from '../components/home/HeroSection.vue'
import BenefitsBar from '../components/home/BenefitsBar.vue'
import CollectionsSection from '../components/home/CollectionsSection.vue'
import FeaturedProducts from '../components/home/FeaturedProducts.vue'
</script>

<template>
  <AppNavbar />

  <HeroSection />

  <BenefitsBar />

  <CollectionsSection />

  <FeaturedProducts />

  <AppFooter />
</template>
