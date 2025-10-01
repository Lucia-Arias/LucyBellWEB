import { createRouter, createWebHistory } from 'vue-router'
import CatalogoContenido from '../Components/CatalogoContenido.vue'

const routes = [
  {
    path: '/',                // 👈 la ruta raíz
    name: 'home',
    component: CatalogoContenido
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

