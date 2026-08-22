import { defineStore } from 'pinia'

export const useCheckoutStore = defineStore(
  'checkout',
  {
    state: () => ({
      customer: {
        name: '',
        cpf: '',
        email: '',
        phone: '',
      },

      address: {
        cep: '',
        street: '',
        number: '',
        complement: '',
        neighborhood: '',
        city: '',
        state: '',
      },

      orderId: null as number | null,
    }),

    actions: {
      clear() {
        this.customer = {
          name: '',
          cpf: '',
          email: '',
          phone: '',
        }

        this.address = {
          cep: '',
          street: '',
          number: '',
          complement: '',
          neighborhood: '',
          city: '',
          state: '',
        }

        this.orderId = null
      },
    },
  }
)
