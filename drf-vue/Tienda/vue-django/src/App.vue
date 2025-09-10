<template>
  <div class="app-container">
    <!-- HEADER -->
    <header class="custom-header d-flex justify-content-between align-items-center">
      <button class="btn btn-icon" @click="toggleSidebar">
        <i class="bi bi-list"></i>
      </button>
      <h1 class="logo-text">LucyBell</h1>
      <button class="btn btn-icon">
        <i class="bi bi-cart"></i>
      </button>
    </header>

    <!-- OVERLAY -->
    <div v-if="sidebarOpen" class="overlay" @click="closeSidebar"></div>

    <!-- SIDEBAR -->
    <div :class="['sidebar shadow', { 'active': sidebarOpen }]">
      <div class="p-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="sidebar-title">Productos</h4>
          <button class="btn btn-icon" @click="closeSidebar">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <input type="text" class="form-control mb-3 search-box" placeholder="Buscar producto..."
          v-model="searchQuery" />

        <h6 class="filter-title">Filtrar por categoría</h6>
        <ul class="list-unstyled">
          <li><a href="#" class="sidebar-link" @click="closeSidebar">Anillos</a></li>
          <li><a href="#" class="sidebar-link" @click="closeSidebar">Pulseras</a></li>
          <li><a href="#" class="sidebar-link" @click="closeSidebar">Collares</a></li>
        </ul>
      </div>
    </div>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="p-3">
      <h2 class="section-title">Catálogo</h2>

      <div class="row">
        <!-- Card de ejemplo -->
        <div class="col-md-4 mb-4" v-for="i in 6" :key="i">
          <div class="card-producto shadow-sm">
            <div class="producto-imagen-wrapper">
              <img src="https://res.cloudinary.com/dm0fp1sru/image/upload/v1757033474/Collar_Stich_ihgw8d.jpg"
                alt="Producto ejemplo" class="img-fluid mb-3 rounded" />
              <span class="producto-etiqueta">Collar de Acero Quirúrgico</span>
            </div>
            <h5 class="producto-nombre">Collar Stich</h5>
            <p class="producto-precio">$3.000</p>
            <!-- Selección de color -->
            <div class="seleccion-container">
              <p class="seleccion-label">Color:</p>
              <div class="seleccion-opciones">
                <button v-for="(color, index) in colores" :key="index" @click="seleccionarColor(i, color)"
                  :class="['seleccion-btn', { 'activo': coloresSeleccionados[i] === color }]">
                  {{ color }}
                </button>
              </div>
            </div>

            <!-- Selección de talle -->
            <div class="seleccion-container">
              <p class="seleccion-label">Talle:</p>
              <div class="seleccion-opciones">
                <button v-for="(t, index) in talles" :key="index" @click="seleccionarTalle(i, t)"
                  :class="['seleccion-btn', { 'activo': tallesSeleccionados[i] === t }]">
                  {{ t }}
                </button>
              </div>
            </div>
            <div class="cantidad-container">
              <button class="btn-cantidad" @click="decrementar(i)">-</button>
              <span class="cantidad">{{ cantidades[i] }}</span>
              <button class="btn-cantidad" @click="incrementar(i)">+</button>
              <button class="btn-comprar" @click="agregarAlCarrito(i)">Agregar al carrito</button>
            </div>

          </div>

        </div>
      </div>
    </main>

    <footer class="text-center py-4 my-4 border-top">
      <p>&copy; 2025 LucyBell_Cba Seguinos en Instagram :DD </p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue"

const sidebarOpen = ref(false)
const searchQuery = ref("")


// Definir colores y talles disponibles
const colores = ["Rojo", "Azul", "Amarillo", "Verde"]
const talles = ["S", "M", "L", "XL"]

// Selección por producto (índice i)
const coloresSeleccionados = ref(Array(6).fill(colores[0])) // por defecto primer color
const tallesSeleccionados = ref(Array(6).fill(talles[0]))   // por defecto primer talle

function seleccionarColor(index, color) {
  coloresSeleccionados.value[index] = color
}

function seleccionarTalle(index, talle) {
  tallesSeleccionados.value[index] = talle
}


/*CONTADOR Y AGREGAR AL CARRITO*/
const cantidades = ref(Array(6).fill(1)) // inicia con 1 unidad por producto

function incrementar(index) {
  cantidades.value[index]++
}

function decrementar(index) {
  if (cantidades.value[index] > 1) {
    cantidades.value[index]--
  }
}

function agregarAlCarrito(index) {
  const cantidadSeleccionada = cantidades.value[index]
  console.log(`Producto ${index} agregado: ${cantidadSeleccionada} unidades`)
  // Aquí iría la lógica para agregar al carrito real
}

/* OTROS */
function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}
</script>

<style>
/* PALETA LUCYBELL */
:root {
  --lucybell-bg: #fbebe3;
  --lucybell-accent: #9c85c9;
  --lucybell-dark: #352e35;
  --lucybell-light: #ffffff;
  --lucybell-accent-dark: #7a61a8;
}

/* TIPOGRAFÍA */
@import url('https://fonts.googleapis.com/css2?family=Handlee&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

/* FONDO GENERAL */
.app-container {
  min-height: 100vh;
  background-color: var(--lucybell-bg);
  font-family: 'Poppins', sans-serif;
}

/* HEADER */
.custom-header {
  background-color: var(--lucybell-bg);
  color: var(--lucybell-dark);
  padding: 12px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-bottom: 3px solid var(--lucybell-accent);
}

.logo-text {
  font-family: 'Handlee';
  font-size: 2.5rem;
  margin: 0;
  color: var(--lucybell-dark);
}

.btn-icon i {
  font-size: 1.5rem;
  color: var(--lucybell-dark);
  transition: transform 0.2s ease, color 0.2s ease;
}

.btn-icon:hover {
  transform: scale(1.1);
  color: var(--lucybell-accent);
}

/* SIDEBAR */
.sidebar {
  position: fixed;
  top: 0;
  left: -260px;
  width: 260px;
  height: 100%;
  background-color: var(--lucybell-bg);
  border-right: 2px solid var(--lucybell-accent);
  transition: left 0.3s ease;
  z-index: 1051;
  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.05);
}

.sidebar.active {
  left: 0;
}

.sidebar-title {
  font-weight: 600;
  color: var(--lucybell-accent);
}

.filter-title {
  font-size: 0.9rem;
  color: var(--lucybell-dark);
  margin-top: 15px;
}

.sidebar-link {
  display: block;
  padding: 5px 0;
  color: var(--lucybell-dark);
  text-decoration: none;
  transition: color 0.2s ease;
}

.sidebar-link:hover {
  color: var(--lucybell-accent);
}

/* BUSCADOR */
.search-box {
  border: 1px solid var(--lucybell-accent);
  border-radius: 8px;
  padding: 6px 12px;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.search-box:focus {
  border-color: var(--lucybell-dark);
  box-shadow: 0 0 8px rgba(156, 133, 201, 0.4);
}

/* OVERLAY */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(74, 44, 42, 0.25);
  z-index: 1050;
}

/* SECCIONES */
.section-title {
  font-weight: 600;
  color: var(--lucybell-dark);
  margin-bottom: 20px;
}

/* CARD DE PRODUCTOS */
.card-producto {
  background-color: var(--lucybell-accent);
  border-radius: 14px;
  border-bottom: 3px solid var(--lucybell-accent);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  padding: 20px;
  text-align: center;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.card-producto:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
}

.producto-nombre {
  font-weight: 600;
  color: var(--lucybell-dark);
  margin-bottom: 6px;
}

.producto-precio {
  color: var(--lucybell-dark);
  margin-bottom: 12px;
  font-size: 1.05rem;
}

/* BOTONES DE COMPRA */
.btn-comprar {
  background-color: var(--lucybell-bg);
  color: var(--lucybell-dark);
  border-radius: 10px;
  padding: 10px 18px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
  box-shadow: 0 4px 12px rgba(156, 133, 201, 0.4);
}

.btn-comprar:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
  box-shadow: 0 6px 18px rgba(156, 133, 201, 0.55);
}

/* FOOTER */
footer {
  background-color: var(--lucybell-bg);
  color: var(--lucybell-dark);
  border-top: 3px solid var(--lucybell-accent);
  text-align: center;
  padding: 18px 0;
  margin-top: 30px;
}

/* Etiqueta Categoria y Material*/

.producto-imagen-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
}

.producto-etiqueta {
  position: absolute;
  left: 10px;
  bottom: 10px;
  background-color: var(--lucybell-bg);
  color: var(--lucybell-dark);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

/* CONTADOR */
.cantidad-container {
  display: flex;
  align-items: center;
  gap: 6px;
  justify-content: center;
  margin-top: 10px;
}

.btn-cantidad {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background-color: var(--lucybell-bg);
  color: var(--lucybell-dark);
  font-weight: 600;
  cursor: pointer;
  transition: filter 0.2s ease;
}

.btn-cantidad:hover {
  filter: brightness(1.1);
}

.cantidad {
  min-width: 20px;
  text-align: center;
  font-weight: 600;
}

/* Selector de Talles y Colores*/
.seleccion-container {
  margin-bottom: 10px;
  text-align: center;
}

.seleccion-label {
  display: inline-block;
  margin-right: 8px;
  font-weight: 600;
  color: var(--lucybell-dark);
}

.seleccion-opciones {
  display: inline-flex;
  gap: 6px;
  flex-wrap: wrap;
}

.seleccion-btn {
  border: 1px solid var(--lucybell-dark);
  background-color: var(--lucybell-bg);
  color: var(--lucybell-dark);
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s;
}

.seleccion-btn:hover {
  filter: brightness(1.1);
}

.seleccion-btn.activo {
  background-color: var(--lucybell-accent);
  color: var(--lucybell-light);
  border-color: var(--lucybell-accent-dark);
}

</style>
