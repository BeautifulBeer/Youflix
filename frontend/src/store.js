import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

// ======Import Other store===========
import infoStore from './store/info';
import userStore from './store/user';
// ===================================

// ======Import getCookie=============
import getCookie from './plugins/cookie';
// ===================================

// =========Static Variable===========
const apiUrl = '/api';
// ===================================

Vue.use(Vuex);

axios.defaults.headers.common['X-CSRFTOKEN'] = getCookie('csrftoken');

export default new Vuex.Store({
    modules: {
        infos: infoStore,
        users: userStore
    }
});
