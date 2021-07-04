<template>
  <nav class="navbar is-dark p-2 px-5" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link class="navbar-item" :to="{ name: 'home' }">
        <img src="../assets/icon_16.png"> casterr
      </router-link>
      
      <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false"
        data-target="navbarBasicExample">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbarBasicExample" class="navbar-menu">
      <div class="navbar-start">
        <router-link class="navbar-item" :to="{ name: 'feeds' }">
          Feeds
        </router-link>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-light is-outlined" href="/admin" title="Admin">
              <span class="mdi mdi-database-lock-outline"></span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>

</script>

<style scoped>
.navbar-brand img {
  height: 28px;
  margin-right: 1rem;
}
</style>