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
        <li><a href="#" class="sidebar-link" @click="$emit('close-sidebar')" v-for="category in categories" :key= "category.id">{{category.name}}</a></li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "ProductosSidebar",
  data(){
    return{
      categories:[]
    }
  },
  mounted(){
    axios.get('http://127.0.0.1:8000/api/categories/')
    .then(response => {
      this.categories = response.data
    })
    .catch(error => {
      console.log(error)
    }
    )
  },
  props: {
    sidebarOpen: Boolean,
    searchQuery: String
  }
}
</script>

