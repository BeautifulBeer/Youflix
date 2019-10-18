import Vue from 'vue';
// import Axios
import axios from 'axios';

const apiUrl = '/api';

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
            promises.push(axios.get(`${apiUrl}/movies/`, {
                params: {
                    genres: genre,
                    page: 1
                }
            }));
        });
        return Promise.all(promises).then((responses) => {
            for (let i = 0; i < preferences.length; i += 1) {
                Vue.$log.debug('Vuex movie.js getMoviesByGenres promises all', preferences[i], responses[i].data);
                commit('setGenreMovies', { genre: preferences[i], movies: responses[i].data });
            }
            return preferences[0];
        });
    },
    async getMoviesByPersonal({ commit }, user) {
        Vue.$log.debug('Vuex movie.js getMoviesByPersonal', user);
        const targetUser = 5797;
        axios.get(`${apiUrl}/auth/recommendMovie/`, {
            params: {
                id: targetUser
            }
        }).then((response) => {
            commit('setPersonalMovies', response.data);
            commit('setIsLoaded', true);
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
