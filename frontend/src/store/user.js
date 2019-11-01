import Vue from 'vue';
import axios from 'axios';
import global from '../plugins/global';

// state
const state = {
    user: null,
    token: null
};

const actions = {
    async updateUserInfo({ commit }, params) {
        Vue.$log.debug('Vuex UpdateUser params', params);
        return axios.post(`${global.API_URL}/auth/updateUser/`, {
            params
        }).then((response) => {
            Vue.$log.debug('UpdateUser response', response);
            if (response.data.status === global.HTTP_SUCCESS) {
                const { result } = response.data;
                Vue.$log.debug('success update user info', result);
                if (result.is_auth) {
                    commit('setUser', result);
                    localStorage.setItem('token', result.token);
                    Vue.$log.debug('Vuex', 'user obj from response', result);
                    commit('setToken', result.token);
                    return true;
                }
            }
            return false;
        });
    },

    async checkDuplicateEmail({ state }, email) {
        Vue.$log.debug('Duplicate param ', email);
        const ret = axios.get(`${global.API_URL}/auth/duplicateInspection/`, {
            params: {
                email
            }
        }).then(() => true).catch(() => false);
        return ret;
    },

    async registerMember({ commit }, params) {
        Vue.$log.debug('Vuex registerMember', params);
        return axios.post(`${global.API_URL}/auth/registermember/`, {
            params
        }).then((response) => {
            if (response.data.status === global.HTTP_SUCCESS) {
                return true;
            }
            return false;
        });
    },

    async login({ commit }, params) {
        Vue.$log.debug('Vuex', params);
        return axios.post(`${global.API_URL}/auth/loginmember/`, {
            email: params.email,
            password: params.password
        }).then((response) => {
            Vue.$log.debug('Vuex login response', response);
            if (response.data.status === global.HTTP_SUCCESS) {
                Vue.$log.debug('Vuex login response success');
                // result가 곧 user에 대한 데이터임
                const { result } = response.data;
                if (result.is_auth) {
                    if (result.movie_taste !== '') {
                        result.movie_taste = JSON.parse(result.movie_taste.replace(/'/g, '"'));
                    }
                    commit('setUser', result);
                    localStorage.setItem('token', result.token);
                    Vue.$log.debug('Vuex', 'user obj from response', result);
                    commit('setToken', result.token);
                    return true;
                }
            }
            return false;
        });
    },

    async logout({ commit }, token) {
        Vue.$log.debug('Vuex logout', token);
        return axios.post(`${global.API_URL}/auth/logoutmember/`, {
            token
        }).then((response) => {
            Vue.$log.debug('Vuex logout response', response);
            if (response.data.status === global.HTTP_SUCCESS) {
                localStorage.removeItem('token');
                commit('setUser', null);
                commit('setToken', null);
                return true;
            }
            return false;
        });
    },
    async getUserBySession({ commit }, token) {
        Vue.$log.debug('Vuex user.js getUserBySession', token);
        return axios.get(`${global.API_URL}/auth/session/`, {
            params: {
                token
            }
        }).then((response) => {
            Vue.$log.debug('Vuex user.js getUserBySession response', response.data);
            if (response.data.status === global.HTTP_SUCCESS) {
                const { result } = response.data;
                if (result.is_auth) {
                    commit('setUser', {
                        email: result.email,
                        username: result.username,
                        token: result.token,
                        gender: result.gender,
                        age: result.age,
                        occupation: result.occupation,
                        is_staff: result.is_staff,
                        movie_taste: JSON.parse(result.movie_taste.replace(/'/g, '"'))
                    });
                    return true;
                }
            }
            return false;
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
