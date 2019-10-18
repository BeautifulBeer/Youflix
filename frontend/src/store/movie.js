import Vue from 'vue';
// import Axios
import axios from 'axios';

const apiUrl = '/api';

const state = {
    movieSearchList: [],
    selectIndex: 0,
    movieVisible: false
};

const actions = {

};

const mutations = {
    setMovieSearchList(state, movies) {
        state.movieSearchList = movies.map((m) => m);
    },
    setSelectIndex(state, selectIndex) {
        state.selectIndex = selectIndex;
    },
    setViewCount(state) {
        state.movieSearchList[state.selectIndex].viewCnt += 1;
    },
    setMovieVisible(state, flag) {
        state.movieVisible = flag;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations
};
