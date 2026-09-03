<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'

import { Modal } from 'bootstrap'

import productService from '../services/productService'
import categoryService from '../services/categoryService'

const toast = useToast()

interface SelectedImage {
  id?: number
  file?: File
  preview: string
  type: 'front' | 'back' | 'gallery'
  existing?: boolean
}

interface ProductImage {
  id: number
  image_url: string
  image_type: string
}

interface Category {
  id: number
  name: string
}

interface Product {
  id: number
  name: string
  slug: string
  description: string

  price: number
  stock: number
  active: boolean

  weight: number
  height: number
  width: number
  length: number

  category?: Category | null
  images?: ProductImage[]
}

interface ProductForm {
  name: string
  description: string
  price: number
  stock: number
  active: boolean

  weight: number
  height: number
  width: number
  length: number

  category_id: number | null
}

const products = ref<Product[]>([])
const categories = ref<Category[]>([])

const editingId = ref<number | null>(null)

const form = ref<ProductForm>({
  name: '',
  description: '',
  price: 0,
  stock: 0,
  active: true,

  weight: 0.1,
  height: 1,
  width: 1,
  length: 1,

  category_id: null
})

const selectedImages = ref<SelectedImage[]>([])

function handleImages(event: Event) {

  const target = event.target as HTMLInputElement

  if (!target.files) return

  const files = Array.from(target.files)

  files.forEach(file => {

    selectedImages.value.push({
      file,
      preview: URL.createObjectURL(file),
      type:
        selectedImages.value.length === 0
          ? 'front'
          : selectedImages.value.length === 1
            ? 'back'
            : 'gallery'
    })

  })
}

async function removeImage(index: number) {

  const image =
    selectedImages.value[index]

  try {

    if (
      image.existing &&
      image.id
    ) {

      await productService.deleteImage(
        image.id
      )
    }

    URL.revokeObjectURL(
      image.preview
    )

    selectedImages.value.splice(
      index,
      1
    )

    toast.success(
      'Imagem removida'
    )

  } catch (error:any) {

    console.error(error)

    toast.error(
      'Erro ao remover imagem'
    )

  }
}

async function loadProducts() {
  try {
    const response =
      await productService.getAll()

    console.log(
      'PRODUTOS RECEBIDOS:',
      response.data
    )

    products.value = response.data

  } catch (error:any) {
    console.error(error)

    toast.error(
      'Erro ao carregar produtos'
    )
  }
}
async function loadCategories() {
  try {
    const response =
      await categoryService.getAll()

    categories.value = response.data
  } catch (error:any) {
    console.error(error)

    toast.error(
      'Erro ao carregar categorias'
    )
  }
}

function editProduct(product: Product) {

  editingId.value = product.id

  form.value = {
    name: product.name,
    description: product.description,
    price: Number(product.price),
    stock: product.stock,
    active: product.active,

    weight: Number(product.weight),
    height: product.height,
    width: product.width,
    length: product.length,

    category_id: product.category?.id || null
  }

  selectedImages.value = (
    product.images || []
  ).map(image => ({
    id: image.id,
    preview: `http://127.0.0.1:8000${image.image_url}`,
    type: image.image_type as 'front' | 'back' | 'gallery',
    existing: true
  }))

  openModal()
}

function resetForm() {

  editingId.value = null

  form.value = {
    name: '',
    description: '',
    price: 0,
    stock: 0,
    active: true,

    weight: 0.1,
    height: 1,
    width: 1,
    length: 1,

    category_id: null
  }

  selectedImages.value.forEach(image => {
    URL.revokeObjectURL(image.preview)
  })

  selectedImages.value = []
}

async function saveProduct() {

  if (!form.value.name) {
    toast.warning(
      'Informe o nome do produto'
    )
    return
  }

  if (!form.value.price || Number(form.value.price) <= 0) {
    toast.warning(
      'O preço deve ser maior que zero'
    )

    return
  }

  const price =
    parseFloat(
      String(form.value.price)
        .replace(',', '.')
    )

  if (isNaN(price) || price <= 0) {
    toast.warning(
      'Informe um preço válido'
    )

    return
  }

  form.value.price = price

  try {

    console.log('Modo edição?', editingId.value)
    console.log('Dados enviados:', form.value)

    if (editingId.value) {

      const response =
        await productService.update(
          editingId.value,
          form.value
        )

      console.log(
        'UPDATE OK:',
        response
      )

      toast.success(
        'Produto atualizado com sucesso'
      )

    } else {

      const response =
        await productService.create(
          form.value
        )

      const productId =
        response.data.id

      for (const image of selectedImages.value) {

        if (!image.file) {
          continue
        }

        await productService.uploadImage(
          productId,
          image.file,
          image.type
        )
      }

      console.log(
        'CREATE OK:',
        response
      )

      toast.success(
        'Produto criado com sucesso'
      )
    }

    await loadProducts()

    resetForm()

    const modalEl =
      document.getElementById('productModal')

    if (modalEl) {

      if (!modalEl) {
        return
      }

      const modalInstance =
        Modal.getOrCreateInstance(modalEl)

      modalInstance.hide()

      setTimeout(() => {
        document.body.classList.remove('modal-open')

        document
          .querySelectorAll('.modal-backdrop')
          .forEach(el => el.remove())

        modalEl.style.display = ''
        modalEl.setAttribute(
          'aria-hidden',
          'true'
        )
      }, 300)
    }

  } catch (error: any) {

    console.error('ERRO COMPLETO:', error)

    if (error.response) {

      console.error(
        'STATUS:',
        error.response.status
      )

      console.error(
        'URL:',
        error.config?.url
      )

      console.error(
        'METHOD:',
        error.config?.method
      )

      console.error(
        'DATA:',
        error.response.data
      )

    } else {

      console.error(
        'SEM RESPONSE:',
        error
      )
    }

    toast.error(
      error.response?.data?.detail ||
      error.message ||
      'Erro ao salvar produto'
    )
  }
}

function openModal() {
  const modalEl =
    document.getElementById('productModal')

  if (!modalEl) {
    return
  }

  const modal =
    Modal.getOrCreateInstance(modalEl)

  modal.show()
}

async function deleteProduct(id: number) {

  const confirmed = confirm(
    'Deseja realmente excluir este produto?'
  )

  if (!confirmed) {
    return
  }

  try {

    await productService.remove(id)

    toast.success(
      'Produto removido com sucesso'
    )

    await loadProducts()

  } catch (error: any) {

    console.error(error)

    toast.error(
      error.response?.data?.detail ||
      'Erro ao excluir produto'
    )

  }
}

onMounted(async () => {

  await Promise.all([
    loadProducts(),
    loadCategories()
  ])

})
</script>

<template>
  <div class="container-fluid py-4">

    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >
      <div>
        <h2 class="fw-bold mb-1">
          Produtos
        </h2>

        <p class="text-muted mb-0">
          Gerencie os produtos da loja
        </p>
      </div>

      <button
        class="btn btn-dark"
        @click="
          resetForm();
          openModal();
        "
      >
        + Novo Produto
      </button>
    </div>

    <div class="row mb-4">

      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h6 class="text-muted">
              Total de Produtos
            </h6>

            <h2 class="fw-bold">
              {{ products.length }}
            </h2>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h6 class="text-muted">
              Produtos Ativos
            </h6>

            <h2 class="fw-bold text-success">
              {{
                products.filter(
                  p => p.active
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
              Categorias Utilizadas
            </h6>

            <h2 class="fw-bold text-primary">
              {{
                [...new Set(
                  products
                    .filter(
                      p => p.category
                    )
                    .map(
                      p => p.category!.id
                    )
                )].length
              }}
            </h2>
          </div>
        </div>
      </div>

    </div>

    <div class="card border-0 shadow-sm">

      <div class="card-body">

        <div
          class="d-flex justify-content-between align-items-center mb-3"
        >
          <h5 class="mb-0">
            Produtos cadastrados
          </h5>
        </div>

        <div class="table-responsive">

          <table class="table table-hover align-middle">

            <thead>
              <tr>
                <th>Produto</th>
                <th>Preço</th>
                <th>Estoque</th>
                <th>Peso</th>
                <th>Dimensões</th>
                <th>Categoria</th>
                <th>Status</th>
                <th width="180">
                  Ações
                </th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="product in products"
                :key="product.id"
              >
                <td>
                  <div>
                    <strong>
                      {{ product.name }}
                    </strong>

                    <div
                      class="text-muted small"
                    >
                      {{ product.slug }}
                    </div>
                  </div>
                </td>

                <td>
                  R$
                  {{
                    Number(
                      product.price
                    ).toFixed(2)
                  }}
                </td>

                <td>
                  {{ product.stock }}
                </td>

                <td>
                    {{ product.weight }} kg
                </td>

                <td>
                    {{ product.height }} x {{ product.width }} x {{ product.length }}
                </td>

                <td>

                  <span
                    v-if="product.category"
                    class="badge bg-primary"
                  >
                    {{
                      product.category.name
                    }}
                  </span>

                  <span
                    v-else
                    class="badge bg-secondary"
                  >
                    Sem categoria
                  </span>

                </td>

                <td>

                    <span
                      v-if="!product.active"
                      class="badge bg-danger"
                    >
                      Inativo
                    </span>

                    <span
                      v-else-if="product.stock <= 0"
                      class="badge bg-warning text-dark"
                    >
                      Esgotado
                    </span>

                    <span
                      v-else
                      class="badge bg-success"
                    >
                      Ativo
                    </span>

                </td>

                <td>

                    <button
                      class="btn btn-sm btn-outline-primary me-2"
                      @click="editProduct(product)"
                    >
                      Editar
                    </button>

                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="
                      deleteProduct(
                        product.id
                      )
                    "
                  >
                    Excluir
                  </button>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

    <div
      class="modal fade"
      id="productModal"
      tabindex="-1"
      data-bs-backdrop="static"
    >
      <div class="modal-dialog modal-lg">

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              {{
                editingId
                  ? 'Editar Produto'
                  : 'Novo Produto'
              }}
            </h5>

            <button
              class="btn-close"
              data-bs-dismiss="modal"
            />
          </div>

          <div class="modal-body">

            <div class="row g-3">

              <div class="col-md-6">
                <label class="form-label">
                  Nome
                </label>

                <input
                  v-model="form.name"
                  class="form-control"
                >
              </div>

              <div class="col-12">
                <label class="form-label">
                  Descrição
                </label>

                <textarea
                  v-model="form.description"
                  class="form-control"
                  rows="4"
                />
              </div>

              <!-- Linha 1 -->

              <div class="row mb-3">

                <div class="col-md-3">
                  <label class="form-label">Preço</label>

                  <input
                    v-model="form.price"
                    type="number"
                    step="0.01"
                    class="form-control"
                  >
                </div>

                <div class="col-md-3">
                  <label class="form-label">Estoque</label>

                  <input
                    v-model="form.stock"
                    type="number"
                    class="form-control"
                  >
                </div>

              </div>

              <!-- Linha 2 -->

              <div class="row mb-3">

                <div class="col-md-3">
                  <label class="form-label">Peso (kg)</label>

                  <input
                    v-model="form.weight"
                    type="number"
                    step="0.001"
                    class="form-control"
                  >
                </div>

                <div class="col-md-2">
                  <label class="form-label">Altura</label>

                  <input
                    v-model="form.height"
                    type="number"
                    class="form-control"
                  >
                </div>

                <div class="col-md-2">
                  <label class="form-label">Largura</label>

                  <input
                    v-model="form.width"
                    type="number"
                    class="form-control"
                  >
                </div>

                <div class="col-md-2">
                  <label class="form-label">Comprimento</label>

                  <input
                    v-model="form.length"
                    type="number"
                    class="form-control"
                  >
                </div>

              </div>

              <div class="col-12">

                <label class="form-label">
                  Imagens
                </label>

                <input
                  type="file"
                  multiple
                  accept="image/*"
                  class="form-control"
                  @change="handleImages"
                />

              </div>

              <div
                v-if="selectedImages.length"
                class="col-12"
              >

                <div class="row g-3">

                  <div
                    v-for="(image, index) in selectedImages"
                    :key="index"
                    class="col-md-3"
                  >

                    <div
                      class="card position-relative"
                    >

                      <button
                        type="button"
                        class="btn btn-danger btn-sm position-absolute top-0 end-0 m-1"
                        @click="removeImage(index)"
                      >
                        ×
                      </button>

                      <img
                        :src="image.preview"
                        class="card-img-top"
                        style="
                          height: 180px;
                          object-fit: cover;
                        "
                      >

                      <div class="card-body">

                        <select
                          v-model="image.type"
                          class="form-select form-select-sm"
                        >
                          <option value="front">
                            Frente
                          </option>

                          <option value="back">
                            Costas
                          </option>

                          <option value="gallery">
                            Galeria
                          </option>
                        </select>

                      </div>

                    </div>

                  </div>

                </div>

              </div>

              <div class="col-md-4">
                <label class="form-label">
                  Categoria
                </label>

                <select
                  v-model="form.category_id"
                  class="form-select"
                >
                  <option
                    :value="null"
                  >
                    Sem categoria
                  </option>

                  <option
                    v-for="category in categories"
                    :key="category.id"
                    :value="category.id"
                  >
                    {{ category.name }}
                  </option>

                </select>
              </div>

              <div
                class="col-md-2 d-flex align-items-end"
              >
                <div
                  class="form-check"
                >
                  <input
                    v-model="form.active"
                    class="form-check-input"
                    type="checkbox"
                  >

                  <label
                    class="form-check-label"
                  >
                    Ativo
                  </label>
                </div>
              </div>

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
              @click="saveProduct"
            >
              {{
                editingId
                  ? 'Salvar'
                  : 'Criar Produto'
              }}
            </button>

          </div>

        </div>

      </div>
    </div>

  </div>
</template>
