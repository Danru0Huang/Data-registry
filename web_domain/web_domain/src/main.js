import Vue from 'vue'
import App from './App.vue'
//引入VueRouter
import VueRouter from 'vue-router'
//引入路由器
import router from './router'
//引入axios
import axios from 'axios'
//引入外部element
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
//引入echarts
import * as echarts from 'echarts';
//import echarts from "echarts";
//引入内网转公网ngrok
import { apiBaseUrl } from './config';

Vue.prototype.$apiBaseUrl = apiBaseUrl;
Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false
Vue.prototype.$axios = axios;
//应用插件
Vue.use(VueRouter)
Vue.use(ElementUI)

new Vue({
  el: '#app',
  render: h => h(App),
  router: router
})
