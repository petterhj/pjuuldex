<template>
  <section class="mt-5">
    <div class="field">
      <label class="label">Feed URL</label>
      <div class="control">
        <input type="text" class="input is-large" 
          :class="{ 'is-danger': v$.form.feed_url.$errors.length }"
          placeholder="Feed URL"
          v-model="v$.form.feed_url.$model"
        >
        <div class="input-errors is-size-7 mt-3" 
          v-for="error of v$.form.feed_url.$errors"
          :key="error.$uid"
        >
          <span class="has-text-danger">{{ error.$message }}</span>
        </div>
      </div>
    </div>

    <div class="field">
      <label class="label">Path</label>
      <div class="control">
        <div class="select is-large">
          <select v-model="form.path">
            <option></option>
            <option
              v-for="path in paths"
              :key="path.name"
            >
              {{ path.name }}
            </option>
          </select>
          <div class="input-errors is-size-7 mt-3" 
            v-for="error of v$.form.path.$errors"
            :key="error.$uid"
          >
            <span class="has-text-danger">{{ error.$message }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="field is-grouped pt-6">
      <div class="control">
        <button 
          class="button is-link is-large"
          @click="submit">
          Save
        </button>
      </div>
    </div>
  </section>
</template>

<script>
import http from "../http";
import useVuelidate from '@vuelidate/core'
import { required, requiredIf, url } from '@vuelidate/validators'

export default {
  name: 'FeedForm',
  props: {
    feed: {
      type: Object,
      required: false
    },
  },
  setup () {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      paths: [],
      form: {
        feed_url: this.feed?.feed_url || "",
        path: this.feed?.path || ""
      }
    }
  },
  validations() {
    return {
      form: {
        feed_url: { required, url },
        path: {}
      }
    }
  },
  methods: {
    async submit() {
      const isFormCorrect = await this.v$.$validate()
      if (!isFormCorrect) return
      this.$emit("submit", this.form)
    }
  },
  mounted() {
    http.get("/system/paths/")
      .then((response) => {
        this.paths = response.data
      }, (error) => {
        console.log(error);
      }
    )
  }
}
</script>
