import { createStore } from 'vuex'
import main from './store/main';
import auth from './store/auth';

export const store = createStore({
  modules: {
    main,
    auth,
  }
})
