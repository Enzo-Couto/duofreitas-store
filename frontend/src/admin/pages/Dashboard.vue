<script setup>
import { ref, computed, onMounted } from 'vue'

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Tooltip,
  ArcElement,
  Legend
} from 'chart.js'

import {
  Line,
  Doughnut,
  Bar
} from 'vue-chartjs'

import dashboardService from '../services/dashboardService'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Tooltip,
  ArcElement,
  Legend
)

const orderStatusData = computed(() => ({
  labels: [
    'Pendente',
    'Processando',
    'Enviado',
    'Entregue',
    'Cancelado'
  ],

  datasets: [
    {
      data: [
        stats.value.pendingOrders,
        stats.value.processingOrders,
        stats.value.shippedOrders,
        stats.value.deliveredOrders,
        stats.value.cancelledOrders
      ],

      backgroundColor: [
        '#ffc107',
        '#0dcaf0',
        '#0d6efd',
        '#198754',
        '#dc3545'
      ],

      borderWidth: 0
    }
  ]
}))

const loading = ref(true)

const stats = ref({
  totalOrders: 0,

  pendingOrders: 0,
  processingOrders: 0,
  shippedOrders: 0,
  deliveredOrders: 0,
  cancelledOrders: 0,

  pendingPayments: 0,
  approvedPayments: 0,
  refundedPayments: 0,
  cancelledPayments: 0,

  revenue: 0
})
const latestOrders = ref([])

const ordersByDay = ref([])

const revenueFormatted = computed(() =>
  Number(stats.value.revenue).toLocaleString(
    'pt-BR',
    {
      style: 'currency',
      currency: 'BRL'
    }
  )
)

const ordersByDayData = computed(() => ({
  labels: ordersByDay.value.map(
    item =>
      new Date(item.date)
        .toLocaleDateString('pt-BR')
  ),

  datasets: [
    {
      label: 'Pedidos',
      data: ordersByDay.value.map(
        item => item.count
      ),
      borderColor: '#0d6efd',
      backgroundColor: 'rgba(13,110,253,0.15)',
      fill: true,
      borderWidth: 3,
      tension: 0.4,
      pointRadius: 5,
      pointHoverRadius: 8
    }
  ]
}))

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: false
    }
  },

  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0
      }
    }
  }
}

const revenueByDayData = computed(() => ({
  labels: ordersByDay.value.map(
    item =>
      new Date(item.date)
        .toLocaleDateString('pt-BR')
  ),

  datasets: [
    {
      label: 'Faturamento',
      data: ordersByDay.value.map(
        item => item.revenue || 0
      ),
      borderWidth: 1
    }
  ]
}))

onMounted(async () => {
  try {

    const data =
      await dashboardService.getStats()

    stats.value = {
      totalOrders:
        data.total_orders,

      pendingOrders:
        data.pending_orders,

      processingOrders:
        data.processing_orders,

      shippedOrders:
        data.shipped_orders,

      deliveredOrders:
        data.delivered_orders,

      cancelledOrders:
        data.cancelled_orders,

      pendingPayments:
        data.pending_payments,

      approvedPayments:
        data.approved_payments,

      refundedPayments:
        data.refunded_payments,

      cancelledPayments:
        data.cancelled_payments,

      revenue:
        data.revenue
    }

    ordersByDay.value =
      data.orders_by_day || []

    latestOrders.value =
      data.latest_orders || []

  } catch (error) {

    console.error(
      'Erro ao carregar dashboard:',
      error
    )

  } finally {

    loading.value = false

  }
})

function formatMoney(value) {
  return Number(value).toLocaleString(
    'pt-BR',
    {
      style: 'currency',
      currency: 'BRL'
    }
  )
}

function getStatusClass(status) {

  switch (status) {

    case 'pending':
      return 'bg-warning text-dark'

    case 'processing':
      return 'bg-info'

    case 'paid':
      return 'bg-success'

    case 'shipped':
      return 'bg-primary'

    case 'delivered':
      return 'bg-success'

    case 'cancelled':
      return 'bg-danger'

    default:
      return 'bg-secondary'
  }
}

function getStatusLabel(status) {

  switch (status) {

    case 'pending':
      return 'Pendente'

    case 'processing':
      return 'Processando'

    case 'paid':
      return 'Pago'

    case 'shipped':
      return 'Enviado'

    case 'delivered':
      return 'Entregue'

    case 'cancelled':
      return 'Cancelado'

    default:
      return status
  }
}
</script>

<template>
  <div class="container-fluid py-4">

    <div class="mb-4">
      <h2 class="fw-bold mb-1">
        Dashboard
      </h2>

      <p class="text-muted mb-0">
        Visão geral da loja
      </p>
    </div>

    <div
      v-if="loading"
      class="card border-0 shadow-sm"
    >
      <div class="card-body">
        Carregando...
      </div>
    </div>

    <template v-else>

      <!-- Cards -->

      <div class="row g-3 mb-4">

        <div class="col-xl-2 col-md-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <small class="text-muted">
                Total Pedidos
              </small>

              <h3 class="fw-bold mb-0">
                {{ stats.totalOrders }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-2 col-md-4">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-warning">
            <div class="card-body">
              <small class="text-muted">
                Pendentes
              </small>

              <h3 class="fw-bold text-warning mb-0">
                {{ stats.pendingOrders }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-2 col-md-4">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-info">
            <div class="card-body">
              <small class="text-muted">
                Processando
              </small>

              <h3 class="fw-bold text-info mb-0">
                {{ stats.processingOrders }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-2 col-md-4">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-primary">
            <div class="card-body">
              <small class="text-muted">
                Enviados
              </small>

              <h3 class="fw-bold text-primary mb-0">
                {{ stats.shippedOrders }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-2 col-md-4">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-success">
            <div class="card-body">
              <small class="text-muted">
                Entregues
              </small>

              <h3 class="fw-bold text-success mb-0">
                {{ stats.deliveredOrders }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-2 col-md-4">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-danger">
            <div class="card-body">
              <small class="text-muted">
                Cancelados
              </small>

              <h3 class="fw-bold text-danger mb-0">
                {{ stats.cancelledOrders }}
              </h3>
            </div>
          </div>
        </div>

      </div>

      <div class="row g-3 mb-4">

        <div class="col-xl-3 col-md-6">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-warning">
            <div class="card-body">
              <small class="text-muted">
                Pag. Pendente
              </small>

              <h3 class="fw-bold text-warning mb-0">
                {{ stats.pendingPayments }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-success">
            <div class="card-body">
              <small class="text-muted">
                Pag. Aprovado
              </small>

              <h3 class="fw-bold text-success mb-0">
                {{ stats.approvedPayments }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-secondary">
            <div class="card-body">
              <small class="text-muted">
                Reembolsados
              </small>

              <h3 class="fw-bold text-secondary mb-0">
                {{ stats.refundedPayments }}
              </h3>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="card border-0 shadow-sm h-100 border-start border-4 border-danger">
            <div class="card-body">
              <small class="text-muted">
                Pag. Cancelado
              </small>

              <h3 class="fw-bold text-danger mb-0">
                {{ stats.cancelledPayments }}
              </h3>
            </div>
          </div>
        </div>

      </div>

      <!-- Gráficos -->

      <div class="row mb-4">

        <div class="col-lg-8">

          <div class="card border-0 shadow-sm">

            <div class="card-body">

              <h5 class="mb-4">
                Pedidos por Data
              </h5>

              <Line
                :data="ordersByDayData"
              />

            </div>

          </div>

        </div>

        <div class="col-lg-4">

          <div class="card border-0 shadow-sm">

            <div class="card-body">

                <h5 class="mb-4">
                  Distribuição dos Pedidos
                </h5>

                <Doughnut
                  :data="orderStatusData"
                />

            </div>

          </div>

        </div>

      </div>

      <!-- Últimos pedidos -->

      <div class="card border-0 shadow-sm">

        <div class="card-body">

          <h5 class="mb-4">
            Últimos Pedidos
          </h5>

          <div class="table-responsive">

            <table class="table table-hover align-middle">

              <thead>
                <tr>
                  <th>#</th>
                  <th>Cliente</th>
                  <th>Data</th>
                  <th>Status Pedido</th>
                  <th>Status Pagamento</th>
                  <th>Total</th>
                </tr>
              </thead>

              <tbody>

                <tr
                  v-for="order in latestOrders"
                  :key="order.id"
                >
                  <td>
                    #{{ order.id }}
                  </td>

                  <td>
                    {{ order.customer_name }}
                  </td>

                  <td>
                      {{
                        new Date(order.created_at)
                          .toLocaleDateString('pt-BR')
                      }}
                  </td>

                  <td>

                    <span
                      class="badge"
                      :class="getStatusClass(order.status)"
                    >
                      {{ getStatusLabel(order.status) }}
                    </span>

                  </td>

                  <td>

                    <span
                      v-if="order.payment_status === 'approved'"
                      class="badge bg-success"
                    >
                      Aprovado
                    </span>

                    <span
                      v-else-if="order.payment_status === 'pending'"
                      class="badge bg-warning text-dark"
                    >
                      Pendente
                    </span>

                    <span
                      v-else-if="order.payment_status === 'refunded'"
                      class="badge bg-secondary"
                    >
                      Reembolsado
                    </span>

                    <span
                      v-else-if="order.payment_status === 'cancelled'"
                      class="badge bg-danger"
                    >
                      Cancelado
                    </span>

                    <span
                      v-else
                      class="badge bg-secondary"
                    >
                      {{ order.payment_status }}
                    </span>

                  </td>

                  <td>
                    {{ formatMoney(order.total) }}
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </div>

      </div>

    </template>

  </div>
</template>
