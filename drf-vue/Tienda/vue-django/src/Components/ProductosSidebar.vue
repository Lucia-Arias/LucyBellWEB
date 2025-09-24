<template>
<!-- SIDEBAR de Productos-->
    
  <div :class="['sidebar shadow', { 'active': sidebarOpen }]">
    <div class="p-3">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="sidebar-title">Productos</h4>
        <button class="btn btn-icon" @click="$emit('close-sidebar')">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>

      <input
        type="text"
        class="form-control mb-3 search-box"
        placeholder="Buscar producto..."
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
      />

      <h6 class="filter-title">Filtrar por categoría</h6>
      <ul class="list-unstyled">
        <li><a href="#" class="sidebar-link" @click="$emit('close-sidebar')">Anillos</a></li>
        <li><a href="#" class="sidebar-link" @click="$emit('close-sidebar')">Pulseras</a></li>
        <li><a href="#" class="sidebar-link" @click="$emit('close-sidebar')">Collares</a></li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductosSidebar",
  props: {
    sidebarOpen: Boolean,
    searchQuery: String
  }
}
</script>

