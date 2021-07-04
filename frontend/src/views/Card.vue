<template>
  <div>
    <span class="is-size-3">Add feed</span>
    <FeedForm @submit="addFeed" />
  </div>
</template>

<script>
import http from "../http";
import FeedForm from "../forms/Feed.vue";

export default {
  components: { FeedForm },
  methods: {
    addFeed(feed) {
      http.post('/feeds/', feed)
        .then((response) => {
          this.$router.push({
            name: 'feed',
            params: { slug: response.data.slug }
          })
        }, (error) => {
          console.log(error);
        }
      )
    }
  }
}
</script>
