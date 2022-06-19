import { createApp } from 'vue'

import App from './views/App.vue'
import Store from './components/Store.js'
import createVueRouter from './components/Router.js'

import VueFusionCharts from 'vue-fusioncharts';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import FusionTheme from './res/fusion-theme.js';

import './styles/main.styl'
import './styles/forms.styl'
import './styles/scrollbars.styl'

FusionCharts.register('theme', FusionTheme);


createApp(App)
  .use(createVueRouter(Store))
  .use(Store)
  .use(VueFusionCharts, FusionCharts, Charts)
  .mount('#app');
