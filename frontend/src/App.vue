<template>
  <div class="layout">
    <navbar />

    <section>
      <router-view />
    </section>

    <footer>
      <img src="/assets/images/table.png">
    </footer>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import Navbar from './components/Navbar.vue'

export default {
  components: { Navbar },
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
    ...mapActions('main', ['getSets']),
    ...mapActions('auth', ['getUser'])
  },
  created() {
    this.getSets()
    this.getUser()
  },
}
</script>

<style>
body, #app, .layout {
  height: 100%;
}
body.has-overlay {
  overflow: hidden;
}

.layout {
  display: flex;
  flex-direction: column;
}
.layout > .header,
.layout > footer { flex: 0 1 auto; }
.layout > section { flex: 1 1 auto; }

footer {
  position: relative;
  min-height: 85px;
  width: 100%;
  background: pink;
  background-image: url("/assets/images/border.png");
  z-index: -1;
  opacity: 0.25;
}
footer > img {
   position: absolute;
   bottom: 0;
   right: 5vh;
}
</style>
