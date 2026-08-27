<template>
  <div class="admin-layout">
    <AdminSidebar />

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import AdminSidebar from "../components/AdminSidebar.vue"
</script>

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
