<template>
  <div>
    <span class="is-size-3">{{ status }}: {{ message }}</span>
    <hr>
    {{$router}}
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
