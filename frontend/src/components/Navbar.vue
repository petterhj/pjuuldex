<template>
  <v-navbar
    class="mb-0"
    :dark="true"
    :disableMobileNavbar="true"
  >
    <template v-slot:brandTitle>
      <router-link :to="{ name: 'home' }">pjuuldex</router-link>
    </template>
    <v-nav-region position="left" class="ml-3">
      <v-nav-dropdown animated v-if="sets && sets.length > 0">
        <template v-slot:title>Sets</template>
          <v-navbar-item
            v-for="set in sets"
            :key="set.id"
            @click="loadSet(set.slug)"
          >
            <div class="icon">
              <img :src="set.symbol" alt="symbol" v-if="set.symbol">
            </div>
            <div class="label">{{ set.name }}</div>
          </v-navbar-item>
      </v-nav-dropdown>
    </v-nav-region>

    <v-nav-region position="right" v-if="isAuthenticated">
      <v-navbar-item @click="logout">
        <i class="zmdi zmdi-lock"></i>
      </v-navbar-item>
    </v-nav-region>
  </v-navbar>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters('main', ['sets',]),
    ...mapGetters('auth', ['isAuthenticated']),
  },
  methods: {
    ...mapActions('auth', ['logout']),
    loadSet(set_slug) {
      this.$router.push({
        name: 'set',
        params: { slug: set_slug }
      })
    },
  }
}
</script>

<style scoped>
.nav-item {
  justify-content: left;
  display: flex;
}
.nav-item div.icon,
.nav-item div.label {
  flex: 0 1 auto;
  align-self: center;
}
.nav-item div.icon { padding-right: 10px; }
.nav-item div.icon > img {
  height: 1rem;
  display: block;
}
.nav-item i.zmdi { font-size: 1.5rem; }
</style>