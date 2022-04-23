import { createApp } from 'vue'

import App from './views/App.vue'
import Store from './components/Store.js'
import createVueRouter from './components/Router.js'

import './styles/main.styl'
import './styles/forms.styl'
import './styles/scrollbars.styl'


createApp(App)
  .use(createVueRouter(Store))
  .use(Store)
  .mount('#app');
