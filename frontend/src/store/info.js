import swal from 'sweetalert';

const state = {

    genres: [
        'TV Movie',
        'Foreign',
        'War',
        'Family',
        'Romance',
        'Music',
        'Mystery',
        'Science Fiction',
        'Documentary',
        'Crime',
        'Thriller',
        'Western',
        'History',
        'Comedy',
        'Action',
        'Horror',
        'Drama',
        'Animation',
        'Fantasy',
        'Adventure'
    ]
};

const actions = {

    commingSoon() {
        swal({
            title: 'Comming Soon',
            text: '아직 준비중인 서비스입니다.',
            icon: 'info',
            button: false
        });
    }
};

export default {

    state,
    actions
};
