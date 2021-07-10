<template>
  <form v-on:submit.prevent="doLogin">
    <input
      type="text"
      name="username"
      placeholder="Username"
      autocomplete="username"
      class="form-group-input mb-2"
      v-model="v$.credentials.username.$model"
      :class="{'input-error': v$.credentials.username.$error}"
    >
    <input
      type="password"
      name="password"
      placeholder="Password"
      autocomplete="current-password"
      class="form-group-input mb-2"
      v-model="v$.credentials.password.$model"
      :class="{'input-error': v$.credentials.password.$error}"
    >

    <v-btn color="info" class="mt-1">Log in</v-btn>

    <span v-if="authError" class="text-danger ml-3">
      {{ loginErrorMessage }}
    </span>
  </form>
</template>

<script>
import useVuelidate from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import { mapActions, mapGetters } from 'vuex'

export default {
  setup () {
    return { v$: useVuelidate() }
  },
  data() {
    return {
      loginErrorMessage: "Login failed! Maybe your name is Gary?",
      credentials: {
        username: null,
        password: null,
      }
    }
  },
  validations() {
    return {
      credentials: {
        username: { required },
        password: { required }
      }
    }
  },
  computed: {
    ...mapGetters('auth', ['authError'])
  },
  methods: {
    ...mapActions('auth', ['login']),
    async doLogin() {
      const isFormCorrect = await this.v$.$validate()
      if (!isFormCorrect) return

      this.login(this.credentials)
    }
  }
}
</script>