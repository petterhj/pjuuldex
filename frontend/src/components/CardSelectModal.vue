<template>
  <modal modal-id="modal-card-select" title="Select card">
    <div class="grid grid-cols-6 grid-gap-0" v-if="set">
      <a 
        v-for="i in set.card_count"
        :key="i"
        class="card-tile"
        :href="'#card'+i"
      >{{ i }}</a>
    </div>
  </modal>
</template>

<script>
import Modal from './Modal.vue';

export default {
  components: { Modal },
  props: {
    set: {
      type: Object
    }
  }
}
</script>

<style scoped>
.grid {
  height: 100%;
}
a.card-tile { 
  text-align: center;
}
</style>
