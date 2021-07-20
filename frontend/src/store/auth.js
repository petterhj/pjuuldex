import http from '../http';

export default {
  namespaced: true,
  state: {
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    username: localStorage.getItem('username') || null,
    error: false,
  },
  getters: {
    isAuthenticated: state => (state.accessToken && state.username),
    refreshToken: state => state.refreshToken,
    authError: state => state.error,
    currentUser: state => state.username,
  },
  mutations: {
    setAuthError: (state, error) => state.error = error,
    setLoggedIn: (state, auth_response) => {
      console.log('Setting logged in state')
      localStorage.setItem('accessToken', auth_response.access_token)
      localStorage.setItem('refreshToken', auth_response.refresh_token)
      localStorage.setItem('username', auth_response.user.username)
      state.accessToken = auth_response.access_token
      state.refreshToken = auth_response.refresh_token
      state.username = auth_response.user.username
      state.error = false
    },
    setAccessToken: (state, accessToken) => {
      console.log('Setting access token')
      localStorage.setItem('accessToken', accessToken)
      state.accessToken = accessToken
    },
    // setRefreshToken: (state, refreshToken) => {
    //   console.log("Setting refresh token")
    //   localStorage.setItem('refreshToken', refreshToken)
    // },
    setLoggedOut: (state) => {
      console.log("Setting logged out state")
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('username');
      state.accessToken = null
      state.refreshToken = null
      state.username = null
    }
  },
  actions: {
    login({ commit }, { username, password }) {
      if (!username || !password)
        return
      console.log(`Logging in as ${username}`)
      return http.post('user/login/', { username, password })
        .then((response) => {
          if (response.data && response.data.access_token) {
            commit('setLoggedIn', response.data)
            
            this.dispatch('main/getSets')
            this.dispatch('main/getRecentInventory')
          } else {
            commit('setAuthError', true)
          }
        })
        .catch((error) => {
          console.log('Login failed')
          console.log(error)
          // console.log(error.response.data)
          // console.log(error.response.status)
          commit('setAuthError', true)
        });
    },
    // refreshToken({ commit, getters }) {
    //   let refreshToken = getters.refreshToken
    //   if (!refreshToken)
    //     return
    //   console.log("Refreshing access token")
    //   return http.post('user/token/refresh/', {
    //     refresh: refreshToken
    //   })
    //     .then((response) => {
    //       commit('setAccessToken', response.data.access)
    //     })
    //     .catch((error) => {
    //       console.log('Refresh token failed')
    //       console.log(error)
    //       this.dispatch('logout')
    //     });
    // },
    logout({ commit, rootState }) {
      return http.post('user/logout/')
        .then(() => console.log('Logged out'))
        .finally(() => {
          commit('setLoggedOut')
          this.dispatch('main/getSets')
          if (rootState.main.currentSet)
            this.dispatch('main/getSet', rootState.main.currentSet.slug)
          this.commit('main/setRecentInventory', [])
        });
    },
    // getUser({ commit, getters }) {
    //   if (!getters.isAuthenticated)
    //     return
    //   console.log("Fetching user data")
    //   return http.get('user/')
    //     .then((response) => {
    //       commit('setUsername', response.data.username)
    //       this.dispatch('main/getSets')
    //       this.dispatch('main/getRecentInventory')
    //     })
    //     .catch((error) => {
    //       this.dispatch('logout')
    //     });
    // },
  }
}
