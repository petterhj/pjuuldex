import axios from 'axios';
import { store } from './store'
// import { router } from './main'

const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

// console.log(router)

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-type': 'application/json',
  },
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_NAME,
});

http.interceptors.request.use(function(request) {
  const accessToken = store.state.auth.accessToken

  if (accessToken) {
    console.log("Requesting data with access token")
    request.headers.Authorization = `Bearer ${accessToken}`;
  } else {
    console.log("Unauthenticated (no access token)")
  }

  return request;
})

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    console.log("Response status", error.response.status)
    const originalConfig = error.config;

    if (error.response.status === 403) {
      console.log("Refreshing token...")
      try {
        const refresh_response = await refreshToken();
        store.commit('auth/setAccessToken', refresh_response.data.access);
        originalConfig.headers.Authorization = `Bearer ${refresh_response.data.access}`;
        return http(originalConfig);
      } catch (refresh_error) {
        console.log("Refresh token failed")
        store.commit('auth/setLoggedOut')
        return refresh_error
      }
    }
    return error
  }
);

function refreshToken() {
  return http.post('user/token/refresh/', {
    refresh: store.state.auth.refreshToken
  })
}

export default http;
