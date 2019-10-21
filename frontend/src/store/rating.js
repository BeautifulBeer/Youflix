import Vue from 'vue';
// import Axios
import axios from 'axios';
import global from '../plugins/global';

const actions = {
    async getRating({ commit }, email) {
        Vue.$log.debug('Vuex movie.js getRating', email);
        return axios.get(`${global.API_URL}/getRating/`, {
            params: {
                email
            }
        }).then((response) => {
            const { result } = response.data;
            Vue.$log.debug('Vuex movie.js getRating RESULT', result);
            return result;
        });
    }
};

export default {
    namespaced: true,
    actions
};
