<template>
<!-- SIDEBAR del carrito -->

  <div :class="['sidebar shadow derecha', { 'active': carritoOpen }]">
    <div class="p-3">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="sidebar-title">Carrito</h4>
        <button class="btn btn-icon" @click="$emit('close-carrito')">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>

      <div v-if="carrito.length === 0">
        <p>El carrito está vacío 😢</p>
      </div>

      <div v-else>
        <div v-for="(item, index) in carrito" :key="index" class="mb-3 p-2 border rounded">
          <p><strong>Producto:</strong> {{ item.productoId }}</p>
          <p><strong>Cantidad:</strong> {{ item.cantidad }}</p>
          <p><strong>Color:</strong> {{ item.color }}</p>
          <p><strong>Talle:</strong> {{ item.talle }}</p>
        </div>

        <button class="btn-comprar w-100 mt-3" @click="$emit('finalizar-compra')">
          Finalizar Compra
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CarritoSidebar",
  props: {
    carritoOpen: Boolean,
    carrito: Array
  }
}
</script>
