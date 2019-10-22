import Vue from 'vue';
// import Axios
import axios from 'axios';
import global from '../plugins/global';

const actions = {
    async rateMovie({ commit }, params) {
        Vue.$log.debug('Vuex movie.js rateMovie', params);
        axios.get(`${global.API_URL}/rateMovie/`, {
            params
        }).then((response) => {
            Vue.$log.debug('Vuex movie.js rateMovie response', response);

            let ratingWord = '최고에요!';

            if (params.ratingValue === 0.5) {
                ratingWord = '최악이에요!';
            } else if (params.ratingValue === 1.0) {
                ratingWord = '싫어요';
            } else if (params.ratingValue === 1.5) {
                ratingWord = '재미없어요';
            } else if (params.ratingValue === 2.0) {
                ratingWord = '별로에요';
            } else if (params.ratingValue === 2.5) {
                ratingWord = '부족해요';
            } else if (params.ratingValue === 3.0) {
                ratingWord = '보통이에요';
            } else if (params.ratingValue === 3.5) {
                ratingWord = '볼만해요';
            } else if (params.ratingValue === 4.0) {
                ratingWord = '재미있어요';
            } else if (params.ratingValue === 4.5) {
                ratingWord = '훌륭해요';
            }
            return ratingWord;
        });
    },
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
