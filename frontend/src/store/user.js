import Vue from 'vue';
// import Axios
import axios from 'axios';
import getCookie from '../plugins/cookie';

const apiUrl = '/api';

// state
const state = {
    user: null,
    token: null
};

const actions = {
    async updateUserInfo({ commit }, params) {
        Vue.$log.debug('UpdateUser params', params);
        return axios.post(`${apiUrl}/auth/updateUser/`, {
            params
        }).then((result) => {
            Vue.$log.debug('UpdateUser response', result);
            if (result.data.is_auth) {
                const user = {
                    email: result.data.email,
                    username: result.data.username,
                    token: result.data.token,
                    gender: result.data.gender,
                    age: result.data.age,
                    occupation: result.data.occupation,
                    is_staff: result.data.is_staff,
                    movie_taste: JSON.parse(result.data.movie_taste.replace(/'/g, '"'))
                };
                commit('setUser', user);
                localStorage.setItem('token', result.data.token);
                Vue.$log.debug('Vuex', 'user obj from response', user);
                commit('setToken', result.data.token);
                axios.defaults.headers.common['X-CSRFTOKEN'] = getCookie('csrftoken');
                return true;
            }
            return false;
        }).catch((error) => {
            Vue.$log.debug(error);
            return false;
        });
    },
    async checkDuplicateEmail({ state }, email) {
        Vue.$log.debug('Duplicate param ', email);
        const ret = axios.get(`${apiUrl}/auth/duplicateInspection/`, {
            params: {
                email
            }
        }).then(() => true).catch(() => false);
        return ret;
    },
    async registerMember({ commit }, params) {
        Vue.$log.debug('store.js', params);
        return axios.post(`${apiUrl}/auth/registermember/`, {
            params
        });
    },

    async login({ commit }, params) {
        Vue.$log.debug('Vuex', params);
        const resp = axios.post(`${apiUrl}/auth/loginmember/`, {
            email: params.email,
            password: params.password
        }).then((result) => {
            Vue.$log.debug('Vuex response', result.data.movie_taste.replace(/'/g, '"'));
            if (result.data.is_auth) {
                const user = {
                    email: result.data.email,
                    username: result.data.username,
                    token: result.data.token,
                    gender: result.data.gender,
                    age: result.data.age,
                    occupation: result.data.occupation,
                    is_staff: result.data.is_staff,
                    movie_taste: JSON.parse(result.data.movie_taste.replace(/'/g, '"'))
                };
                commit('setUser', user);
                localStorage.setItem('token', result.data.token);
                Vue.$log.debug('Vuex', 'user obj from response', user);
                commit('setToken', result.data.token);
                axios.defaults.headers.common['X-CSRFTOKEN'] = getCookie('csrftoken');
                return true;
            }
            return false;
        }).catch((error) => {
            Vue.$log.debug(error);
            return false;
        });
        return resp;
    },

    async logout({ commit, state }) {
        Vue.$log.debug(state.token);
        return axios.post(`${apiUrl}/auth/logoutmember/`, {
            token: state.token
        }).then(() => {
            localStorage.removeItem('token');
            commit('setUser', null);
            commit('setToken', null);
            return true;
        });
    },

    async getSession({ commit }) {
        Vue.$log.debug('Vuex', localStorage.getItem('token'));
        return axios.post(`${apiUrl}/auth/session/`, {
            token: localStorage.getItem('token')
        }).then((result) => {
            Vue.$log.debug('Vuex response result', result);

            if (result.data.is_auth) {
                commit('setUser', {
                    email: result.data.email,
                    username: result.data.username,
                    token: result.data.token,
                    gender: result.data.gender,
                    age: result.data.age,
                    occupation: result.data.occupation,
                    is_staff: result.data.is_staff,
                    movie_taste: JSON.parse(result.data.movie_taste.replace(/'/g, '"'))
                });
            } else {
                localStorage.removeItem('token');
                commit('setUser', null);
            }
            return result.data.is_auth;
        });
    },

    async getUserBySession({ commit }, token) {
        Vue.$log.debug('Vuex', token);
        return axios.get(`${apiUrl}/auth/session/`, {
            params: {
                token
            }
        }).then((response) => {
            Vue.$log.debug('Vuex response', response.data.movie_taste.replace(/'/g, '"'));
            commit('setUser', {
                email: response.data.email,
                username: response.data.username,
                token: response.data.token,
                gender: response.data.gender,
                age: response.data.age,
                occupation: response.data.occupation,
                is_staff: response.data.is_staff,
                movie_taste: JSON.parse(response.data.movie_taste.replace(/'/g, '"'))
            });
        }).catch((error) => {
            Vue.$log.debug('Vuex getUserBySession error', error);
            localStorage.removeItem('token');
        });
    }
};

// mutations
const mutations = {
    setProfileList(state, profiles) {
        state.profileList = profiles;
    },
    setUser(state, user) {
        Vue.$log.debug('Vuex mutations', 'state obj', state, 'user', user);
        state.user = user;
    },
    setToken(state, token) {
        state.token = token;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations
};
