import api from '@/services/api'

export default {

  async getStats() {

    const response =
      await api.get(
        '/dashboard/stats'
      )

    return response.data
  }

}
