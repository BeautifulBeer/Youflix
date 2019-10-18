import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

// ======Import Other store===========
import infoStore from './store/info';
import userStore from './store/user';
import movieStore from './store/movie';
// ===================================

// ======Import getCookie=============
import getCookie from './plugins/cookie';
// ===================================

Vue.use(Vuex);

axios.defaults.headers.common['X-CSRFTOKEN'] = getCookie('csrftoken');

export default new Vuex.Store({
    modules: {
        infos: infoStore,
        users: userStore,
        movies: movieStore
    }
});
