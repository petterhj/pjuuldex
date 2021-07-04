import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import { routes } from './routes.js'
import { store } from './store'
import VueCirrus from 'vue-cirrus';
import 'vue-cirrus/dist/vue-cirrus.css';
// import dayjs from 'dayjs'
// import calendar from 'dayjs/plugin/calendar'
// import duration from 'dayjs/plugin/duration'
import 'jetbrains-mono'
import '@mdi/font/css/materialdesignicons.css'
import './assets/main.scss'

const router = createRouter({
    history: createWebHistory(),
    routes,
})

const app = createApp(App)

app.use(router)
app.use(store)
app.use(VueCirrus)

// dayjs.extend(calendar)
// dayjs.extend(duration)
// app.config.globalProperties.$dayjs = dayjs

app.mount('#app')
