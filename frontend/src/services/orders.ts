import api from './api'

export async function createOrder(payload: any) {
  const { data } = await api.post(
    '/orders',
    payload
  )

  return data
}
