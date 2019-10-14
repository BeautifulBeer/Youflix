import axios from 'axios';

const apiUrl = '/api';

export default {
    getUserMoviePref(email) {
        console.log("PARAMS ", email);
        return axios.get(`${apiUrl}/movies/pref/`, {
            params: {
                email
            }
        });
    }
};
