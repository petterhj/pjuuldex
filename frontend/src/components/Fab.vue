<template>
  <v-btn 
    class="fab"
    style="padding: 2px 5px"
    :circle="true"
    :color="color"
  > 
    <slot></slot>
  </v-btn>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      default: 'primary'
    }
  }
}
</script>

<style scoped>
button.fab {
  position: fixed; bottom: 1rem; right: 1rem;
  padding: 0;
  width: 42px;
  height: 42px;
  min-width: auto;
  box-shadow: 0 5px 12px 0 rgb(42 51 83 / 12%), 0 0 5px rgb(0 0 0 / 6%);
  opacity: 0.8;
  font-size: 1.5rem;
}
button.fab:hover {
  opacity: 1;
}
</style>
