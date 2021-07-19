<template>
  <div class="error-message space xlarge">
    <b>{{ status }}: {{ message }}</b>
  </div>
</template>

<script>
export default {
  props: {
    status: {
      type: String,
      required: false,
      default: "404"
    },
    message: {
      type: String,
      required: false,
      default: 'Not Found',
    },
  },
}
</script>

<style scoped>
.error-message {
  text-align: center;
}
</style>
