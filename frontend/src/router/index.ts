import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import CatalogView from '@/views/CatalogView.vue'
import ProductView from '@/views/ProductView.vue'
import CheckoutView from '@/views/CheckoutView.vue'
import PaymentView from '@/views/PaymentView.vue'
import OrderSuccessView from '@/views/OrderSuccessView.vue'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      component: HomeView,
    },
    {
      path: '/catalog',
      component: CatalogView,
    },
    {
      path: '/product/:slug',
      component: ProductView,
    },
    {
      path: '/checkout',
      component: CheckoutView,
    },
    {
      path: '/payment',
      component: PaymentView,
    },
    {
      path: '/order-success',
      name: 'order-success',
      component: OrderSuccessView,
    },
    {
      path: "/admin/login",
      component: () =>
        import("@/admin/pages/Login.vue")
    },
    {
      path: "/admin",
      component: () =>
        import("@/admin/layouts/AdminLayout.vue"),
      children: [
        {
          path: "",
          component: () =>
            import("@/admin/pages/Dashboard.vue")
        },
        {
          path: "products",
          component: () =>
            import("@/admin/pages/Products.vue")
        },
        {
          path: "categories",
          component: () =>
            import("@/admin/pages/Categories.vue")
        },
        {
          path: "orders",
          component: () =>
            import("@/admin/pages/Orders.vue")
        }
      ]
    }
  ],

  scrollBehavior() {
    return {
      top: 0,
      behavior: 'smooth',
    }
  },
})

router.beforeEach((to, from, next) => {

  const token =
    localStorage.getItem(
      'admin_token'
    )

  const isAdminRoute =
    to.path.startsWith('/admin')

  const isLoginRoute =
    to.path === '/admin/login'

  if (
    isAdminRoute &&
    !isLoginRoute &&
    !token
  ) {
    return next(
      '/admin/login'
    )
  }

  if (
    isLoginRoute &&
    token
  ) {
    return next('/admin')
  }

  next()
})

export default router
