import axios from 'axios'

const apiUrl = '/api'

export default {
    getUsers(params) {
        return axios.get(`${apiUrl}/auth/getUsers/`, {
            params
        });
    },
    getUserClustering(params) {
        return axios.get(`${apiUrl}/auth/similarUser/`, {
            params
        });
    }
};