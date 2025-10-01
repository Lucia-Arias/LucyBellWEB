<template>
<!-- CATALOGO CONTENIDO -->

  <main class="p-3">
    <h2 class="section-title">Catálogo</h2>

    <div class="row">
      <div class="col-md-4 mb-4" v-for="product in products" :key="product.id">
        <div class="card-producto shadow-sm">
          <div class="producto-imagen-wrapper">
            <img
              :src="product.image"
              alt="Imagen de {{ product.name }}"
              class="img-fluid mb-3 rounded"
            />
            <span class="producto-etiqueta">{{product.category_name}} de {{ product.material_name }}</span>
          </div>
          <h5 class="producto-nombre">{{ product.name }}</h5>
          <p class="producto-precio">${{ product.price }}</p>

          <!-- Selección de color -->
          <div class="seleccion-container">
            <p class="seleccion-label">Color:</p>
            <div class="seleccion-opciones">
              <button
                v-for="(color, index) in colores"
                :key="index"
                @click="seleccionarColor(product.id, color)"
                :class="['seleccion-btn', { 'activo': coloresSeleccionados[product.id] === color }]"
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
                @click="seleccionarTalle(product.id, t)"
                :class="['seleccion-btn', { 'activo': tallesSeleccionados[product.id] === t }]"
              >
                {{ t }}
              </button>
            </div>
          </div>

          <!-- Cantidad y agregar al carrito -->
          <div class="cantidad-container">
            <button class="btn-cantidad" @click="decrementar(product.id)">-</button>
            <span class="cantidad">{{ cantidades[product.id] }}</span>
            <button class="btn-cantidad" @click="incrementar(product.id)">+</button>
            <button class="btn-comprar" @click="agregarAlCarrito(product.id)">Agregar al carrito</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios';

export default {
  name: "CatalogoContenido",
  data(){
    return{
      products:[]
    }
  },
  mounted(){
    axios.get('http://127.0.0.1:8000/api/products/')
    .then(response => {
      this.products = response.data
    })
    .catch(error => {
      console.log(error)
    }
    )
  },
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
