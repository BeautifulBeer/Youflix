import Vue from 'vue';
// import Axios
import axios from 'axios';
import global from '../plugins/global';

const state = {
    personalMovies: [],
    genreMovies: {},
    isloaded: true
};

const actions = {
    async getMoviesByGenres({ commit }, preferences) {
        Vue.$log.debug('Vuex movie.js getMoviesByGenres', preferences);
        let promises = [];
        preferences.forEach((genre) => {
            promises.push(axios.get(`${global.API_URL}/movies/`, {
                params: {
                    genres: genre,
                    page: 1
                }
            }));
        });
        return Promise.all(promises).then((responses) => {
            for (let i = 0; i < preferences.length; i += 1) {
                Vue.$log.debug('Vuex movie.js getMoviesByGenres promises all', preferences[i], responses[i].data);
                if (responses[i].data.status === global.HTTP_SUCCESS) {
                    const { result } = responses[i].data;
                    commit('setGenreMovies', { genre: preferences[i], movies: result });
                }
            }
            return preferences[0];
        });
    },
    async getMoviesByPersonal({ commit }, user) {
        Vue.$log.debug('Vuex movie.js getMoviesByPersonal', user);
        const targetUser = 5797;
        axios.get(`${global.API_URL}/auth/recommendMovie/`, {
            params: {
                id: targetUser
            }
        }).then((response) => {
            Vue.$log.debug('Vuex movie.js getMoviesByPersonal response', response);
            const { result } = response.data;
            commit('setPersonalMovies', result);
            commit('setIsLoaded', true);
        });
    },
    async rateMovie({ commit }, params) {
        Vue.$log.debug('Vuex movie.js rateMovie', params);
        axios.get(`${global.API_URL}/rateMovie/`, {
            params
        }).then((response) => {
            Vue.$log.debug('Vuex movie.js rateMovie response', response);
        });
    }
};

const mutations = {
    setPersonalMovies(state, movies) {
        state.personalMovies = movies;
    },
    setIsLoaded(state, flag) {
        state.isloaded = flag;
    },
    setGenreMovies(state, { genre, movies }) {
        state.genreMovies[genre] = movies;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations
};
