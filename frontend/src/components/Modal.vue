<template>
  <div class="pd-modal p-2" :id="modalId" @keydown.esc="close" tabindex="0">
    <a class="modal-close-btn" aria-label="Close" ref="close-btn" @click="close">
      <i class="zmdi zmdi-close"></i>
    </a>

    <div class="modal-header" v-if="title">
      <h5 class="uppercase">{{ title }}</h5>
    </div>

    <div class="modal-body">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modalId: {
      type: String,
      default: 'modal',
    },
    title: {
      type: String,
    }
  },
  methods: {
    close(e) {
      this.$emit('closed')
      window.location.hash = 'close'
    }
  }
}
</script>

<style scoped>
.pd-modal {
  position: relative;
  display: none;
  height: 100%;
  background: white;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}
.pd-modal:target {
  display: flex;
  flex-direction: column;
}

.modal-close-btn {
  position: absolute;
  top: 0.5rem;
  right: 1.5rem;
  font-size: 0.6rem;
  padding: 0;
  cursor: pointer;
}
.modal-close-btn {
  font-size: 1.75rem;
}

.modal-body {
  flex: 1 1 auto;
  overflow-y: auto;
}
</style>
