<template>
  <div
    v-if="card"
    style="display: flex;"
    :class="{compact: compact}"
  >
    <div class="" style="flex: 0 1 auto; align-self: stretch;">
      <img :src="card.image" alt="avatar" v-if="card.image">
    </div>
    <div class="pt-1 pr-1 pl-2"  style="flex: 1 1 auto; align-self: stretch;">
      <div style="display: flex; flex-direction: column; height: 100%;">
        <div style="flex: 0 1 auto; align-self: stretch;">
          <div style="display: flex">
            <v-tag color="black" size="" class="u-pull-left mr-1" style="align-self: center;">
              <b>{{ card.number }}</b>/{{ set.card_count }}
            </v-tag>
            <h5 class="m-0 mr-1 u-pull-left" style="align-self: center;">{{ card.name }}</h5>
            <h6 class="m-0 font-alt font-light text-gray-400" style="align-self: center;" v-if="card.hp">({{ card.hp }} HP)</h6>
          </div>
        </div>
        <div class="pt-1" style="flex: 0 1 auto; align-self: stretch;">
          <v-tag-container style="flex: 0 1 auto; align-self: stretch;">
            <v-tag class="m-0 mr-1" v-if="card.supertype">{{ card.supertype }}</v-tag>
            <v-tag class="m-0 mr-1" v-if="card.subtype">{{ card.subtype }}</v-tag>
            <v-tag class="m-0 mr-1" v-if="card.type">{{ card.type }}</v-tag>
            <v-tag class="m-0 mr-1" v-if="card.rarity">{{ card.rarity }}</v-tag>
            <v-tag class="m-0 mr-1" v-if="compact">{{ card.set.name }}</v-tag>
          </v-tag-container>
        </div>
        <div style="flex: 1 1 auto; align-self: stretch;" v-if="!compact">
          <small style="font-size: 0.6rem" class="text-gray-600">
            <i>Illu. {{ card.illustrator }}</i>
          </small>
        </div>
        <div style="flex: 0 1 auto; align-self: stretch;" v-if="!compact">
          <v-tag-container
            v-for="variant in card.variants"
            :key="variant.id"
            :grouped="true"
            class="u-pull-left m-0 mr-1 mb-1"
            :class="{dim: variant.inventory_count && variant.inventory_count === 0}"
          >
            <v-tag
              class="m-0"
              v-if="variant.inventory_count"
              :color="variant.inventory_count > 0 ? 'success' : 'danger'"
            >
              <i class="zmdi zmdi-check"></i>
            </v-tag>
            <v-tag class="m-0">{{ variant.name }}</v-tag>
          </v-tag-container>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    card: {
      type: Object,
      required: true
    },
    compact: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters('main', ['set',]),
  }
}
</script>

<style scoped>
img {
  display: block;
  min-width: 123px;
  height: 171px;
  border: 1px solid #999;
  border-radius: 2px;
  background-color: #CCC;
}
.compact img {
  min-width: 55px;
  height: 76px;
}
</style>
