import Vue from 'vue';
// import Axios
import axios from 'axios';

import Store from '../store';

const apiUrl = '/api';

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
                commit('data/setUser', user);
                localStorage.setItem('token', result.data.token);
                Vue.$log.debug('Vuex', 'user obj from response', user);
                commit('data/setToken', result.data.token);
                axios.defaults.headers.common['X-CSRFTOKEN'] = Store.getCookie('csrftoken');
                return true;
            }
            return false;
        }).catch((error) => {
            Vue.$log.debug(error);
            return false;
        });
    }
};

export default {

    actions
};
