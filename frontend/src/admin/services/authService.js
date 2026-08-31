import api from '@/services/api'

export default {

  login(data: any) {
    return api.post(
      '/auth/login',
      data
    )
  }

}
