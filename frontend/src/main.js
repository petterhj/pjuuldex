import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import { routes } from './routes.js'
import { store } from './store'
import VueCirrus from 'vue-cirrus';
import 'vue-cirrus/dist/vue-cirrus.css';
import 'jetbrains-mono'
import '@mdi/font/css/materialdesignicons.css'
import './assets/main.scss'


const router = createRouter({
    history: createWebHistory(import.meta.env.VITE_APP_BASE_PATH),
    routes,
})

const app = createApp(App)

app.use(router)
app.use(store)
app.use(VueCirrus)

app.mount('#app')
