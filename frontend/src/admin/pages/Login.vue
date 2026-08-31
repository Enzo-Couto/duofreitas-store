<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const email = ref('')
const password = ref('')

const loading = ref(false)
const error = ref('')

async function login() {
  try {
    loading.value = true
    error.value = ''

    const response = await axios.post(
      'http://127.0.0.1:8000/auth/login',
      {
        email: email.value,
        password: password.value
      }
    )

    localStorage.setItem(
      'admin_token',
      response.data.access_token
    )

    router.push('/admin')

  } catch (err: any) {
    error.value =
      err.response?.data?.detail ||
      'Erro ao fazer login'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="flex min-h-screen items-center justify-center bg-zinc-100"
  >
    <div
      class="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg"
    >
      <h1
        class="mb-6 text-center text-3xl font-bold"
      >
        Duo Freitas Admin
      </h1>

      <form
        @submit.prevent="login"
        class="space-y-4"
      >
        <div>
          <label class="mb-2 block">
            E-mail
          </label>

          <input
            v-model="email"
            type="email"
            class="w-full rounded-lg border p-3"
          />
        </div>

        <div>
          <label class="mb-2 block">
            Senha
          </label>

          <input
            v-model="password"
            type="password"
            class="w-full rounded-lg border p-3"
          />
        </div>

        <p
          v-if="error"
          class="text-sm text-red-500"
        >
          {{ error }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="cursor-pointer w-full rounded-lg bg-black py-3 text-white"
        >
          {{
            loading
              ? 'Entrando...'
              : 'Entrar'
          }}
        </button>
      </form>
    </div>
  </div>
</template>
