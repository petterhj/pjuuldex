<template>
  <div>
    <div class="hero bg-link-dark" v-if="set">
      <div class="hero-body py-1 pl-3">
        <div class="symbol mr-3">
          <img :src="set.symbol" v-if="set.symbol" />
        </div>
        <div class="content m-0">
          <h4 class="title white">{{ set.name }}</h4>
          <h6 class="subtitle text-gray-300">{{ set.card_count }} cards</h6>
        </div>
      </div>
    </div>

    <section class="m-0 py-2" v-if="set && set.cards.length > 0">
      <div
        class="m-2 mb-3 p-2 card"
        v-for="card in filteredCards"
        :key="card.id"
        :class="{dim: card.inventory_count === 0}"
        :id="'card'+card.number"
        @click="selectCard(card)"
      >
        <card :card="card" />
      </div>
    </section>

    <card-modal
      :card="activeCard"
      @closed="modalClosed" />

    <card-select-modal />

    <fab
      v-if="set && set.cards.length > 0"
      @click="openModal('modal-card-select')"
    >
      <i class="zmdi zmdi-dialpad"></i>
    </fab>
    
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
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
      hideCollected: false,
      activeCard: null,
    }
  },
  computed: {
    ...mapGetters('main', ['set',]),
    filteredCards() {
      return this.set.cards.filter(card => {
        if (this.hideCollected)
          return card.inventory_count === 0
        return true
      })
    }
  },
  methods: {
    ...mapActions('main', ['getSet']),
    selectCard(card) {
      this.activeCard = card
      this.openModal('modal-card')
    },
    openModal(target){
      window.location.hash = target;
    },
    modalClosed(card) {
      if (card)
        card.variants.sort((a, b) => b.inventory_count - a.inventory_count)
      this.activeCard = null
    },
  },
  watch: {
    '$route.params.slug'(slug) {
      if (slug)
        this.getSet(slug)
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
.hero div.symbol {
  width: 40px;
  height: 40px;
}
.hero div.symbol > img {
  width: inherit;
  height: inherit;
}

.card { opacity: 0.9; }
.card:hover { opacity: 1; cursor: pointer; }
.card.dim { opacity: 0.3; }
.card.dim:hover { opacity: 0.5; }
</style>
