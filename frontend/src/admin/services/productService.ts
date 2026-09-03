import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export default {

  getAll() {
    return api.get('/products')
  },

  getBySlug(slug: string) {
    return api.get(`/products/slug/${slug}`)
  },

  create(data: any) {
    return api.post('/products/', data)
  },

  update(id: number, data: any) {
    return api.put(`/products/${id}`, data)
  },

  remove(id: number) {
    return api.delete(`/products/${id}`)
  },

  deleteImage(imageId: number) {
    return api.delete(
      `/products/images/${imageId}`
    )
  },

  uploadImage(
    productId: number,
    file: File,
    imageType: string
  ) {

    const formData = new FormData()

    formData.append(
      'file',
      file
    )

    formData.append(
      'image_type',
      imageType
    )

    return api.post(
      `/products/${productId}/images`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
  },

}
