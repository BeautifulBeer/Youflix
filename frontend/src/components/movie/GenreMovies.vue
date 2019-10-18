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
                <!-- <transition-group name="fade" tag="span" class="span-group"> -->
                <AnimateWhenVisible name="fadeDown">
                    <span
                        key="span1"
                        class="section-title deepshadow"
                    >Genres</span>
                    <span
                        key="span2"
                        class="section-content"
                    >Top movies for each genre</span>
                <!-- </transition-group> -->
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
                    class="effect-4"
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
                    @click="movePrevPage()"
                    class="arrow left"
                />
                <div
                    v-for="(movie, index) in currentMovies"
                    :key="'personalized' + movie.id + index"
                    class="tile"
                >
                    <v-img
                        class="tile-img"
                        :src="movie.poster_path"
                        @click="movieDetail()"
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
import axios from 'axios';

const { mapState } = createNamespacedHelpers('users');

export default {
    name: 'GenreMovies',
    data() {
        return {
            movies: {},
            selectedGenre: undefined,
            currentIndex: 0,
            currentPage: 0,
            showCount: 6,
            maxPage: 2,
            selectedIndex: 0,
            totalCnt: 20
        };
    },
    watch: {
        getUserTaste(val) {
            if (val) {
                let promises = [];
                this.getUserTaste.forEach((genre) => {
                    promises.push(axios.get('/api/movies/', {
                        params: {
                            genres: genre,
                            page: 1
                        }
                    }));
                });
                Promise.all(promises).then((responses) => {
                    for (let i = 0; i < this.getUserTaste.length; i += 1) {
                        this.movies[this.getUserTaste[i]] = responses[i].data;
                    }
                    this.selectGenre(this.getUserTaste[0]);
                });
            }
        }
    },
    mounted() {
        window.addEventListener('resize', () => {
            const windowWidth = window.innerWidth;
            let result = 2;
            if (windowWidth > 1600) {
                result = 6;
            } else if (windowWidth > 1400) {
                result = 5;
            } else if (windowWidth > 1200) {
                result = 4;
            } else if (windowWidth > 1000) {
                result = 3;
            }
            this.showCount = result;
        });
    },
    computed: {
        ...mapState(['user']),
        getUserTaste() {
            if (this.user) {
                return this.user.movie_taste ? this.user.movie_taste : [];
            }
            return [];
        },
        currentMovies() {
            if (this.genreMovies.length === 0) {
                return [];
            }
            const start = this.currentIndex;
            const end = this.currentIndex + this.showCount;
            // console.log(start, end);
            let result = [];
            if (end >= this.genreMovies.length) {
                result = result.concat(this.genreMovies.slice(start));
                // console.log(result);
                result = result.concat(this.genreMovies.slice(0, end - this.genreMovies.length));
                // console.log(result);
            } else {
                result = result.concat(this.genreMovies.slice(start, end));
            }
            return result;
        },
        genreMovies() {
            if (!(this.selectedGenre in this.movies)) {
                return [];
            }
            return this.movies[this.selectedGenre];
        }
    },
    methods: {
        selectGenre(genre) {
            this.selectedGenre = genre;
            this.currentIndex = 0;
            this.currentPage = 0;
            this.selectedIndex = 0;
        },
        moveNextPage() {
            this.currentIndex = this.currentIndex + this.showCount;
            if (this.genreMovies.length <= this.currentIndex) {
                this.currentIndex = this.currentIndex - this.genreMovies.length;
            }
        },
        movePrevPage() {
            this.currentIndex = this.currentIndex - this.showCount;
            if (this.currentIndex < 0) {
                this.currentIndex = this.genreMovies.length + this.currentIndex;
            }
        }
    }
};
</script>

<style lang="scss" scoped>

.section{
    height: 600px;
    background-color:transparent;
    color: white;
}

.title{
    height: 100px;
    color: white;
    margin-bottom: 20px;
    padding-top: 30px;
}

.section-title {
    font-family: "Avant Garde", Avantgarde, "Century Gothic", CenturyGothic, "AppleGothic", sans-serif;
    font-size: 45px;
    text-align: left;
    text-transform: uppercase;
    text-rendering: optimizeLegibility;
    display: block;


    &.deepshadow {
    color: #f5f5f1;
    background-color: #221f1f;
    letter-spacing: .1em;
    text-shadow:
        0 5px 7px rgba(0, 0, 0, 0.9);
    }

}


.section-content{
    font: 600 'Raleway', sans-serif;
    color: rgba(255,255,255,.6);
    text-align: left;
    text-transform: uppercase;
    letter-spacing: .35em;
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
    font: 600 'Raleway', sans-serif;
    color: rgba(245, 245, 241,.6);
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
    background: #f5f5f1;
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

</style>
