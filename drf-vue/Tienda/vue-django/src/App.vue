<template>
  <div class="app-container">
    
    <!-- HEADER -->
    <HeaderComponent
      @toggle-sidebar="toggleSidebar"
      @toggle-carrito="toggleCarrito"
    />

    <!-- OVERLAYS -->
    <div v-if="sidebarOpen" class="overlay" @click="closeSidebar"></div>
    <div v-if="carritoOpen" class="overlay" @click="closeCarrito"></div>
    
    <!-- SIDEBAR del carrito -->
    <CarritoSidebar
      :carrito-open="carritoOpen"
      :carrito="carrito"
      @close-carrito="closeCarrito"
      @finalizar-compra="finalizarCompra"
    />

    <!-- SIDEBAR de Productos-->
    <ProductosSidebar
      :sidebar-open="sidebarOpen"
      v-model:searchQuery="searchQuery"
      @close-sidebar="closeSidebar"
    />

    <!-- CONTENIDO PRINCIPAL -->
    <CatalogoContenido
      :colores="colores"
      :talles="talles"
      :coloresSeleccionados="coloresSeleccionados"
      :tallesSeleccionados="tallesSeleccionados"
      :cantidades="cantidades"
      :seleccionarColor="seleccionarColor"
      :seleccionarTalle="seleccionarTalle"
      :incrementar="incrementar"
      :decrementar="decrementar"
      :agregarAlCarrito="agregarAlCarrito"
    />

    <!-- FOOTER -->
    <FooterComponent/>
    
  </div>
</template>

<script>
import { ref } from "vue"
import HeaderComponent from "./Components/HeaderComponent.vue"
import CarritoSidebar from "./Components/CarritoSidebar.vue"
import ProductosSidebar from "./Components/ProductosSidebar.vue"
import FooterComponent from "./Components/FooterComponent.vue"
import CatalogoContenido from "./Components/CatalogoContenido.vue"

export default {
  name: "App",
  components: {
    HeaderComponent,
    CarritoSidebar,
    ProductosSidebar,
    FooterComponent,
    CatalogoContenido
  },
  setup() {
    const sidebarOpen = ref(false)
    const carritoOpen = ref(false)
    const carrito = ref([])
    const searchQuery = ref("")

    const toggleSidebar = () => { sidebarOpen.value = !sidebarOpen.value }
    const closeSidebar = () => { sidebarOpen.value = false }
    const toggleCarrito = () => { carritoOpen.value = !carritoOpen.value }
    const closeCarrito = () => { carritoOpen.value = false }

    const finalizarCompra = () => { carrito.value = [] }

    const colores = ["Rojo", "Azul", "Amarillo", "Verde"]
    const talles = ["S", "M", "L", "XL"]
    const coloresSeleccionados = ref(Array(6).fill(colores[0]))
    const tallesSeleccionados = ref(Array(6).fill(talles[0]))
    const cantidades = ref(Array(6).fill(1))

    const seleccionarColor = (index, color) => { coloresSeleccionados.value[index] = color }
    const seleccionarTalle = (index, talle) => { tallesSeleccionados.value[index] = talle }
    const incrementar = (i) => { cantidades.value[i]++ }
    const decrementar = (i) => { if (cantidades.value[i] > 1) cantidades.value[i]-- }
    const agregarAlCarrito = (i) => {
      const cantidadSeleccionada = cantidades.value[i]
      carrito.value.push({
        productoId: i,
        cantidad: cantidadSeleccionada,
        color: coloresSeleccionados.value[i],
        talle: tallesSeleccionados.value[i]
      })
    }

    return {
      sidebarOpen, carritoOpen, carrito, searchQuery,
      toggleSidebar, closeSidebar, toggleCarrito, closeCarrito,
      finalizarCompra,
      colores, talles, coloresSeleccionados, tallesSeleccionados,
      cantidades, seleccionarColor, seleccionarTalle,
      incrementar, decrementar, agregarAlCarrito
    }
  }
}
</script>
