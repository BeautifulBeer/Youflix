import Vue from 'vue';
// import Axios
import axios from 'axios';
import global from '../plugins/global';

const state = {
    personalMovies: [],
    genreMovies: {},
    searchResultMovies: {
        category: 'genre',
        keyword: 'Total',
        title: '',
        result: []
    },
    selectedMovie: {},
    isloaded: true
};

const actions = {
    async getMovieById({ commit }, movieId) {
        Vue.$log.debug('Vuex movie.js getMovieById', movieId);
        axios.get(`${global.API_URL}/movies/`, {
            params: {
                id: movieId
            }
        }).then((response) => {
            if (response.data.status === global.HTTP_SUCCESS) {
                Vue.$log.debug('Vuex movie.js getMovieById response', response.data);
                const { result } = response.data;
                commit('setSelectedMovie', result[0]);
                return true;
            }
            return false;
        });
    },
    async addMovieView({ commit }, movieId) {
        Vue.$log.debug('Vuex movie.js addMovieView', movieId);
        return axios.get(`${global.API_URL}/movies/views/`, {
            params: {
                id: movieId
            }
        }).then((response) => {
            if (response.data.status === global.HTTP_SUCCESS) {
                Vue.$log.debug('Vuex movie.js addMovieView response', true);
                return true;
            }
            return false;
        });
    },
    async getMovieByConditions({ state, commit }) {
        Vue.$log.debug('Vuex movie.js getMovieByConditions', state.searchResultMovies);
        axios.get(`${global.API_URL}/movies/`, {
            params: {
                category: state.searchResultMovies.category,
                keyword: state.searchResultMovies.keyword,
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
                    category: 'genre',
                    keyword: genre,
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
    async getRatingPref({ commit }, email) {
        Vue.$log.debug('Vuex movie.js getRatingPref', email);
        return axios.get(`${global.API_URL}/movies/pref/`, {
            params: {
                email
            }
        }).then((response) => {
            Vue.$log.debug('Vuex movie.js getRatingPref response', response);
            return response.data;
        });
    },
    async getNeverSeenMovieList({ commit }, email) {
        Vue.$log.debug('Vuex movie.js getNeverSeenMovieList', email);
        return axios.get(`${global.API_URL}/movies/neverSeenMovies/`, {
            params: {
                email
            }
        }).then((response) => {
            Vue.$log.debug('Vuex movie.js getNeverSeenMovieList response', response);
            return response.data;
        });
    },
    // For Test
    async getContentBased({ commit }, email) {
        Vue.$log.debug('Vuex movie.js getContentBased', email);
        return axios.get(`${global.API_URL}/contentBased/`, {
            params: {
                email
            }
        }).then((response) => {
            Vue.$log.debug('Vuex movie.js getContentBased response', response);
            return response.data;
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
    setSelectedMovie(state, movie) {
        state.selectedMovie = movie;
    },
    setSearchConditionTitle(state, title) {
        state.searchResultMovies.title = title;
    },
    setSearchConditionCategory(state, category) {
        state.searchResultMovies.category = category;
    },
    setSearchConditionKeyword(state, keyword) {
        state.searchResultMovies.keyword = keyword;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations
};
