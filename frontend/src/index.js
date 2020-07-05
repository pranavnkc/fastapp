import Vue from 'vue';
import Vuelidate from 'vuelidate';

import { router } from './_helpers';
import App from './app/App';
import api from "./_services/api";

Vue.use(Vuelidate);
Vue.config.productionTip = false;
Vue.prototype.$http = api; 
api.defaults.timeout = 10000;
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.common["Authorization"] = "token "+token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);
api.interceptors.response.use(
  response => {
    if (response.status === 200 || response.status === 201) {
      return Promise.resolve(response);
    } else {
      return Promise.reject(response);
    }
  },
error => {
    if (error.response.status) {
      switch (error.response.status) {
        case 400:
         
         //do something
          break;
      
        case 401:
          alert("session expired");
          break;
        case 403:
          router.replace({
            path: "/login",
            query: { redirect: router.currentRoute.fullPath }
          });
           break;
        case 404:
          alert('page not exist');
          break;
        case 502:
         setTimeout(() => {
            router.replace({
              path: "/login",
              query: {
                redirect: router.currentRoute.fullPath
              }
            });
          }, 1000);
      }
      return Promise.reject(error.response);
    }
  }
);

new Vue({
    el: '#app',
    router,
    render: h => h(App)
});
