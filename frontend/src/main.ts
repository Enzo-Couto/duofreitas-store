import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { vMaska } from 'maska/vue'

import App from './App.vue'
import router from './router'

import './assets/styles/main.css'

const app = createApp(App)

app.directive('maska', vMaska)

app.use(createPinia())
app.use(router)

app.mount('#app')
