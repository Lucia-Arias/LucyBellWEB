<template>
  <!-- CATALOGO CONTENIDO -->
  <main class="p-3">
    <h2 class="section-title">Catálogo</h2>

    <div v-if="products.length === 0" class="text-center">
      <p>Cargando productos...</p>
    </div>

    <div class="row" v-else>
      <div class="col-md-4 mb-4" v-for="product in products" :key="product.id">
        <div class="card-producto shadow-sm">
          <div class="producto-contenido">
            <!-- Imagen y etiqueta con carrusel -->
            <div class="producto-imagen-wrapper">
                
              <span class="producto-etiqueta">{{product.category_name}} de {{ product.material_name }}</span>
              
              <!-- Carrusel para múltiples imágenes -->
              <div v-if="hasMultipleImages(product)" class="image-carousel">
                <img
                  :src="getImageUrl(getCurrentImage(product))"
                  :alt="getAltText(product, getCurrentImageIndex(product.id))"
                  class="img-fluid rounded carousel-image"
                  @error="handleImageError(product.id)"
                />
                
                <!-- Flechas de navegación -->
                <button class="carousel-arrow prev" @click.stop="imagenAnterior(product.id)">
                  ‹
                </button>
                <button class="carousel-arrow next" @click.stop="siguienteImagen(product.id)">
                  ›
                </button>
                
                <!-- Indicadores -->
                <div class="carousel-indicators">
                  <span 
                    v-for="(img, index) in product.images" 
                    :key="index"
                    :class="['carousel-dot', { 'active': getCurrentImageIndex(product.id) === index }]"
                    @click.stop="cambiarImagen(product.id, index)"
                  ></span>
                </div>
                
                <!-- Contador -->
                <div class="image-counter">
                  {{ getCurrentImageIndex(product.id) + 1 }}/{{ product.images.length }}
                </div>
              </div>
              
              <!-- Imagen única -->
              <div v-else-if="hasSingleImage(product)">
                <img
                  :src="getImageUrl(getFirstImage(product))"
                  :alt="getAltText(product, 0)"
                  class="img-fluid rounded"
                  @error="handleImageError(product.id)"
                />
              </div>
              
              <!-- Sin imágenes -->
              <div v-else class="no-image-placeholder">
                <span>Sin imagen</span>
              </div>
              
            </div>
            
            <!-- Nombre y precio -->
            <h5 class="producto-nombre">{{ product.name }}</h5>
            <p class="producto-precio">${{ product.price }}</p>
            <div class="selectores-container">
              <!-- Selección de color - Solo muestra si el producto tiene colores disponibles -->
              <div class="seleccion-container" v-if="product.colores_disponibles && product.colores_disponibles.length > 0">
                <p class="seleccion-label">Color:</p>
                <div class="seleccion-opciones">
                  <button
                    v-for="(colorObj, index) in product.colores_disponibles"
                    :key="index"
                    @click="seleccionarColor(product.id, colorObj.color)"
                    :class="['seleccion-btn', { 'activo': coloresSeleccionados[product.id] === colorObj.color }]"
                    :title="`Stock: ${colorObj.stock}`"
                  >
                    {{ colorObj.color }}
                  </button>
                </div>
              </div>

              <!-- Selección de talle - Solo muestra si el producto tiene talles disponibles -->
              <div class="seleccion-container" v-if="product.talles_disponibles && product.talles_disponibles.length > 0">
                <p class="seleccion-label">Talle:</p>
                <div class="seleccion-opciones">
                  <button
                    v-for="(talleObj, index) in product.talles_disponibles"
                    :key="index"
                    @click="seleccionarTalle(product.id, talleObj.talle)"
                    :class="['seleccion-btn', { 'activo': tallesSeleccionados[product.id] === talleObj.talle }]"
                    :title="`Stock: ${talleObj.stock}`"
                  >
                    {{ talleObj.talle }}
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

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  coloresSeleccionados: Object,
  tallesSeleccionados: Object,
  cantidades: Object,
  seleccionarColor: Function,
  seleccionarTalle: Function,
  incrementar: Function,
  decrementar: Function,
  agregarAlCarrito: Function
})

// Reactive data
const products = ref([])
const imagenIndex = ref({})

// Methods
const getImageUrl = (url) => {
  if (!url) return null
  
  // Si la URL ya es absoluta (http:// o https://), úsala directamente
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  
  // Si la URL es relativa, prepéndele la base del backend
  const baseUrl = 'http://127.0.0.1:8000'
  if (url.startsWith('/')) {
    return `${baseUrl}${url}`
  }
  
  // Si no empieza con /, asumimos que es relativa a la raíz
  return `${baseUrl}/${url}`
}

const hasMultipleImages = (product) => {
  return product.images && Array.isArray(product.images) && product.images.length > 1
}

const hasSingleImage = (product) => {
  return product.images && Array.isArray(product.images) && product.images.length === 1
}

const getFirstImage = (product) => {
  if (product.images && Array.isArray(product.images) && product.images.length > 0) {
    return product.images[0].image
  }
  return null
}

const getCurrentImageIndex = (productId) => {
  return imagenIndex.value[productId] || 0
}

const getCurrentImage = (product) => {
  const currentIndex = getCurrentImageIndex(product.id)
  if (product.images && Array.isArray(product.images) && product.images[currentIndex]) {
    return product.images[currentIndex].image
  }
  return null
}

const getTotalImages = (product) => {
  if (product.images && Array.isArray(product.images)) {
    return product.images.length
  }
  return 0
}

const handleImageError = (productId) => {
  console.error(`Error cargando imagen para producto ${productId}`)
}

// Función auxiliar para obtener el stock disponible según las selecciones
const getStockDisponible = (product) => {
  const colorSeleccionado = props.coloresSeleccionados[product.id]
  const talleSeleccionado = props.tallesSeleccionados[product.id]
  
  // Si no hay selecciones, retornar stock total
  if (!colorSeleccionado && !talleSeleccionado) {
    return product.stock_total || 0
  }
  
  // Buscar combinación específica
  if (colorSeleccionado && talleSeleccionado) {
    // Aquí deberías tener lógica para buscar la combinación exacta
    // Esto depende de cómo esté estructurado tu backend
    return Math.min(
      getStockPorColor(product, colorSeleccionado),
      getStockPorTalle(product, talleSeleccionado)
    )
  }
  
  if (colorSeleccionado) {
    return getStockPorColor(product, colorSeleccionado)
  }
  
  if (talleSeleccionado) {
    return getStockPorTalle(product, talleSeleccionado)
  }
  
  return 0
}

const getStockPorColor = (product, color) => {
  const colorObj = product.colores_disponibles.find(c => c.color === color)
  return colorObj ? colorObj.stock : 0
}

const getStockPorTalle = (product, talle) => {
  const talleObj = product.talles_disponibles.find(t => t.talle === talle)
  return talleObj ? talleObj.stock : 0
}

const puedeAgregarAlCarrito = (product) => {
  const tieneColores = product.colores_disponibles && product.colores_disponibles.length > 0
  const tieneTalles = product.talles_disponibles && product.talles_disponibles.length > 0
  
  if (tieneColores && !props.coloresSeleccionados[product.id]) {
    return false
  }
  if (tieneTalles && !props.tallesSeleccionados[product.id]) {
    return false
  }
  
  // Verificar stock
  const stockDisponible = getStockDisponible(product)
  const cantidadActual = props.cantidades[product.id] || 0
  
  return stockDisponible > 0 && cantidadActual > 0 && cantidadActual <= stockDisponible
}

const siguienteImagen = (productId) => {
  const product = products.value.find(p => p.id === productId)
  if (!product) return
  
  const totalImages = getTotalImages(product)
  const currentIndex = getCurrentImageIndex(productId)
  const nextIndex = (currentIndex + 1) % totalImages
  cambiarImagen(productId, nextIndex)
}

const imagenAnterior = (productId) => {
  const product = products.value.find(p => p.id === productId)
  if (!product) return
  
  const totalImages = getTotalImages(product)
  const currentIndex = getCurrentImageIndex(productId)
  const prevIndex = (currentIndex - 1 + totalImages) % totalImages
  cambiarImagen(productId, prevIndex)
}

const cambiarImagen = (productId, index) => {
  imagenIndex.value[productId] = index
  // Forzar reactividad
  imagenIndex.value = { ...imagenIndex.value }
}

const getAltText = (product, index) => {
  if (product.images && Array.isArray(product.images) && product.images[index]) {
    return product.images[index].alt_text || `Imagen de ${product.name}`
  }
  return `Imagen de ${product.name}`
}

// Lifecycle
onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/products/')
    console.log('Datos recibidos:', response.data)
    products.value = response.data
    
    // Debug detallado de las imágenes
    products.value.forEach(product => {
      console.log(`Producto ${product.id} - ${product.name}:`, {
        images: product.images,
        totalImages: product.images ? product.images.length : 0,
        colores_disponibles: product.colores_disponibles,
        talles_disponibles: product.talles_disponibles,
        imagesDetail: product.images ? product.images.map((img, idx) => ({
          index: idx,
          image: img.image,
          alt_text: img.alt_text,
          order: img.order
        })) : []
      })
      
      // Inicializar índice de imagen para cada producto
      if (product.images && product.images.length > 0) {
        imagenIndex.value[product.id] = 0
      }
    })
  } catch (error) {
    console.error('Error cargando productos:', error)
  }
})
</script>