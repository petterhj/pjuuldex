<template>
  <div 
    class="mb-2 p-2"
    style=""
  >
    <div class="card-variant" v-if="cardVariant">
      <div class="inventory-count" v-if="isAuthenticated">
        <v-tag 
          class="m-0"
          size="large"
          :color="(cardVariant.inventory_count > 0) ? 'success' : 'gray'"
        >
          <template v-if="cardVariant.inventory_count === 1">
            <i class="zmdi zmdi-check"></i>
          </template>
          <template v-else-if="cardVariant.inventory_count === 0">
            -
          </template>
          <template v-else>
            {{ cardVariant.inventory_count }}
          </template>
        </v-tag>
      </div>
      <div class="variant-name">
        <b class="title">{{ cardVariant.name }}</b><br>
      </div>
      <div class="inventory-update" v-if="isAuthenticated">
        <v-tag-container
          :grouped="true"
        >
          <v-tag
            class="m-0"
            size="large"
            color="success"
            @click="add"
          >+</v-tag>
          <v-tag
            class="m-0"
            size="large"
            :color="cardVariant.inventory_count > 0 ? 'warning' : 'gray'"
            @click="sub"
          >-</v-tag>
        </v-tag-container>
      </div>
      <!-- <div style="variant-price" v-if="isAuthenticated">
        <v-tag
          class="m-0 ml-2"
          color="info"
          size="large"
        >
          <i class="zmdi zmdi-money-box"></i>
        </v-tag>
      </div> -->
    </div>    
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  props: {
    variant: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      cardVariant: this.variant,
    }
  },
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
  },
  methods: {
    ...mapActions('main', ['addInventory', 'subInventory']),
    add() {
      this.addInventory(this.cardVariant.id)
    },
    sub() {
      if (this.cardVariant.inventory_count == 0)
        return
      this.subInventory(this.cardVariant.id)
    }
  }
}
</script>

<style scoped>
.card-variant { display: flex; }
.card-variant > div {
  flex: 0 1 auto;
  align-self: center;
}
.variant-name { flex-grow: 1 !important; }
.inventory-count, .inventory-update { min-width: 75px; }

.tag {
  min-width: 38px;
  min-height: 38px;
}
.inventory-count .tag:hover,
.tag.tag--gray {
  cursor: default !important;
}
.inventory-update .tag:hover { cursor: pointer; }
</style>