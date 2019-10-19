import Vue from 'vue';
import Vuex from 'vuex';

// ======Import Other store===========
import infoStore from './store/info';
import userStore from './store/user';
import movieStore from './store/movie';
// ===================================

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        infos: infoStore,
        users: userStore,
        movies: movieStore
    }
});
