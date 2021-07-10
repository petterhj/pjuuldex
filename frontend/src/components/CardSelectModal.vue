<template>
  <modal modal-id="modal-card-select" title="Select card">
    <div class="grid grid-cols-6 grid-gap-0" v-if="set">
      <a 
        v-for="card in set.cards"
        :key="card.id"
        class="card-tile"
        :href="'#card'+card.number"
      >{{ card.number }}</a>
    </div>
  </modal>
</template>

<script>
import { mapGetters } from 'vuex'
import Modal from './Modal.vue';

export default {
  components: { Modal },
  computed: {
    ...mapGetters('main', ['set',]),
  },
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
