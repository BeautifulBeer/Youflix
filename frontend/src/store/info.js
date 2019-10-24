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
    ],
    occupations: [
        'other',
        'academic/educator',
        'artist',
        'clerical/admin',
        'college/grad student',
        'customer service',
        'doctor/health care',
        'executive/managerial',
        'farmer',
        'homemaker',
        'K-12 student',
        'lawyer',
        'programmer',
        'retired',
        'sales/marketing',
        'scientist',
        'self-employed',
        'technician/engineer',
        'tradesman/craftsman',
        'unemployed',
        'writer'
    ],
    category: {
        genre: [
            'New',
            'Drama',
            'Documentary',
            'Animation',
            'English',
            'Adventure',
            'Fantasy',
            'Disaster',
            'Romance',
            'History',
            'Sitcom',
            'Sport',
            'Science Fiction',
            'Music',
            'Teen'
        ],
        nation: [
            'English',
            'German',
            'Canada',
            'India',
            'Taiwan',
            'Hongkong',
            'France',
            'Spain',
            'China',
            'Japan',
            'Korea',
            'Italy'
        ],
        property: [
            'Queen',
            'HBO',
            'Middle Ages',
            'Miserable',
            'Another World',
            'Magic',
            'Betray',
            'Spectacle',
            'Siberia',
            'Hotel',
            'Novel',
            'Experimental',
            'Serious',
            'Marvel',
            'Pixar',
            '7080',
            'Blockbuster'
        ]
    },
    rules: {
        nicknameLenCheck: (value) => (value.length >= 2 && value.length <= 10) || '닉네임은 2-10자까지만 가능합니다.',
        passwordLenCheck: (value) => (value.length >= 6 && value.length <= 30) || '비밀번호는 6-30자까지만 가능합니다.',
        nicknameCheck: (value) => (/^[a-zA-Z0-9[가-힣]+]*$/).test(value) || '영문, 한글, 숫자만 가능합니다.',
        passwordCheck: (value) => (/^[a-zA-Z0-9!@#$%^&*]*$/).test(value) || '영문, 숫자, 특수문자(!@#$%^&*)만 가능합니다.'
    }
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
    namespaced: true,
    state,
    actions
};
