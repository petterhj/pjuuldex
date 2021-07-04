import Home from './views/Home.vue'
import Set from './views/Set.vue'
import Error from './views/Error.vue'

export const routes = [{
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: 'Home' }
  },
  {
    path: '/set/:slug',
    name: 'set',
    component: Set,
    meta: { title: 'Set' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'error',
    props: true,
    component: Error
  },
]