import axios from 'axios';

const apiUrl = '/api';

export default {
    getUserMoviePref(email) {
        return axios.get(`${apiUrl}/movies/pref/`, {
            params: {
                email
            }
        });
        
    },
    getAllMovies(params){
        return axios.get(`${apiUrl}/movies/`, {
            params,
        })
    },
    modifyMovie(data){
        return axios.post(`${apiUrl}/movies/modify/`, {
            data,
        })
    }
};
