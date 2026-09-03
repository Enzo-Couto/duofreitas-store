import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export default {
  getAll() {
    return api.get('/categories')
  },

  create(data: any) {
    return api.post('/categories', data)
  },

  remove(id: number) {
    return api.delete(`/categories/${id}`)
  },

  update(id: number, data: any) {
    return api.put(`/categories/${id}`, data)
  }
}
