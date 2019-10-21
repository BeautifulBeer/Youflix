import Vue from 'vue';
// import Axios
import axios from 'axios';
import global from '../plugins/global';

const state = {
    personalMovies: [],
    genreMovies: {},
    searchResultMovies: {
        genre: 'Romance',
        title: 'mariposa',
        result: {}
    },
    isloaded: true
};

const actions = {
    // async getMovieById({ commit }, movieId) {
    //     Vue.$log.debug('Vuex movie.js getMovieById', movieId);
    //     axios.get(`${global.API_URL}/movies`, {
    //         params: {
    //             id: movieId
    //         }
    //     }).then((response) => {
    //         if (response.data.status === global.HTTP_SUCCESS) {
    //             const { result } = response.data;
    //             return result;
    //         }
    //         return {};
    //     });
    // },
    async addMovieView({ commit }, movieId) {
        return axios.get(`${global.API_URL}/movies/views`, {
            params: {
                id: movieId
            }
        }).then((response) => {
            if (response.data.status === global.HTTP_SUCCESS) {
                return true;
            }
            return false;
        });
    },
    async getMovieByConditions({ state, commit }) {
        Vue.$log.debug('Vuex movie.js getMovieByConditions', state.searchResultMovies);
        axios.get(`${global.API_URL}/movies/`, {
            params: {
                genres: state.searchResultMovies.genre,
                title: state.searchResultMovies.title
            }
        }).then((response) => {
            if (response.data.status === global.HTTP_SUCCESS) {
                const { result } = response.data;
                commit('setSearchResultMovies', result);
                return true;
            }
            return false;
        });
    },
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
    },
    setSearchResultMovies(state, result) {
        state.searchResultMovies.result = result;
    },
    setSearchCondition(state, { genre, title }) {
        state.searchResultMovies.genre = genre;
        state.searchResultMovies.title = title;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations
};
