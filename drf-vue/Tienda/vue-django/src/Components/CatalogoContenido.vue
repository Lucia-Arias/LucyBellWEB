<template>
<!-- CATALOGO CONTENIDO -->
  <main class="p-3">
    <h2 class="section-title">Catálogo</h2>

    <div class="row">
      <div class="col-md-4 mb-4" v-for="product in products" :key="product.id">
        <div class="card-producto shadow-sm">
          <div class="producto-contenido">
            <!-- Imagen y etiqueta -->
            <div class="producto-imagen-wrapper">
              <img
                :src="product.image"
                alt="Imagen de {{ product.name }}"
                class="img-fluid mb-3 rounded"
              />
              <span class="producto-etiqueta">{{product.category_name}} de {{ product.material_name }}</span>
            </div>
            
            <!-- Nombre y precio -->
            <h5 class="producto-nombre">{{ product.name }}</h5>
            <p class="producto-precio">${{ product.price }}</p>

            <!-- Contenedor para selectores -->
            <div class="selectores-container">
              <!-- Selección de color - Solo muestra si el producto tiene colores disponibles -->
              <div class="seleccion-container" v-if="product.colores_disponibles && product.colores_disponibles.length > 0">
                <p class="seleccion-label">Color:</p>
                <div class="seleccion-opciones">
                  <button
                    v-for="(color, index) in product.colores_disponibles"
                    :key="index"
                    @click="seleccionarColor(product.id, color)"
                    :class="['seleccion-btn', { 'activo': coloresSeleccionados[product.id] === color }]"
                  >
                    {{ color }}
                  </button>
                </div>
              </div>

              <!-- Selección de talle - Solo muestra si el producto tiene talles disponibles -->
              <div class="seleccion-container" v-if="product.talles_disponibles && product.talles_disponibles.length > 0">
                <p class="seleccion-label">Talle:</p>
                <div class="seleccion-opciones">
                  <button
                    v-for="(talle, index) in product.talles_disponibles"
                    :key="index"
                    @click="seleccionarTalle(product.id, talle)"
                    :class="['seleccion-btn', { 'activo': tallesSeleccionados[product.id] === talle }]"
                  >
                    {{ talle }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Cantidad y agregar al carrito -->
            <div class="cantidad-container">
              <button class="btn-cantidad" @click="decrementar(product.id)">-</button>
              <span class="cantidad">{{ cantidades[product.id] || 0 }}</span>
              <button class="btn-cantidad" @click="incrementar(product.id)">+</button>
              <button 
                class="btn-comprar" 
                @click="agregarAlCarrito(product.id)"
                :disabled="!puedeAgregarAlCarrito(product)"
              >
                Agregar al carrito
              </button>
            </div>
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
    })
  },
  methods: {
    puedeAgregarAlCarrito(product) {
      // Verificar si se requiere selección de color/talle y si están seleccionados
      const tieneColores = product.colores_disponibles && product.colores_disponibles.length > 0;
      const tieneTalles = product.talles_disponibles && product.talles_disponibles.length > 0;
      
      if (tieneColores && !this.coloresSeleccionados[product.id]) {
        return false;
      }
      if (tieneTalles && !this.tallesSeleccionados[product.id]) {
        return false;
      }
      return true;
    }
  },
  props: {
    coloresSeleccionados: Object,
    tallesSeleccionados: Object,
    cantidades: Object,
    seleccionarColor: Function,
    seleccionarTalle: Function,
    incrementar: Function,
    decrementar: Function,
    agregarAlCarrito: Function
  }
}
</script>