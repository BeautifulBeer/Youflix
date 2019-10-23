<template>
    <div>
        <div
            v-if="getlogoutflag"
            style="height: 10vh;"
        />
        <nav id="header">
            <v-row class="wrapper">
                <v-col
                    cols="1"
                    class="wrapper"
                >
                    <v-row
                        justify="start"
                        style="height: 100%;"
                    >
                        <v-col
                            cols="12"
                            class="wrapper"
                        >
                            <v-btn
                                text
                                :to="getlogoutflag ? '/home' : '/'"
                                class="btn-link"
                                style="height: 100%;"
                            >
                                <span
                                    style="line-height: 10vh"
                                    class="log-font"
                                >
                                    YOUFLIX
                                </span>
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col
                    cols="1"
                >
                    <v-row
                        style="width: 100%; height: 100%;"
                        justify="center"
                        align="center"
                    >
                        <v-btn
                            text
                            color="transparent"
                            class="genre-btn"
                        >
                            <span
                                class="label"
                            >
                                탐색하기
                            </span>
                            <div
                                class="overlay"
                            >
                                <div class="category-wrapper">
                                    <div
                                        v-for="(value, key) in genres"
                                        :key="'categoryWrapper' + key"
                                        class="category"
                                        @click="setSearchConditionGenre(key)"
                                    >
                                        {{ key }}
                                    </div>
                                </div>
                                <div class="genres-wrapper">
                                    <div
                                        v-for="(genreRow, index) in get2DGenres[getSelectedGenre]"
                                        :key="'HeaderGenreCategory' + index"
                                        class="genre-row"
                                    >
                                        <div
                                            v-for="genre in genreRow"
                                            :key="'HeaderGenre' + genre"
                                            class="genre"
                                        >
                                            {{ genre }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </v-btn>
                        <v-btn
                            text
                            color="transparent"
                            class="genre-btn"
                        >
                            <span
                                class="label"
                            >
                                평가하기
                            </span>
                        </v-btn>
                    </v-row>
                </v-col>
                <v-col
                    v-if="getlogoutflag"
                    cols="10"
                    class="wrapper"
                >
                    <v-row
                        align="center"
                        justify="end"
                        class="wrapper"
                    >
                        <v-col cols="4">
                            <div class="search">
                                <div
                                    id="header-search-effect"
                                    class="search-effect"
                                />
                                <input
                                    id="header-search-input"
                                    v-model="keyword"
                                    type="search"
                                    class="search-box"
                                    placeholder="영화명"
                                >
                                <span
                                    class="search-button"
                                    @click="searchKeyword()"
                                >
                                    <span
                                        id="header-search-icon"
                                        class="search-icon"
                                    />
                                </span>
                            </div>
                        </v-col>
                        <v-col cols="1">
                            <div class="dropdown">
                                <v-btn
                                    text
                                >
                                    <span class="menu-font">
                                        {{ getUserName }}
                                        <i class="fa fa-angle-down" />
                                    </span>
                                </v-btn>
                                <div class="dropdown-content">
                                    <router-link to="/myflix">
                                        myflix
                                    </router-link>
                                    <router-link
                                        to="/setting"
                                    >
                                        setting
                                    </router-link>
                                    <router-link
                                        to="#"
                                    >
                                        likes
                                    </router-link>
                                    <router-link to="/adminPage">
                                        admin
                                    </router-link>
                                    <router-link
                                        to="#"
                                        @click="logoutState()"
                                    >
                                        logout
                                    </router-link>
                                </div>
                            </div>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </nav>
    </div>
</template>

<script>
import swal from 'sweetalert';
import { createNamespacedHelpers } from 'vuex';

const { mapState, mapActions } = createNamespacedHelpers('users');
const movieMapState = createNamespacedHelpers('movies').mapState;
const movieMapMutations = createNamespacedHelpers('movies').mapMutations;
const movieMapActions = createNamespacedHelpers('movies').mapActions;

export default {
    name: 'Header',
    data() {
        return {
            keyword: '',
            mouseOver: false,
            prevOffset: 0,
            genres: {
                장르: [
                    '새로 올라온 작품',
                    'TV 드라마',
                    'TV 다큐멘터리',
                    'TV 애니메이션',
                    '영어자막 지원 작품',
                    '모험',
                    '판타지',
                    '재난',
                    '로멘틱코미디',
                    '시대극',
                    '역사',
                    '시트콤',
                    '스포츠',
                    'SF',
                    '음악',
                    '틴에이저',
                    '전쟁',
                    '키즈'
                ],
                국가: [
                    '영국',
                    '독일',
                    '캐나다',
                    '인도',
                    '대만',
                    '홍콩',
                    '프랑스',
                    '스페인',
                    '중국',
                    '일본',
                    '한국',
                    '이탈리아'
                ],
                특징: [
                    '여왕',
                    'HBO',
                    '중세배경',
                    '참혹한',
                    '가공의세계',
                    '마법',
                    '배신',
                    '화려한',
                    '러시아배경',
                    '호텔',
                    '소설원작',
                    '실험적',
                    '진지한',
                    '마블',
                    '픽사',
                    '7080',
                    '블록버스터'
                ]
            },
            NumGenreOnRow: 3
        };
    },
    computed: {
        ...mapState({
            user: (state) => state.user,
            token: (state) => state.token,
            username: (state) => {
                return state.user ? state.user.username : state.user;
            }
        }),
        ...movieMapState(['searchResultMovies']),
        getlogoutflag() {
            return (this.token !== null && this.token !== undefined);
        },
        getUserName() {
            return this.username;
        },
        getSelectedGenre() {
            return this.searchResultMovies.genre === 'Total' ? '장르' : this.searchResultMovies.genre;
        },
        get2DGenres() {
            let result = {};
            for (let key in this.genres) {
                result[key] = [];
                const rows = parseInt(this.genres[key].length / this.NumGenreOnRow, 10);
                for (let i = 0; i <= rows; i += 1) {
                    const end = (i + 1) * this.NumGenreOnRow;
                    result[key].push(this.genres[key].slice(
                        i * this.NumGenreOnRow,
                        end >= this.genres[key].length ? this.genres[key].length : end
                    ));
                }
            }
            return result;
        }
    },
    mounted() {
        window.addEventListener('DOMContentLoaded', () => {
            const headerIcon = document.getElementById('header-search-icon');
            const headerInput = document.getElementById('header-search-input');
            const headerEffect = document.getElementById('header-search-effect');

            if (headerIcon) {
                headerIcon.addEventListener('mouseenter', () => {
                    this.mouseOver = true;
                });

                headerIcon.addEventListener('mouseleave', () => {
                    this.mouseOver = false;
                });
            }

            if (headerInput) {
                headerInput.addEventListener('focusout', () => {
                    if (!this.mouseOver) {
                        headerEffect.classList.remove('open');
                        headerIcon.classList.remove('open');
                        headerInput.value = '';
                    }
                });
            }
            if (this.getUser) {
                this.logoutflag = true;
            }
        });
        window.addEventListener('scroll', () => {
            const header = document.getElementById('header');
            if (parseInt(window.scrollY, 10) < this.prevOffset) {
                header.style.transform = 'translate(0,0)';
                header.style['-webkit-transform'] = 'translate(0,0)';
                header.style['-moz-transform'] = 'translate(0,0)';
                header.style['-ms-transform'] = 'translate(0,0)';
                header.style['-o-transform'] = 'translate(0,0)';
            } else {
                header.style.transform = 'translate(0,-100px)';
                header.style['-webkit-transform'] = 'translate(0,-100px)';
                header.style['-moz-transform'] = 'translate(0,-100px)';
                header.style['-ms-transform'] = 'translate(0,-100px)';
                header.style['-o-transform'] = 'translate(0,-100px)';
            }
            this.prevOffset = window.scrollY;
        });
    },
    methods: {
        ...movieMapMutations(['setSearchConditionTitle', 'setSearchConditionGenre']),
        ...movieMapActions(['getMovieByConditions']),
        ...mapActions(['logout', 'getSession']),
        changeFlag() {
            if (this.getLoginModalOpen === true) {
                this.$store.commit('setLoginModalOpen', false);
            } else {
                this.$store.commit('setLoginModalOpen', true);
            }
        },
        logoutState() {
            this.getSession().then((ret) => {
                if (ret === true) {
                    this.logout(this.token).then(() => {
                        swal({
                            title: 'GoodBye',
                            text: '다음에 또 만나요.',
                            icon: 'info',
                            button: false
                        }).then(() => {
                            window.location = '/';
                        });
                    });
                } else {
                    swal({
                        title: 'Error',
                        text: 'Server Error, 관리자에게 문의하세요.',
                        icon: 'error',
                        button: false
                    }).then(() => {
                        window.location = '/';
                    });
                }
            });
        },
        searchKeyword() {
            const effect = document.getElementById('header-search-effect');
            const keywordInput = document.getElementById('header-search-input');
            const icon = document.getElementById('header-search-icon');
            if (effect.classList.contains('open')) {
                // search function trigger
                this.setSearchConditionTitle({
                    title: keywordInput.value
                });
                this.getMovieByConditions();
                effect.classList.remove('open');
                icon.classList.remove('open');
                keywordInput.value = '';
                this.$router.push('/movie/search');
            } else {
                effect.classList.add('open');
                icon.classList.add('open');
                keywordInput.focus();
            }
        }
    }
};
</script>

<style lang="scss" scoped>

$search-bg-color: transparent;
$icon-color: #e50914;
$transition: all .5s ease;

//variables
$background-purple: #EEEEEE;
$subtle-white: #f9f9f9;
$subtle-grey: #f2f2f2;
$masked-grey: #333;
$blue: #F03861;

$open-sans: 'Open Sans', sans-serif;

#header{
    top: 0;
    left: 0;
    position: fixed;
    width: 100%;
    height: 10vh;
    padding: 0 50px;
    background-position: right bottom;
    z-index: 100;
    color: transparent;
    transition: transform 1s ease, background-position 5s ease;
    -webkit-transition: -webkit-transform 1s ease, background-position 2s;
    transform:translate(0,0);
    -webkit-transform:translate(0,0);
    -moz-transform:translate(0,0);
    -ms-transform:translate(0,0);
    -o-transform:translate(0,0);
    .wrapper{
        padding: 0;
        margin: auto 0;
        height: 100%;
    }
    .menu-font{
        font-size: 1.2em;
        color: white;
        text-transform: uppercase;
    }
    .log-font{
        font-size: 2.5em;
        color: #e50914;
        font-weight: bold;
        letter-spacing: -1px;
        text-shadow: 1px 1px 1px black;
    }

    .search, .search-box, .search-button, .search-icon {
        box-sizing: border-box;
    }
    .search {
        width: 420px;
        height: 40px;
        float: right;
        background-color: $search-bg-color;
        position: relative;
        overflow: hidden;
        transition: $transition;

    }

    .search-box {
        width: 100%;
        height: 100%;
        box-shadow: none;
        border: none;
        background: transparent;
        color: white;
        position: absolute;
        top: 0;
        left: 0;
        padding-left: 10px;
        font-size: 1.2em;
        opacity: 0;
        transition: all 1s ease;
        &:focus {
            outline: none;
            opacity: 1;
        }
    }

    .search-effect{
        position: relative;
        width: 380px;
        height: 100%;
        // background: #221f1f;
        background: transparent;
        transition: $transition;
        z-index: 10;

        &:after {
            content: '';
            display: block;
            width: 3px;
            height: 100%;
            position: absolute;
            right: 0;
            background-color: $icon-color;
            transition: $transition;
        }

        &.open{
            width: 3px;
        }
    }


    .search-button {
        width: 30px;
        height: 30px;
        display: block;
        position: absolute;
        right: 5px;
        top: 0;
        padding-top: 5px;
        cursor: pointer;
    }

    .search-icon {
        width: 25px;
        height: 25px;
        border-radius: 25px;
        border: 3px solid $icon-color;
        display: block;
        position: relative;
        margin-left: 5px;
        transition: $transition;
        &:before {
            content: '';
            width: 3px;
            height: 5px;
            position: absolute;
            right: -2px;
            top: 17px;
            display: block;
            background-color: $icon-color;
            transform: rotate(-45deg);
            transition: $transition;
        }
        &:after {
            content: '';
            width: 3px;
            height: 8px;
            position: absolute;
            right: -5px;
            top: 19px;
            display: block;
            background-color: $icon-color;
            transform: rotate(-45deg);
            transition: $transition;
        }
        &.open {
            width: 30px;
            height: 30px;
            border-radius: 30px;
            &:before {
            transform: rotate(52deg);
            right: 10px;
            top: 10px;
            height: 10px;
            }
            &:after {
            transform: rotate(-230deg);
            right: 10px;
            top: 5px;
            height: 10px;
            }
        }
    }
}

.btn-link:link {
    color: transparent;
}

.dropdown {
    position: relative;
    display: inline-block;
}


.dropdown-content {
    display: none;
    position: absolute;
    background-color: #221f1f;
    min-width: 110px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 20;
    -webkit-animation-name: dropdown-animation;
    -webkit-animation-duration: 1s;
    animation-name: dropdown-animation;
    animation-duration: 1s;
}

@-webkit-keyframes dropdown-animation {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes dropdown-animation {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

.dropdown-content a {
    color: white;
    padding: 10px 16px;
    text-decoration: none;
    display: block;
    font-size: 1em;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.dropdown-content a:hover {
    color: white;
}

.dropdown:hover .dropdown-content{
    display: block;
}

.genre-btn{
    position: relative;
    height: 50px;
    .label{
        color: white;
        font-size: 0.9em;
    }
    .overlay{
        position: absolute;
        z-index: 20;
        background-color: black;
        opacity: 0.9;
        top: 1.8em;
        left: 0px;
        width: 550px;
        padding: 15px;
        color: white;
        display: none;

        .category-wrapper{
            height: 100%;
            text-align: left;
            padding: 0px 20px 0px 10px;
            font-size: 1.2em;
            font-weight: bold;
            .category{
                width: 100%;
                margin: 0 0 10px 0;
                float: none;

                &:active{
                    text-decoration: underline;
                }
            }
        }
        .genres-wrapper{
            height: 100%;
            width: 100%;
            text-align: center;
            margin: 0px 10px;
            .genre-row{
                margin: 0 0 5px 0;
                text-align: left;
                .genre{
                    font-size: 1em;
                    margin: 0 15px 5px 0;
                    display: inline-block;
                    width: 33%;
                }
            }
        }
    }
    &:hover{
       .overlay{
           display: flex;
       }
    }
}

</style>
