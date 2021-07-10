<template>
  <modal modal-id="modal-card" class="p-0" @closed="$emit('closed', card)">
    <template v-if="card">
      <div class="mb-3">
        <Card :card="card" :compact="true" />
      </div>
      <div class="mb-2">
        <h5>
          <template v-if="isAuthenticated">
            Inventory <span class="text-gray-600">({{ card.inventory_count }})
            </span>
          </template>
          <template v-else>
            Variants
          </template>
        </h5>
        
        <inventory-variant
          v-for="variant in card.variants"
          :key="variant.id"
          :variant="variant"
        />

        <h5 class="mt-4">Prices</h5>
        <div class="prices bg-gray-200 m-2 p-2">
          <span class="text-gray-600">Not implemented yet... :/</span>
        </div>
      </div>
    </template>
  </modal>
</template>

<script>
import { mapGetters } from 'vuex'
import Modal from './Modal.vue';
import Card from './Card.vue';
import InventoryVariant from './InventoryVariant.vue';

export default {
  components: { Modal, Card, InventoryVariant },
  props: {
    card: {
      type: Object
    }
  },
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
  }
}
</script>

<style scoped>
img {
  width: 1rem;
  height: 1rem;
  display: block;
  border-radius: 50%;
}
.prices {
  border-radius: 4px;
}
</style>
