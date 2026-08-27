<template>
  <aside class="sidebar">

    <div class="brand">
      <h2>Duo Freitas</h2>
      <p>Painel Administrativo</p>
    </div>

    <nav class="nav-menu">

      <RouterLink
        to="/admin"
        class="menu-item"
        exact-active-class="menu-item-active"
      >
        Dashboard
      </RouterLink>

      <RouterLink
        to="/admin/products"
        class="menu-item"
        active-class="menu-item-active"
      >
        Produtos
      </RouterLink>

      <RouterLink
        to="/admin/categories"
        class="menu-item"
        active-class="menu-item-active"
      >
        Categorias
      </RouterLink>

      <RouterLink
        to="/admin/orders"
        class="menu-item"
        active-class="menu-item-active"
      >
        Pedidos
      </RouterLink>

    </nav>

  </aside>
</template>

<style scoped>

.sidebar {
  width: 280px;
  min-height: 100vh;

  padding: 2rem;

  background: #ffffff;
  border-right: 1px solid #e5e7eb;
}

.brand {
  margin-bottom: 3rem;
}

.brand h2 {
  margin: 0;

  font-size: 2rem;
  font-weight: 700;

  color: #111827;
}

.brand p {
  margin-top: .5rem;

  color: #6b7280;
}

.nav-menu {
  display: flex;
  flex-direction: column;

  gap: .75rem;
}

.menu-item {
  display: block;

  padding: 1rem 1.25rem;

  border-radius: 1rem;

  text-decoration: none;

  color: #111827;
  font-weight: 500;

  transition: all .2s ease;
}

.menu-item:not(.menu-item-active):hover {
  background: #f3f4f6;
  color: #111827;
}

/* Item selecionado */
.menu-item-active {
  background: #111827;
  color: #ffffff;
}

/* Hover do item selecionado */
.menu-item-active:hover {
  background: #111827;
  color: #ffffff;
}

</style>
