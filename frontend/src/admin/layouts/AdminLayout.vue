<script setup>
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import AdminSidebar from '../components/AdminSidebar.vue'
</script>

<template>
  <div class="admin-layout">
    <AdminSidebar />

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.content {
  flex: 1;
  padding: 24px;
}
</style>
