import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export default {

  getAll() {
    return api.get('/products')
  },

  create(data) {
    return api.post('/products/', data)
  },

  update(id, data) {
    return api.put(`/products/${id}`, data)
  },

  remove(id) {
    return api.delete(`/products/${id}`)
  },

  deleteImage(imageId) {
    return api.delete(
      `/products/images/${imageId}`
    )
  },

  uploadImage(
    productId,
    file,
    imageType
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
