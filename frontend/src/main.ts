import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { vMaska } from 'maska/vue'

import App from './App.vue'
import router from './router'

import Toast from 'vue-toastification'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import 'vue-toastification/dist/index.css'
import './assets/styles/main.css'

const app = createApp(App)

app.directive('maska', vMaska)

app.use(createPinia())
app.use(router)

app.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnHover: true,
})

app.mount('#app')
