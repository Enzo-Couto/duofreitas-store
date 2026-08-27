<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'

import categoryService from '../services/categoryService'

const toast = useToast()

const categories = ref([])

const editingId = ref(null)

const form = ref({
  name: '',
  slug: ''
})

async function loadCategories() {
  try {
    const response = await categoryService.getAll()

    categories.value = response.data
  } catch (error) {
    console.error(error)

    toast.error(
      'Erro ao carregar categorias'
    )
  }
}

function editCategory(category) {
  editingId.value = category.id

  form.value = {
    name: category.name,
    slug: category.slug
  }
}

function resetForm() {
  editingId.value = null

  form.value = {
    name: '',
    slug: ''
  }
}

async function saveCategory() {
  if (!form.value.name || !form.value.slug) {
    toast.warning(
      'Preencha todos os campos'
    )

    return
  }

  try {
    if (editingId.value) {
      await categoryService.update(
        editingId.value,
        form.value
      )

      toast.success(
        'Categoria atualizada com sucesso'
      )
    } else {
      await categoryService.create(
        form.value
      )

      toast.success(
        'Categoria criada com sucesso'
      )
    }

    resetForm()

    await loadCategories()

  } catch (error) {
    console.error(error)

    toast.error(
      error.response?.data?.detail ||
      'Erro ao salvar categoria'
    )
  }
}

async function deleteCategory(id) {
  const confirmed = confirm(
    'Deseja realmente excluir esta categoria?'
  )

  if (!confirmed) {
    return
  }

  try {
    await categoryService.remove(id)

    toast.success(
      'Categoria removida com sucesso'
    )

    await loadCategories()

  } catch (error) {
    console.log('ERRO COMPLETO:', error)
    console.log('RESPONSE:', error.response)
    console.log('DATA:', error.response?.data)

    toast.error(
      error.response?.data?.detail ||
      'Erro ao salvar categoria'
    )
  }
}

onMounted(async () => {
  await loadCategories()
})
</script>

<template>
  <div class="container-fluid">

    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >
      <div>
        <h2 class="fw-bold mb-0">
          Categorias
        </h2>

        <small class="text-muted">
          Gerencie as categorias da loja
        </small>
      </div>

      <button
        class="btn btn-dark"
        data-bs-toggle="modal"
        data-bs-target="#categoryModal"
        @click="resetForm"
      >
        + Nova Categoria
      </button>
    </div>

    <div class="row mb-4">

      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h6 class="text-muted">
              Total de Categorias
            </h6>

            <h3 class="fw-bold mb-0">
              {{ categories.length }}
            </h3>
          </div>
        </div>
      </div>

    </div>

    <div class="card border-0 shadow-sm">

      <div class="card-body">

        <h5 class="mb-3">
          Categorias cadastradas
        </h5>

        <div class="table-responsive">

          <table class="table table-hover align-middle">

            <thead>
              <tr>
                <th>Nome</th>
                <th>Slug</th>
                <th width="180">
                  Ações
                </th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="category in categories"
                :key="category.id"
              >
                <td class="fw-semibold">
                  {{ category.name }}
                </td>

                <td>
                  {{ category.slug }}
                </td>

                <td>

                  <button
                    class="btn btn-sm btn-primary me-2"
                    data-bs-toggle="modal"
                    data-bs-target="#categoryModal"
                    @click="editCategory(category)"
                  >
                    Editar
                  </button>

                  <button
                    class="btn btn-sm btn-danger"
                    @click="
                      deleteCategory(category.id)
                    "
                  >
                    Excluir
                  </button>

                </td>

              </tr>

              <tr
                v-if="!categories.length"
              >
                <td
                  colspan="3"
                  class="text-center text-muted"
                >
                  Nenhuma categoria cadastrada
                </td>
              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

    <div
      class="modal fade"
      id="categoryModal"
      tabindex="-1"
    >
      <div class="modal-dialog">

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              {{
                editingId
                  ? 'Editar Categoria'
                  : 'Nova Categoria'
              }}
            </h5>

            <button
              class="btn-close"
              data-bs-dismiss="modal"
            />

          </div>

          <div class="modal-body">

            <div class="mb-3">

              <label class="form-label">
                Nome
              </label>

              <input
                v-model="form.name"
                class="form-control"
              />

            </div>

            <div>

              <label class="form-label">
                Slug
              </label>

              <input
                v-model="form.slug"
                class="form-control"
              />

            </div>

          </div>

          <div class="modal-footer">

            <button
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Cancelar
            </button>

            <button
              class="btn btn-dark"
              @click="saveCategory"
            >
              {{
                editingId
                  ? 'Salvar Alterações'
                  : 'Criar Categoria'
              }}
            </button>

          </div>

        </div>

      </div>
    </div>

  </div>
</template>
