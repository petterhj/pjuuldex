<template>
  <modal modal-id="modal-card" class="p-0">
    <div v-if="card">
      <div class="mb-3">
        <Card :card="card" :compact="true" />
      </div>
      <div class="mb-2">
        <h6>Inventory</h6>
        <div 
          class="mb-2 p-2 bg-gray-100"
          v-for="variant in card.variants"
          :key="variant.id"
        >
          <div style="overflow: auto">
            <b class="title">{{ variant.name }}</b>
            <a href="#" class="uppercase u-pull-right">Add</a>
          </div>
          <div class="inventory-card" v-for="(card, i) in variant.inventory" :key="i">
            <div style="flex: 0 1 auto;" class="text-gray-400">
              <v-tag color="info">{{ (i + 1) }}</v-tag>
            </div> 
            <div style="flex: 0 1 auto;" class="">
              <star-rating
                style="padding-top: 10px;"
                :rating="getGarding(card.grade)"
                :max-rating="4"
                :star-size="16"
                :rounded-corners="true"
                :padding="6"
                :show-rating="false"
              />
            </div> 
            <div style="flex: 1 1 auto;">{{ card.grade }}</div> 
            <div style="flex: 0 1 auto;">{{ card.bought_date }}</div> 
            <div style="flex: 0 1 auto;" class="p-0">
              <button class="btn-xsmall btn-success outline m-0 u-pull-right" style="visibility: hidden;">
                Save
              </button>
            </div> 
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import StarRating from 'vue-star-rating'
import Modal from './Modal.vue';
import Card from './Card.vue';

export default {
  components: { StarRating, Modal, Card },
  props: {
    card: {
      type: Object
    }
  },
  methods: {
    getImageUrl(path) {
      return import.meta.env.VITE_API_BASE_URL + path
    },
    getGarding(grade) {
      switch(grade) {
        case 'Excellent':
          return 4;
        case 'Good':
          return 3;
        case 'OK':
          return 2;
        case 'Poor':
          return 1;
        default:
          return 0
      }
    }
  },
  mounted() {
    console.log(this.card)
  }
}
</script>

<style scoped>
.inventory-card {
  display: flex;
  align-content: center;
}
.inventory-card > div {
  align-self: center;
  padding-right: 1rem;
}
img {
  width: 1rem;
  /* height: 33px; */
  height: 1rem;
  display: block;
  border-radius: 50%;
}
</style>
