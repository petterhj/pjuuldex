<template>
  <div>
    <div class="hero bg-dark">
      <div class="hero-body py-1 pl-1">
        <template v-if="!isAuthenticated">
          <img src="/assets/images/oak.png" class="mr-1" />
        </template>
        <template v-if="isAuthenticated">
          <img src="/assets/images/charmander.png" class="mr-1" />
        </template>
        <div class="content m-0" v-if="!isAuthenticated">
          <h4 class="title white">Welcome!</h4>
          <h6 class="subtitle text-gray-300">What is your name again?</h6>
        </div>
        <div class="content m-0" v-else>
          <h4 class="title white">Dashboard</h4>
          <h6 class="subtitle text-gray-300" v-if="currentUser">
            {{ currentUser }}
          </h6>
        </div>
      </div>
    </div>

    <section class="m-6" v-if="!isAuthenticated">
      <h5>Log in</h5>
      <login-form />
    </section>

    <section class="m-6" v-else>
      <section class="mb-6">
        <h6>Sets</h6>
        <table class="set-table table small borderless">
          <tbody>
            <tr v-for="set in sets" :key="set.id">
              <td>
                <img class="set-image" :src="set.symbol" alt="card">
              </td>
              <td>
                <router-link :to="{name: 'set', params: {slug: set.slug}}">
                  {{ set.name }}
                </router-link>
              </td>
              <td>
                <div class="progress-bar">
                  <div
                    :style="'width: '+getSetProgressPercent(set.collected_count, set.card_count)+'%'"
                    class="progress"
                  >
                  </div>
                  <div class="label">
                    {{ set.collected_count }}/{{ set.card_count }} ({{getSetProgressPercent(set.collected_count, set.card_count)}} %)
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section>
        <h6>Recent</h6>
        <table class="recent-table table small borderless">
          <tbody>
            <tr v-for="inventory in recentInventory" :key="inventory.id">
              <td>
                <img class="card-image" :src="inventory.card.image" alt="card">
              </td>
              <td>{{ inventory.card.name }}</td>
              <td>{{ inventory.variant.name }}</td>
              <td>
                <router-link :to="{name: 'set', params: {slug: inventory.set.slug}}">
                  {{ inventory.set.name }}
                </router-link>
              </td>
              <td>{{ inventory.updated_date }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </section>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import LoginForm from '../components/LoginForm.vue'

export default {
  components: { LoginForm },
  computed: {
    ...mapGetters(
      'auth', [
        'isAuthenticated',
        'currentUser'
      ]
    ),
    ...mapGetters(
      'main', ['sets', 'recentInventory',]
    )
  },
  methods: {
    ...mapActions('main', ['getRecentInventory']),
    getSetProgressPercent(collected, total) {
      return Math.round((collected / total) * 100)
    }
  },
  mounted() {
    if (this.isAuthenticated)
      this.getRecentInventory()
  }
}
</script>

<style scoped>
.hero img {
  width: 85px;
  height: 85px;
}
.table {
  text-align: left;
  font-size: 0.9rem;
}
.table td { vertical-align: middle; }
.table tr td:first-child {
  width: 50px;
  text-align: center;
}
.table tr td:nth-child(2) { width: 200px; }
.table img.set-image {
  max-height: 25px;
  max-width: 25px;  
}
.table img.card-image {
  max-height: 40px;
  max-width: 55px;
  border: 1px solid #999;
  border-radius: 2px;
  background-color: #CCC;
}

.progress-bar {
  margin-top: 5px;
  position: relative;
  height: 1.25rem;
  background: #363636;
  border-radius: 6px;
}
.progress-bar > div.progress {
  height: inherit;
  background: #0dd157;
  border-radius: inherit;
}
.progress-bar > div.label {
  position: absolute;
  top: 0;
  left: 0.5rem;
  color: white;
  font-size: 0.7rem;
}
</style>