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
      path: '/product/:id',
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
    }
  ],

  scrollBehavior() {
    return {
      top: 0,
      behavior: 'smooth',
    }
  },
})

export default router
