<template>
  <div>
    <div class="hero bg-link-dark" v-if="set">
      <div class="hero-body py-1 px-4">
        <div class="content m-0">
          <h4 class="title white">{{ set.name }}</h4>
          <h6 class="subtitle text-gray-300">{{ set.card_count }} cards</h6>
        </div>
      </div>
    </div>

    <section class="m-0 py-2" v-if="cards">
      <div
        class="m-2 mb-3 p-2 card"
        v-for="card in cards"
        :key="card.id"
        :class="{dim: card.inventory_count === 0}"
        :id="'card'+card.number"
        @click="selectCard(card)"
      >
        <card
          :card="card"
        />
      </div>
    </section>

    <card-modal :card="activeCard" />
    <card-select-modal :set="set" />

    <fab @click="openModal('modal-card-select')">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path fill="currentColor" d="M 4 4 L 4 8 L 8 8 L 8 4 L 4 4 z M 10 4 L 10 8 L 14 8 L 14 4 L 10 4 z M 16 4 L 16 8 L 20 8 L 20 4 L 16 4 z M 4 10 L 4 14 L 8 14 L 8 10 L 4 10 z M 10 10 L 10 14 L 14 14 L 14 10 L 10 10 z M 16 10 L 16 14 L 20 14 L 20 10 L 16 10 z M 4 16 L 4 20 L 8 20 L 8 16 L 4 16 z M 10 16 L 10 20 L 14 20 L 14 16 L 10 16 z M 16 16 L 16 20 L 20 20 L 20 16 L 16 16 z"/>
      </svg>
    </fab>
    
  </div>
</template>

<script>
import http from '../http';
import Card from '../components/Card.vue';
import CardModal from '../components/CardModal.vue';
import CardSelectModal from '../components/CardSelectModal.vue';
import Fab from '../components/Fab.vue';

export default {
  components: {
    Card,
    CardModal,
    CardSelectModal,
    Fab
  },
  data() {
    return {
      set: null,
      cards: [],
      activeCard: null,
    }
  },
  methods: {
    getSet(slug) {
      console.log(`Fetching set details for ${slug}`)
      http.get(`sets/${slug}`)
        .then((response) => {
          this.set = response.data
      
          http.get(`sets/${slug}/cards`)
            .then((response) => {
              this.cards = response.data
            }, (error) => {
              
            }
          )
        }, (error) => {
          this.$router.replace({ name: 'error', params: {
            status: error.response.status,
            message: error.response.data.detail
          }})
        }
      )
    },
    selectCard(card) {
      console.log("select")
      this.activeCard = card
      console.log(this.activeCard)
    },
    openModal(target){
      window.location.hash = target;
    }
  },
  watch: {
    '$route.params.slug'(slug) {
      this.getSet(slug)
    },
    activeCard(card) {
      console.log("Card changed!")
      console.log(card)
      this.openModal('modal-card')
    }
  },
  mounted() {
    this.getSet(this.$route.params.slug)
    if (window.location.hash.split("#")[1] === "modal-card")
      window.location.hash = ""
  },
}
</script>

<style scoped>
.card { opacity: 0.9; }
.card:hover { opacity: 1; cursor: pointer; }
.card.dim { opacity: 0.3; }
.card.dim:hover { opacity: 0.5; }
</style>
