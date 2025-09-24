<template>
<!-- HEADER -->

    <header class="custom-header d-flex justify-content-between align-items-center">
      
      <button class="btn btn-icon" @click="$emit('toggle-sidebar')">
        <i class="bi bi-list"></i>
      </button>

      <h1 class="logo-text">LucyBell</h1>

      <button class="btn btn-icon" @click="$emit('toggle-carrito')">
        <i class="bi bi-cart"></i>
      </button>

    </header>

</template>

<script>
export default {
    name: 'HeaderComponent'
}
</script>