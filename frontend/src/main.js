import axios from 'axios';
import SmoothScrollbar from 'vue-smooth-scrollbar';
// https://www.npmjs.com/package/vuejs-logger
import VueLogger from 'vuejs-logger';
import Vue from 'vue';
import lineClamp from 'vue-line-clamp';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import AnimateWhenVisible from './components/AnimateWhenVisible.vue';
import router from './router';
import store from './store';
// CSS, SCSS
import './style/app.scss';

// ======Import getCookie=============
import getCookie from './plugins/cookie';
// ===================================

// USE LOGGER
const isProduction = process.env.NODE_ENV === 'production';
const options = {
    isEnabled: true,
    logLevel: isProduction ? 'error' : 'debug',
    stringifyArguments: false,
    showLogLevel: true,
    showMethodName: true,
    separator: '|',
    showConsoleColors: true
};
Vue.use(VueLogger, options);

// USE SECTION
Vue.config.productionTip = false;
// SmoothScrollbar
Vue.use(SmoothScrollbar);
Vue.component('AnimateWhenVisible', AnimateWhenVisible);
// Line clamp
Vue.use(lineClamp, {
    // plugin options
});

// 로그인 세션에 대한 접근제어
router.beforeResolve((to, from, next) => {
    const token = localStorage.getItem('token');
    Vue.$log.debug('Main.js router beforeResolve', token, to, from);
    // 로그인 했을때 로그인이 필요하지 않은 곳으로
    if (token && !to.meta.authRequired) {
        return next('/home');
    }
    // 로그인 안했을 때 로그인이 필요한 곳으로
    if (!token && to.meta.authRequired) {
        return next('/');
    }
    return next();
});

// CSRFTOKEN을 매 request마다 체크하여 없으면 넣어준다.
axios.interceptors.request.use((config) => {
    Vue.$log.debug('axios interceptors req', config);
    if (!('X-CSRFTOKEN' in config.headers)) {
        Vue.$log.debug('axios interceptors check X-CSRFTOKEN', 'Nope');
        // eslint-disable-next-line
        config.headers['X-CSRFTOKEN'] = getCookie('csrftoken');
    }
    return config;
}, (err) => {
    Vue.$log.debug('axios interceptors err', err);
    return Promise.reject(err);
});


new Vue({
    vuetify,
    router,
    store,
    render: (h) => h(App)
}).$mount('#app');
