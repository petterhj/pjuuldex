import http from '../http';

const isProduction = process.env.NODE_ENV === 'production';

export default {
  namespaced: true,
  state: {
    auth: {
      token: localStorage.getItem('token') || null,
      error: false,
    },
    username: null,
  },
  getters: {
    isAuthenticated: state => !!state.auth.token,
    authError: state => state.auth.error,
    currentUser: state => state.username,
  },
  mutations: {
    setAuthError: (state, error) => state.auth.error = error,
    setUsername: (state, username) => state.username = username,
    setToken(state, token) {
      console.log('Got token, setting')
      if (!isProduction) localStorage.setItem('token', token)
      state.auth.token = token
      state.auth.error = false
    },
    loggedOutUser(state) {
      localStorage.removeItem('token');
      state.auth.token = null
      state.username = null
    }
  },
  actions: {
    login({ commit, dispatch }, { username, password }) {
      if (!username || !password)
        return
      console.log(`Logging in as ${username}`)
      return http.post('user/login/', { username, password })
        .then((response) => {
          commit('setToken', response.data.key)
          dispatch('getUser')
        })
        .catch((error) => {
          console.log('Login failed')
          console.log(error)
          console.log(error.response.data)
          console.log(error.response.status)
          commit('setAuthError', true)
        });
    },
    logout({ commit, rootState }) {
      return http.post('user/logout/')
        .then(() => console.log('Logged out'))
        .finally(() => {
          commit('loggedOutUser')
          this.dispatch('main/getSets')
          if (rootState.main.currentSet)
            this.dispatch('main/getSet', rootState.main.currentSet.slug)
          this.commit('main/setRecentInventory', [])
        });
    },
    getUser({ commit, getters }) {
      if (!getters.isAuthenticated)
        return
      console.log("Fetching user data")
      return http.get('user/')
        .then((response) => {
          commit('setUsername', response.data.username)
          this.dispatch('main/getSets')
          this.dispatch('main/getRecentInventory')
        })
        .catch((error) => {
          this.dispatch('logout')
        });
    },
  }
}
