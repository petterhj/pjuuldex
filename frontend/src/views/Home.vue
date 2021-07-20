<template>
  <div>
    <div class="hero bg-dark">
      <div class="hero-body py-1 pl-1">
        <template v-if="!isAuthenticated">
          <img src="/assets/images/oak.png" class="mr-2" />
        </template>
        <template v-if="isAuthenticated">
          <img src="/assets/images/charmander.png" class="mr-2" />
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
        <div class="set-progress mb-2" v-for="set in sets" :key="set.id">
          <div>
            <img
              class="set-image" 
              :src="set.symbol"
              v-if="set.symbol"
              alt="card"
              style="max-height: 24px;"
            >
          </div>
          <div>
            <router-link :to="{name: 'set', params: {slug: set.slug}}">
              {{ set.name }}
            </router-link>
            <progress-bar
              :card-count="set.card_count || 0"
              :collected-count="set.collected_count || 0"
            />
          </div>
        </div>
      </section>

      <section>
        <h6>Recent</h6>
        <div class="recent-inventory-card mb-2" v-for="inventory in recentInventory" :key="inventory.id">
          <img class="card-image" :src="inventory.card.image" alt="card">
          <span><b>{{ inventory.card.name }}</b></span>
          <span><i>{{ inventory.variant.name }}</i></span>
          <router-link :to="{name: 'set', params: {slug: inventory.set.slug}}">
            {{ inventory.set.name }}
          </router-link>
          <span>{{ inventory.updated_date }}</span>
        </div>
      </section>
    </section>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import LoginForm from '../components/LoginForm.vue'
import ProgressBar from '../components/ProgressBar.vue'

export default {
  components: { LoginForm, ProgressBar },
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
    ...mapActions('auth', ['refreshToken']),
    // getSetProgressPercent(collected, total) {
    //   return Math.round((collected / total) * 100)
    // }
  },
  mounted() {
    if (this.isAuthenticated)
      this.getRecentInventory()
  }
}
</script>

<style scoped>
.hero img {
  width: 65px;
  height: 65px;
  margin: 10px;
}

.set-progress { display: flex; }
.set-progress > div:nth-child(1) {
  flex: 0 1 auto;
  width: 2rem;
  margin-right: 1rem;
  text-align: center;
}
.set-progress > div:nth-child(2) {
  flex: 1 1 auto;
  display: grid;
  grid-template-columns: 2fr 3fr;
}
@media screen and (max-width: 767px) {
  .set-progress > div:nth-child(2) {
    display: block;
  }
}

.recent-inventory-card {
  font-size: 0.8rem;
  display: grid;
  grid-template-columns: 60px 2fr 2fr 2fr 1fr;
}
@media screen and (max-width: 767px) {
  .recent-inventory-card {
    grid-template-columns: 60px 1fr auto;
  }
  .recent-inventory-card *:nth-child(1) {
    grid-area: 1 / 1 / span 3 / 2;
  }
  .recent-inventory-card *:nth-child(4) {
    grid-area: 2 / 2 / 3 / span 2;
  }
  .recent-inventory-card *:nth-child(5) {
    grid-area: 3 / 2 / 4 / span 2;
  }
}
.recent-inventory-card img {
  max-height: 40px;
  max-width: 55px;
  border: 1px solid #999;
  border-radius: 2px;
  background-color: #CCC;
}
</style>