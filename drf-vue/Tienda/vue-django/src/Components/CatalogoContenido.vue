<template>
<!-- CATALOGO CONTENIDO -->

  <main class="p-3">
    <h2 class="section-title">Catálogo</h2>

    <div class="row">
      <div class="col-md-4 mb-4" v-for="i in 6" :key="i">
        <div class="card-producto shadow-sm">
          <div class="producto-imagen-wrapper">
            <img
              src="https://res.cloudinary.com/dm0fp1sru/image/upload/v1757033474/Collar_Stich_ihgw8d.jpg"
              alt="Producto ejemplo"
              class="img-fluid mb-3 rounded"
            />
            <span class="producto-etiqueta">Collar de Acero Quirúrgico</span>
          </div>
          <h5 class="producto-nombre">Collar Stich</h5>
          <p class="producto-precio">$3.000</p>

          <!-- Selección de color -->
          <div class="seleccion-container">
            <p class="seleccion-label">Color:</p>
            <div class="seleccion-opciones">
              <button
                v-for="(color, index) in colores"
                :key="index"
                @click="seleccionarColor(i, color)"
                :class="['seleccion-btn', { 'activo': coloresSeleccionados[i] === color }]"
              >
                {{ color }}
              </button>
            </div>
          </div>

          <!-- Selección de talle -->
          <div class="seleccion-container">
            <p class="seleccion-label">Talle:</p>
            <div class="seleccion-opciones">
              <button
                v-for="(t, index) in talles"
                :key="index"
                @click="seleccionarTalle(i, t)"
                :class="['seleccion-btn', { 'activo': tallesSeleccionados[i] === t }]"
              >
                {{ t }}
              </button>
            </div>
          </div>

          <!-- Cantidad y agregar al carrito -->
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
</template>

<script>
export default {
  name: "CatalogoContenido",
  props: {
    colores: Array,
    talles: Array,
    coloresSeleccionados: Array,
    tallesSeleccionados: Array,
    cantidades: Array,
    seleccionarColor: Function,
    seleccionarTalle: Function,
    incrementar: Function,
    decrementar: Function,
    agregarAlCarrito: Function
  }
}
</script>
