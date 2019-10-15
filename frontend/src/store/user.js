import Vue from 'vue';
import Vuex from 'vuex';
// import Axios
import axios from 'axios';

const apiUrl = '/api';

const actions = {

    async updateUserInfo({ commit }, params) {

        return axios.post(`${apiUrl}/auth/updateUser/`, {
            params
        }).then((ret) => {
            Vue.$log.debug('update response', ret);
        });
    }
};

export default {

    actions
};
