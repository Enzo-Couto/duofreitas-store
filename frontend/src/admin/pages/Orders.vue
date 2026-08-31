<script setup>
import { ref, onMounted } from "vue"
import * as bootstrap from "bootstrap"
import { Modal } from 'bootstrap'

import { useToast } from 'vue-toastification'

const toast = useToast()

const API_BASE = import.meta.env.VITE_API_BASE

const orders = ref([])
const loading = ref(false)

const selectedOrder = ref(null)
const loadingDetails = ref(false)

const loadOrders = async () => {
  try {
    loading.value = true

    const token = localStorage.getItem("token")

    const response = await fetch(
      `${API_BASE}/orders`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    if (!response.ok) {
      throw new Error("Erro ao carregar pedidos")
    }

    orders.value = await response.json()
  }
  catch (error) {
    console.error(error)
    toast.error("Erro ao carregar pedidos")
  }
  finally {
    loading.value = false
  }
}

const openOrder = async (id) => {
  try {
    console.log("Abrindo pedido:", id)

    loadingDetails.value = true

    const token = localStorage.getItem("token")

    const response = await fetch(
      `${API_BASE}/orders/${id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    console.log("Status:", response.status)

    if (!response.ok) {
      throw new Error("Erro ao carregar pedido")
    }

    const data = await response.json()

    console.log("Pedido recebido:", data)

    selectedOrder.value = data

    console.log("Antes modal")

    const modalElement =
      document.getElementById("orderModal")

    console.log("Modal:", modalElement)

    const modal = new bootstrap.Modal(
      modalElement
    )

    modal.show()

    console.log("Modal aberto")
  }
  catch (error) {
    console.error("ERRO COMPLETO:", error)
    alert("Erro ao carregar pedido")
  }
  finally {
    loadingDetails.value = false
  }
}

const formatCurrency = (value) => {
  return Number(value).toLocaleString(
    "pt-BR",
    {
      style: "currency",
      currency: "BRL"
    }
  )
}

const formatDate = (date) => {
  return new Date(date).toLocaleString(
    "pt-BR"
  )
}

const getStatusBadge = (status) => {
  switch (status) {
    case "pending":
      return "bg-warning"

    case "processing":
      return "bg-primary"

    case "shipped":
      return "bg-info"

    case "delivered":
      return "bg-success"

    case "cancelled":
      return "bg-danger"

    default:
      return "bg-secondary"
  }
}

const translateStatus = (status) => {
  const map = {
    pending: "Pendente",
    processing: "Processando",
    shipped: "Enviado",
    delivered: "Entregue",
    cancelled: "Cancelado"
  }

  return map[status] || status
}

const translatePaymentStatus = (status) => {
  const map = {
    pending: "Pendente",
    approved: "Aprovado",
    refunded: "Reembolsado",
    cancelled: "Cancelado"
  }

  return map[status] || status
}

const saveOrder = async () => {
  try {
    const token = localStorage.getItem("token")

    await fetch(
      `${API_BASE}/orders/${selectedOrder.value.id}/status`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          status: selectedOrder.value.status
        })
      }
    )

    await fetch(
      `${API_BASE}/orders/${selectedOrder.value.id}/payment-status`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          payment_status:
            selectedOrder.value.payment_status
        })
      }
    )

    await loadOrders()

    toast.success(
      "Pedido atualizado com sucesso"
    )

    const modalEl =
      document.getElementById("orderModal")

    if (modalEl) {
      const modal =
        Modal.getOrCreateInstance(modalEl)

      modal.hide()
    }

    selectedOrder.value = null

  }
  catch (error) {
    console.error(error)
    toast.error("Erro ao atualizar pedido")
  }
}

const getStatusLabel = (status) => {
  const labels = {
    pending: "Pendente",
    processing: "Processando",
    shipped: "Enviado",
    delivered: "Entregue",
    cancelled: "Cancelado"
  }

  return labels[status] || status
}

const getPaymentStatusLabel = (status) => {
  const labels = {
    pending: "Pendente",
    approved: "Aprovado",
    refunded: "Reembolsado",
    cancelled: "Cancelado"
  }

  return labels[status] || status
}

onMounted(() => {
  loadOrders()
})
</script>

<template>
  <div class="container-fluid py-4">

    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >
      <div>
        <h2 class="fw-bold mb-1">
          Pedidos
        </h2>

        <p class="text-muted mb-0">
          Gerencie os pedidos da loja
        </p>
      </div>
    </div>

    <!-- Cards -->

    <div class="row mb-4">

      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h6 class="text-muted">
              Total de Pedidos
            </h6>

            <h2 class="fw-bold">
              {{ orders.length }}
            </h2>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h6 class="text-muted">
              Pendentes
            </h6>

            <h2 class="fw-bold text-warning">
              {{
                orders.filter(
                  order => order.status === 'pending'
                ).length
              }}
            </h2>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h6 class="text-muted">
              Faturamento
            </h6>

            <h2 class="fw-bold text-success">
              {{
                formatCurrency(
                  orders
                    .filter(order => order.status === 'delivered')
                    .reduce(
                      (total, order) =>
                        total + Number(order.total_amount),
                      0
                    )
                )
              }}
            </h2>
          </div>
        </div>
      </div>

    </div>

    <!-- Tabela -->

    <div class="card border-0 shadow-sm">

      <div class="card-body">

        <div
          class="d-flex justify-content-between align-items-center mb-3"
        >
          <h5 class="mb-0">
            Pedidos cadastrados
          </h5>
        </div>

        <div class="table-responsive">

          <table
            class="table table-hover align-middle"
          >

            <thead>
              <tr>
                <th>#</th>
                <th>Cliente</th>
                <th>Telefone</th>
                <th>Itens</th>
                <th>Total</th>
                <th>Status</th>
                <th>Pagamento</th>
                <th>Data</th>
                <th width="120">
                  Ações
                </th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="order in orders"
                :key="order.id"
              >
                <td>
                  <strong>
                    #{{ order.id }}
                  </strong>
                </td>

                <td>
                  {{ order.customer_name }}
                </td>

                <td>
                  {{ order.customer_phone }}
                </td>

                <td>
                  {{ order.items_count }}
                </td>

                <td>
                  {{
                    formatCurrency(
                      order.total_amount
                    )
                  }}
                </td>

                <td>
                  <span
                    class="badge"
                    :class="
                      getStatusBadge(
                        order.status
                      )
                    "
                  >
                    {{
                      getStatusLabel(
                        order.status
                      )
                    }}
                  </span>
                </td>

                <td>
                  <span
                    class="badge bg-secondary"
                  >
                    {{
                      getPaymentStatusLabel(
                        order.payment_status
                      )
                    }}
                  </span>
                </td>

                <td>
                  {{
                    formatDate(
                      order.created_at
                    )
                  }}
                </td>

                <td>

                  <button
                    class="btn btn-sm btn-outline-primary"
                    :disabled="loadingDetails"
                    @click="
                      openOrder(order.id)
                    "
                  >
                    Ver
                  </button>

                </td>
              </tr>

              <tr
                v-if="orders.length === 0"
              >
                <td
                  colspan="9"
                  class="text-center py-4"
                >
                  Nenhum pedido encontrado
                </td>
              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

    <!-- Modal -->

    <div
      class="modal fade"
      id="orderModal"
      tabindex="-1"
      data-bs-backdrop="static"
    >
      <div
        class="modal-dialog modal-xl"
      >
        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              Pedido
              #{{ selectedOrder?.id }}
            </h5>

            <button
              class="btn-close"
              data-bs-dismiss="modal"
            />

          </div>

          <div
            v-if="selectedOrder"
            class="modal-body"
          >

            <div class="row">

              <!-- Cliente -->

              <div class="col-md-6 mb-4">

                <div class="card border-0 bg-light">
                  <div class="card-body">

                    <h6 class="fw-bold mb-3">
                      Cliente
                    </h6>

                    <p>
                      <strong>Nome:</strong>
                      {{ selectedOrder.customer_name }}
                    </p>

                    <p>
                      <strong>Email:</strong>
                      {{ selectedOrder.customer_email }}
                    </p>

                    <p>
                      <strong>Telefone:</strong>
                      {{ selectedOrder.customer_phone }}
                    </p>

                    <p class="mb-0">
                      <strong>CPF:</strong>
                      {{ selectedOrder.customer_cpf }}
                    </p>

                  </div>
                </div>

              </div>

              <!-- Entrega -->

              <div class="col-md-6 mb-4">

                <div class="card border-0 bg-light">
                  <div class="card-body">

                    <h6 class="fw-bold mb-3">
                      Localização
                    </h6>

                    <p>
                      <strong>Endereço:</strong>
                      {{ selectedOrder.street }},
                      {{ selectedOrder.number }}
                    </p>

                    <p
                      v-if="
                        selectedOrder.complement
                      "
                    >
                      <strong>Complemento:</strong>
                      {{
                        selectedOrder.complement
                      }}
                    </p>

                    <p>
                      <strong>Bairro:</strong>
                      {{
                        selectedOrder.neighborhood
                      }}
                    </p>

                    <p>
                      <strong>Cidade:</strong>
                      {{ selectedOrder.city }}
                      -
                      {{ selectedOrder.state }}
                    </p>

                    <p>
                      <strong>CEP:</strong>
                      {{ selectedOrder.cep }}
                    </p>

                  </div>
                </div>

              </div>

            </div>

            <!-- Status -->

            <div class="card border-0 bg-light mb-4">
              <div class="card-body">

                <div class="row">

                  <div class="col-md-6">

                    <label
                      class="form-label fw-semibold"
                    >
                      Status do Pedido
                    </label>

                    <select
                      v-model="
                        selectedOrder.status
                      "
                      class="form-select"
                    >
                      <option value="pending">
                        Pendente
                      </option>

                      <option value="processing">
                        Processando
                      </option>

                      <option value="shipped">
                        Enviado
                      </option>

                      <option value="delivered">
                        Entregue
                      </option>

                      <option value="cancelled">
                        Cancelado
                      </option>
                    </select>

                  </div>

                  <div class="col-md-6">

                    <label
                      class="form-label fw-semibold"
                    >
                      Status Pagamento
                    </label>

                    <select
                      v-model="
                        selectedOrder.payment_status
                      "
                      class="form-select"
                    >
                      <option value="pending">
                        Pendente
                      </option>

                      <option value="approved">
                        Aprovado
                      </option>

                      <option value="refunded">
                        Reembolsado
                      </option>

                      <option value="cancelled">
                        Cancelado
                      </option>
                    </select>

                  </div>

                </div>

              </div>
            </div>

            <!-- Produtos -->

            <div class="card border-0 shadow-sm">

              <div class="card-body">

                <h6 class="fw-bold mb-3">
                  Produtos
                </h6>

                <div
                  class="table-responsive"
                >

                  <table
                    class="table align-middle"
                  >

                    <thead>
                      <tr>
                        <th>Produto</th>
                        <th>Qtd</th>
                        <th>Valor</th>
                        <th>Subtotal</th>
                      </tr>
                    </thead>

                    <tbody>

                      <tr
                        v-for="item in selectedOrder.items"
                        :key="item.product_id"
                      >
                        <td>
                          {{
                            item.product_name
                          }}
                        </td>

                        <td>
                          {{
                            item.quantity
                          }}
                        </td>

                        <td>
                          {{
                            formatCurrency(
                              item.unit_price
                            )
                          }}
                        </td>

                        <td>
                          {{
                            formatCurrency(
                              item.quantity *
                              item.unit_price
                            )
                          }}
                        </td>
                      </tr>

                    </tbody>

                  </table>

                </div>

                <hr>

                <div class="text-end">

                  <div>
                    Subtotal:
                    <strong>
                      {{
                        formatCurrency(
                          selectedOrder.subtotal
                        )
                      }}
                    </strong>
                  </div>

                  <div>
                    Frete:
                    <strong>
                      {{
                        formatCurrency(
                          selectedOrder.shipping_cost
                        )
                      }}
                    </strong>
                  </div>

                  <h4
                    class="mt-3 fw-bold"
                  >
                    Total:
                    {{
                      formatCurrency(
                        selectedOrder.total_amount
                      )
                    }}
                  </h4>

                </div>

              </div>

            </div>

          </div>

          <div class="modal-footer">

            <button
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Fechar
            </button>

            <button
              class="btn btn-dark"
              @click="saveOrder"
            >
              Salvar Alterações
            </button>

          </div>

        </div>
      </div>
    </div>

  </div>
</template>
