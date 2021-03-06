import http from '../http';

export default {
  namespaced: true,
  state: {
    loadingState: false,
    sets: [],
    currentSet: null,
    recentInventory: [],
  },
  getters: {
    loadingState: state => state.loadingState,
    sets: state => state.sets,
    set: state => state.currentSet,
    recentInventory: state => state.recentInventory,
  },
  mutations: {
    setLoadingState(state, isLoading) {
      state.loadingState = isLoading
    },
    setSets(state, sets) {
      state.sets = sets
    },
    setSet(state, set) {
      if (set && set.inventory_count) {
        console.log("Sorting variants by inventory")
        for (let card of set.cards) {
          card.variants.sort((a, b) => {
            return b.inventory_count - a.inventory_count
          })
        }
      }
      state.currentSet = set
    },
    updateInventory(state, inventory) {
      if (!inventory)
        return

      // Update inventory data
      for (let set of state.sets) {
        if (set.id == inventory.set.id) {
          set.collected_count = inventory.set.collected_count
          set.inventory_count = inventory.set.inventory_count
        }
      }
      if (state.currentSet.id == inventory.set.id) {
        state.currentSet.collected_count = inventory.set.collected_count
        state.currentSet.inventory_count = inventory.set.inventory_count
      }
        
      for (let card of state.currentSet.cards) {
        if (card.id == inventory.card.id) {
          card.inventory_count = inventory.card.inventory_count

          for (let variant of card.variants) {
            if (variant.id == inventory.variant.id) {
              variant.inventory_count = inventory.variant.inventory_count
            }
          }
        }
      }
    },
    setRecentInventory(state, inventory) {
      state.recentInventory = inventory
    },
  },
  actions: {
    getSets({ commit }) {
      console.log('Fetching sets...')
      commit('setLoadingState', true)
      return http.get('sets/')
        .then((response) => {
          commit('setSets', response.data)
        })
        .catch((error) => {
          commit('setSets', [])
        })
        .finally(() => commit('setLoadingState', false));
    },
    getSet({ commit }, set_slug) {
      console.log(`Fetching set ${set_slug}...`)
      commit('setLoadingState', true)
      commit('setSet', null)
      return http.get(`sets/${set_slug}/`)
        .then((response) => {
          commit('setSet', response.data)
        })
        .catch((error) => {
          console.error("Could not fetch set")
        })
        .finally(() => commit('setLoadingState', false))
    },

    addInventory({ commit }, variant_id) {
      return http.post(`user/inventory/variant/${variant_id}/`)
        .then((response) => {
          commit('updateInventory', response.data)
        })
        .catch((error) => {
          console.log(error)
        });
    },
    subInventory({ commit }, variant_id) {
      return http.delete(`user/inventory/variant/${variant_id}/`)
        .then((response) => {
          commit('updateInventory', response.data)
        })
        .catch((error) => {
          console.log(error)
        });
    },
    getRecentInventory({ commit }) {
      console.log("Fetching recent inventory...")
      
      return http.get('user/inventory/recent/')
        .then((response) => {
          // console.log("--------------")
          // console.log(response)
          commit('setRecentInventory', response.data)
        })
        .catch((error) => {
          console.log(error)
          commit('setRecentInventory', [])
          return Promise.reject(error);
        });
    },
  }
}
