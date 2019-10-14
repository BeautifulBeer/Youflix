import SmoothScrollbar from 'vue-smooth-scrollbar';
// https://www.npmjs.com/package/vuejs-logger
import VueLogger from 'vuejs-logger';
import Vue from 'vue';
import { mapActions } from 'vuex';
import lineClamp from 'vue-line-clamp';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import AnimateWhenVisible from './components/AnimateWhenVisible.vue';
import router from './router';
import store from './store';
// CSS, SCSS
import './style/app.scss';

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
    Vue.$log.debug('Main.js router beforeResolve', token);
    // 로그인 했을때
    if (token) {
        // 로그인이 필요하지 않은 곳으로
        if (!to.meta.authRequired) {
            return next('/home');
        }
    // 로그인 안했을때
    } else {
        // 로그인이 필요한 곳으로
        if (to.meta.authRequired) {
            return next('/');
        }
    }
    return next();
});

new Vue({
    vuetify,
    router,
    store,
    created() {
        if (localStorage.getItem('token') !== undefined && localStorage.getItem('token') !== null) {
            if (this.getSession() === false) { // 토큰이 잘못된 값일 때
                router.push('/');
            }
        } else { // 토큰 없을 때
            router.push('/');
        }
    },
    methods: {
        ...mapActions({
            getSession: 'data/getSession'
        })
    },
    render: (h) => h(App)
}).$mount('#app');
