<template>
  <div>
    <v-navbar :dark="true" class="mb-0">
      <template v-slot:brandTitle>pjuuldex</template>
      <v-nav-region position="left" class="ml-3">
        <v-nav-dropdown animated>
          <template v-slot:title>Sets</template>
            <v-navbar-item
              v-for="set in sets"
              :key="set.id"
              @click="loadSet(set.slug)"
            >
              {{ set.name }}
            </v-navbar-item>
        </v-nav-dropdown>
      </v-nav-region>

      <v-nav-region position="right">
        <v-navbar-item>Admin</v-navbar-item>
      </v-nav-region>
    </v-navbar>
    <section>
      <router-view />
    </section>
  </div>
</template>

<script>
import http from "./http";

export default {
  components: { },
  data() {
    return {
      sets: [],
      cards: [],
    }
  },
  watch: {
    '$route'(to) {
      const bodyEl = document.body;
      const hash = to.hash.split("#")[1];
      if (hash && hash.split("-")[0] === "modal") {
        bodyEl.classList.add("has-overlay")
      } else {
        bodyEl.classList.remove("has-overlay")
      }
    },
  },
  methods: {
    loadSet(set_slug) {
      console.log(`Loading set: ${set_slug}`)
      this.$router.push({
        name: 'set',
        params: { slug: set_slug }
      })
    }
  },
  mounted() {
    http.get('/sets')
      .then((response) => {
        this.sets = response.data
      }, (error) => {
        this.$router.replace({ name: 'error', params: {
          status: error.response.status,
          message: error.response.data.detail
        }})
      }
    )
  }
}
</script>

<style>
body.has-overlay {
  overflow: hidden;
}
</style>
