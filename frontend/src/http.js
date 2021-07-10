import axios from 'axios';
import { store } from './store'

const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-type': 'application/json',
  },
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_NAME,
});

http.interceptors.request.use(function(config) {
  const token = store.state.auth.auth.token;

  if (token)
    config.headers.Authorization = `Token ${token}`;

  return config;
})

export default http;
