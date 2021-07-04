<template>
  <div class="pd-modal p-2" :id="modalId">
    <a href="#close" class="modal-close-btn" aria-label="Close">
      <span class="icon">
        <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="times" class="svg-inline--fa fa-times fa-w-11 fa-wrapper" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 352 512">
          <path fill="currentColor" d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z"></path>
        </svg>
      </span>
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
  mounted() {
    document.addEventListener('keyup', function(e) {
      if(e.key === "Escape") {
          const modals = document.querySelectorAll('.modal-close-btn');
          for (const modal of modals) {
              modal.click();
          }
        }
    });   
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
  top: 1rem;
  right: 1rem;
  font-size: 0.6rem;
  padding: 0;
}
.modal-close-btn .icon { width: 1rem; }

.modal-body {
  flex: 1 1 auto;
  overflow-y: auto;
}
</style>
