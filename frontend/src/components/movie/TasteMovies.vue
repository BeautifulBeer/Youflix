<template>
    <v-container
        class="section"
        fluid
    >
        <v-row
            justify="center"
            class="title"
        >
            <v-col sm="8">
                <AnimateWhenVisible name="fadeDown">
                    <span
                        key="span1"
                        class="section-title deepshadow title-family"
                    >Feature Based</span>
                    <span
                        key="span2"
                        class="section-content content-family"
                    >원하시는 특징을 선택해서 추천받아보세요!</span>
                </AnimateWhenVisible>
            </v-col>
        </v-row>
        <v-row
            justify="center"
            class="movie-category"
        >
            <AnimateWhenVisible name="fadeUp">
                <a
                    v-for="genre in getUserTaste"
                    :key="'genreMoviesLabel' + genre"
                    class="effect-4 content-family"
                    @click="selectGenre(genre)"
                >
                    {{ genre }}
                </a>
            </AnimateWhenVisible>
        </v-row>
        <v-row justify="center">
            <v-col
                cols="10"
                class="movie-slider"
            >
                <a
                    class="arrow left"
                    @click="movePrevPage()"
                />
                <div
                    v-for="(movie, index) in currentMovies"
                    :key="'personalized' + movie.id + index"
                    class="tile"
                >
                    <v-img
                        class="tile-img"
                        :src="movie.poster_path | imagePath"
                        @click="viewMovie(movie.id)"
                    />
                </div>
                <a
                    class="arrow right"
                    @click="moveNextPage()"
                />
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const userMapState = createNamespacedHelpers('users').mapState;
const userMapActions = createNamespacedHelpers('users').mapActions;
const movieMapActions = createNamespacedHelpers('movies').mapActions;
const movieMapState = createNamespacedHelpers('movies').mapState;
const movieMapMutation = createNamespacedHelpers('movies').mapMutations;

export default {
    name: 'GenreMovies',
    filters: {
        imagePath(value) {
            return value === '' ? '/static/img/no_poster.png' : value;
        }
    },
    props: {
        setLoaded: {
            type: Function,
            default: null
        }
    },
    data() {
        return {
            selectedGenre: undefined,
            currentIndex: 0,
            currentPage: 0,
            showCount: 6,
            maxPage: 2,
            selectedIndex: 0,
            totalCnt: 20
        };
    },
    computed: {
        ...userMapState(['user']),
        ...movieMapState(['featureMovies']),
        getUserTaste() {
            return ['Director/Actor', 'Director', 'Actor'];
        },
        currentMovies() {
            if (this.getGenreMovies.length === 0) {
                return [];
            }
            const start = this.currentIndex;
            const end = this.currentIndex + this.showCount;
            let result = [];
            if (end >= this.getGenreMovies.length) {
                result = result.concat(this.getGenreMovies.slice(start));
                result = result.concat(
                    this.getGenreMovies.slice(0, end - this.getGenreMovies.length)
                );
            } else {
                result = result.concat(this.getGenreMovies.slice(start, end));
            }
            return result;
        },
        getGenreMovies() {
            if (!(this.selectedGenre in this.featureMovies)) {
                return [];
            }
            return this.featureMovies[this.selectedGenre];
        },
        getUser() {
            if (this.user) {
                return this.user;
            }
            return false;
        }
    },
    mounted() {
        if (this.currentMovies.length === 0) {
            this.$log.debug(this.getUserTaste);
            this.setLoaded(false);

            if (this.user === null) {
                this.getUserBySession(localStorage.getItem('token')).then(() => {
                    if (this.user == null) {
                        swal({
                            title: 'Session Timeout',
                            text: 'Session이 만료되었습니다. Login Page로 돌아갑니다.',
                            icon: 'error',
                            button: false
                        }).then(() => {
                            this.$router.push('/login');
                            this.setIsLoaded(true);
                        });
                    } else {
                        this.getContentBasedByFeatures(
                            [this.getUserTaste, this.user.email]
                        ).then((ret) => {
                            this.selectGenre(ret);
                        }).then((() => {
                            this.setLoaded(true);
                        }));
                    }
                });
            } else {
                this.getContentBasedByFeatures([this.getUserTaste, this.user.email]).then((ret) => {
                    this.selectGenre(ret);
                }).then((() => {
                    this.setLoaded(true);
                }));
            }
        }
        this.setSlider();
        window.addEventListener('resize', () => {
            this.setSlider();
        });
    },
    methods: {
        ...movieMapActions(['getContentBasedByFeatures', 'addMovieView']),
        ...userMapActions(['getUserBySession']),
        ...movieMapMutation(['setIsLoaded']),
        selectGenre(genre) {
            this.selectedGenre = genre;
            this.currentIndex = 0;
            this.currentPage = 0;
            this.selectedIndex = 0;
        },
        moveNextPage() {
            this.currentIndex = this.currentIndex + this.showCount;
            if (this.getGenreMovies.length <= this.currentIndex) {
                this.currentIndex = this.currentIndex - this.getGenreMovies.length;
            }
        },
        movePrevPage() {
            this.currentIndex = this.currentIndex - this.showCount;
            if (this.currentIndex < 0) {
                this.currentIndex = this.getGenreMovies.length + this.currentIndex;
            }
        },
        viewMovie(id) {
            this.addMovieView(id);
            this.$router.push(`/movies/detail/${id}`);
        },
        setSlider() {
            const innerWidth = screen.width;
            let result = 1;
            if (innerWidth > 1600) {
                result = 6;
            } else if (innerWidth > 1400) {
                result = 5;
            } else if (innerWidth > 1200) {
                result = 4;
            } else if (innerWidth > 1000) {
                result = 3;
            } else if (innerWidth > 800) {
                result = 2;
            }
            this.showCount = result;
        }
    }
};
</script>

<style lang="scss" scoped>
@import "@/style/variables.scss";
@import "@/style/font.scss";

.section{
    height: 600px;
    background-color:transparent;
    color: $text-color;
}

.title{
    height: 100px;
    color: $text-color;
    margin-bottom: 20px;
    padding-top: 30px;
}

.section-title {
    text-align: left;
    text-transform: uppercase;
    text-rendering: optimizeLegibility;
    display: block;


    &.deepshadow {
    color: $text-color;
    background-color: $background-color;
    letter-spacing: .1em;
    text-shadow:
        0 5px 7px rgba(0, 0, 0, 0.9);
    }

}


.section-content{
    color: $text-gray-color;
    text-align: left;
    text-transform: uppercase;
    letter-spacing: .35em;
    font-size: 1.2em;
    position: absolute;
    width: 100%;
    margin-top: 10px;
}

.movie-slider{
    display: flex;
    position: relative;
    justify-content: center;
}

.tile{
    width: 200px;
    height: 300px;
    margin: 0 7px;
    object-fit: fill;
    object-position: top;
    display: block;
    position: relative;
    transition: all 0.3s ease;
}

.tile-img {
    position: absolute;
    top: 0;
    width: 200px;
    height: 300px;
}


.arrow {
    position: absolute;
    top: 50%;
    width: 3vmin;
    height: 3vmin;
    background: transparent;
    border-top: 1vmin solid white;
    border-right: 1vmin solid white;
    box-shadow: 0 0 0 lightgray;
    transition: all 200ms ease;

    &.left {
        left: 0;
        transform: translate3d(0,-50%,0) rotate(-135deg);
    }

    &.right {
        right: 0;
        transform: translate3d(0,-50%,0) rotate(45deg);
    }

    &:hover {
        border-color: orange;
        box-shadow: 0.5vmin -0.5vmin 0 white;
    }

    &:before { // for better hit area
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-40%,-60%) rotate(45deg);
        width: 200%;
        height: 200%;
    }
}

.movie-category a {
    text-decoration: none;
    margin: 0 10px;
    color: $text-gray-color;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.effect-4 {
  padding: 10px;
  display: inline-block;
  overflow: hidden;
  &:before, &:after {
    left: 0;
    width: 100%;
    height: 2px;
    background: $text-color;
  }
  &:before {
    bottom: 0;
    transform:  translateX(-100%);
  }
  &:after {
    top: 0;
    transform:  translateX(100%);
  }
  &:hover:before, &:hover:after {
    transform:  translateX(0);
  }
}

a, a > span {
  position: relative;
  color: inherit;
  text-decoration: none;
  line-height: 24px;
  &:before, &:after {
    content: '';
    position: absolute;
    transition: transform .5s ease;
  }
}

.movie-category{
    padding-top: 20px;
}

.tile:hover {
  transform: scale(1.1);
  z-index: 10;
  cursor: pointer;
}

@media (max-width: map-get($breakpoints, mobile)) {
    .section-title {
        font-size: 1.5em;
        margin-top: 0px;
    }

    .section-content{
        font-size: 0.8em;
        word-spacing: 1px;
        line-height: 1.2em;
    }

    .title{
        padding-left: 20px;
    }
}
</style>
