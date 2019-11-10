<template>
    <v-container
        class="pa-2"
        fluid
        grid-list-md
    >
        <v-row style="height: 10vh;" />
        <v-row
            align="stretch"
            justify="center"
            class="content-wrapper"
        >
            <v-col
                cols="12"
                sm="3"
            >
                <v-img
                    :src="getPoster | posterPath"
                />
            </v-col>
            <v-col
                cols="12"
                sm="8"
            >
                <v-row
                    class="label-row"
                >
                    <v-col
                        cols="12"
                        sm="8"
                    >
                        <v-row>
                            <v-col
                                cols="12"
                            >
                                <span
                                    class="detail-title title-family"
                                >
                                    {{ getMovie.title }}
                                </span>
                            </v-col>
                            <v-col cols="12">
                                <span
                                    class="detail-feature content-family"
                                >
                                    {{ movieDetailInfo }}
                                </span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col
                        cols="12"
                        sm="4"
                    >
                        <v-row
                            justify="end"
                            align="center"
                        >
                            <v-col
                                sm="10"
                                cols="12"
                            >
                                <div class="detail-rating">
                                    <AnimateWhenVisible name="fade">
                                        <div class="wrapper">
                                            <span class="label">
                                                예상별점
                                            </span>
                                            <span class="score">
                                                {{ predictedScore | getPredictionScore }}
                                            </span>
                                        </div>
                                        <div class="wrapper">
                                            <span class="label">
                                                영화별점
                                            </span>
                                            <span class="score">
                                                {{ getMovie.vote_average | scoreConverter }}
                                            </span>
                                        </div>
                                    </AnimateWhenVisible>
                                </div>
                            </v-col>
                        </v-row>
                        <v-row
                            justify="end"
                            align="center"
                        >
                            <v-col
                                cols="12"
                                sm="10"
                            >
                                <span
                                    class="taste-word"
                                    style="color: white;"
                                >
                                    {{ ratingWord }}
                                </span>
                                <v-rating
                                    id="ratingStar"
                                    v-model="rating"
                                    dense
                                    color="white"
                                    background-color="white"
                                    half-increments
                                    hover
                                />
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <v-divider />
                <v-row>
                    <v-col cols="12">
                        <span
                            class="detail-content content-family"
                        >
                            {{ getMovie.overview }}
                        </span>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col
                        v-if="getMovie.video "
                        cols="12"
                    >
                        <div class="detail-play">
                            <div
                                class="detail-play-content"
                                @click="moveTrailerPage()"
                            >
                                <span>예고편 보기</span>
                                <i class="material-icons">play_circle_outline</i>
                            </div>
                        </div>
                    </v-col>
                </v-row>
                <v-row v-if="getMovie && getMovie.genres && getMovie.genres.length != 0">
                    <div class="label-wrapper">
                        <span class="label">
                            Genre
                        </span>
                        <div class="content">
                            <v-chip
                                v-for="(genre, index) in getMovie.genres"
                                :key="'MovieDetailPage' + genre + index"
                                class="genre-chip"
                                :color="genre_colors[index % genre_colors.length]"
                            >
                                {{ genre }}
                            </v-chip>
                        </div>
                    </div>
                </v-row>
                <v-row v-if="getMovie && getMovie.keywords && getMovie.keywords.length != 0">
                    <div class="label-wrapper">
                        <span class="label">
                            Keyword
                        </span>
                        <div class="content">
                            <v-chip
                                v-for="(keyword, index) in getMovie.keywords"
                                :key="'MovieDetailPage' + keyword + index"
                                class="genre-chip"
                                :color="keyword_colors[index % keyword_colors.length]"
                            >
                                {{ keyword }}
                            </v-chip>
                        </div>
                    </div>
                </v-row>
            </v-col>
        </v-row>
        <v-row
            v-show="!isMobile"
            justify="center"
            align="center"
        >
            <v-col
                cols="12"
                sm="10"
            >
                <span
                    class="detail-title title-family"
                >
                    Faculties
                </span>
            </v-col>
        </v-row>
        <v-row
            v-show="!isMobile"
            :style="getCrewStyle"
            class="slider-container"
        >
            <div
                v-if="maxPageFlag"
                class="btn prev"
                @click="movePrevPage()"
            />
            <div
                v-if="maxPageFlag"
                class="btn next"
                @click="moveNextPage()"
            />
            <div
                v-for="(crew, index) in currentCrews"
                :key="'personalized' + crew.id + index"
                class="slider"
            >
                <v-img
                    class="slider-img"
                    :src="crew.profile_path | profilePath"
                />
                <div
                    class="crew-overlay"
                >
                    <div
                        style="height: 30%"
                    />
                    <div
                        class="name"
                    >
                        <span>
                            {{ crew.name }}
                        </span>
                    </div>
                    <div
                        class="department"
                    >
                        {{ getFacultyInform(crew) }}
                    </div>
                </div>
            </div>
        </v-row>
    </v-container>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapState, mapActions } = createNamespacedHelpers('movies');
const userMapState = createNamespacedHelpers('users').mapState;

export default {
    name: 'MovieDetailPage',
    filters: {
        profilePath(value) {
            if (value && value !== '') {
                return value;
            }
            return '/static/img/no_profile.png';
        },
        posterPath(value) {
            if (value && value !== '') {
                return value;
            }
            return '/static/img/no_poster.png';
        },
        scoreConverter(value) {
            return (value / 2).toFixed(1);
        },
        getPredictionScore(value) {
            if (value === 0) {
                return '-';
            }
            return value.toFixed(1);
        }
    },
    props: {
        id: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            genre_colors: [
                '#E0FFFF',
                '#7CFC00',
                '#4B0082',
                '#40E0D0',
                '#FF6347',
                '#FFB6C1'
            ],
            keyword_colors: [
                '#FFB6C1',
                '#FF4500',
                '#FF00FF',
                '#8B4513',
                '#FFFF00',
                '#EE82EE'
            ],
            rating: 0,
            ratingWord: '평가해주세요',
            showCount: 0,
            currentIndex: 0,
            currentPage: 0,
            maxPage: 2,
            sliderWidth: 200,
            margin: 15,
            predictedScore: 0
        };
    },
    computed: {
        ...mapState(['selectedMovie']),
        ...userMapState(['user']),
        getUserEmail() {
            if (this.user) {
                return this.user.email;
            }
            return false;
        },
        getMovie() {
            return this.selectedMovie.movie;
        },
        getCrews() {
            let result = [];
            if (this.selectedMovie.faculties.casts) {
                result = result.concat(this.selectedMovie.faculties.casts);
            }
            if (this.selectedMovie.faculties.crews) {
                result = result.concat(this.selectedMovie.faculties.crews);
            }
            return result;
        },
        isEmpty() {
            if (this.getMovie && 'id' in this.getMovie && this.id === this.getMovie.id) {
                return false;
            }
            return true;
        },
        getMovieTrailer() {
            if (this.getMovie.video) {
                return this.getMovie.video;
            }
            if (this.getMovie.backdrop_path) {
                return this.getMovie.backdrop_path;
            }
            return '/static/img/commingsoon.jpg';
        },
        getPoster() {
            if (this.getMovie.poster_path) {
                return this.getMovie.poster_path;
            }
            return '/static/img/no_poster.png';
        },
        isVideo() {
            return this.getMovie.video !== '';
        },
        isPosterPath() {
            return this.getMovie.video
                && this.getMovie.backdrop_path
                && !this.getMovie.poster_path;
        },
        currentCrews() {
            const start = this.currentIndex;
            const end = this.currentIndex + this.showCount;
            let result = [];
            if (!this.getCrews && this.getCrews.length <= 0) {
                return result;
            }
            if (this.maxPage === 1) {
                return this.getCrews.slice(start, end);
            }
            if (this.getCrews && end >= this.getCrews.length) {
                result = result.concat(this.getCrews.slice(start));
                result = result.concat(this.getCrews.slice(0, end - this.getCrews.length));
            } else {
                result = result.concat(this.getCrews.slice(start, end));
            }
            return result;
        },
        getCrewStyle() {
            if (this.maxPage > 1) {
                return {
                    'justify-content': 'flex-start',
                    width: '200vw'
                };
            }
            return {
                'justify-content': 'center',
                width: '100vw'
            };
        },
        maxPageFlag() {
            return this.maxPage > 1;
        },
        getCompanies() {
            if ('production_companies' in this.getMovie) {
                return this.getMovie.production_companies;
            }
            return [];
        },
        movieDetailInfo() {
            let result = '';
            const companies = this.getCompanies;
            const { runtime } = this.getMovie;
            const time = (runtime === 0) ? '' : (String(runtime).concat('Min'));
            if (companies && companies.length > 0) {
                for (let i = 0; i < companies.length; i += 1) {
                    result += companies[i];
                    result += ', ';
                }
            }
            if (result === '') {
                return time;
            }
            if (time === '') {
                return '';
            }
            result.slice(0, result.length - 2);
            return result.concat(' | ', time);
        },
        isMobile() {
            const mobile = 600;
            const { innerWidth } = window;
            this.$log.debug('Window breakpoint isMobile()', innerWidth);
            if (innerWidth < mobile) {
                return true;
            }
            return false;
        }
    },
    watch: {
        // eslint-disable-next-line
        id: function(val) {
            this.$log.debug('MovieDetailPage.vue watch id', val);
            if (val && this.getMovie && this.getMovie.id !== val) {
                this.$log.debug('MovieDetailPage.vue watch id', val, this.getMovie);
                this.getMovieById(val).then((result) => {
                    this.$log.debug('MovieDetailPage.vue getMovieById response', this.user.email, val);
                    if (result) {
                        this.getMovieFaculties(val).then(() => {
                            this.$forceUpdate();
                        }).then(() => {
                            this.loadSliderWidth();
                        });
                    } else {
                        this.$forceUpdate();
                    }
                    this.getPrediction([this.user.email, this.id]).then((score) => {
                        if (score !== -1) {
                            this.predictedScore = score;
                        }
                        this.$forceUpdate();
                    });
                });
            }
        }
    },
    mounted() {
        this.$nextTick(() => {
            window.addEventListener('resize', () => {
                this.loadSliderWidth();
            });
            if (this.id && !Number.isNaN(this.id)) {
                this.getMovieById(this.id).then((result) => {
                    this.$log.debug('MovieDetailPage.vue getMovieById response', this.user.email, this.id);
                    if (result) {
                        this.getMovieFaculties(this.id).then(() => {
                            this.$forceUpdate();
                        }).then(() => {
                            this.loadSliderWidth();
                        });
                        this.getRatingForMovie(this.id).then((ret) => {
                            this.rating = ret;
                        });
                    } else {
                        this.$forceUpdate();
                    }
                    this.getPrediction([this.user.email, this.id]).then((score) => {
                        if (score !== -1) {
                            this.predictedScore = score;
                        }
                        this.$forceUpdate();
                    });
                });
            }
        });
    },
    methods: {
        ...mapActions(['getMovieById', 'getMovieFaculties', 'getPrediction', 'getRatingForMovie']),
        back() {
            this.$router.go(-1);
        },
        loadSliderWidth() {
            const { innerWidth } = screen.width;
            this.$log.debug('MovieDetailPage.vue loadSliderWidth innerWidth', innerWidth);
            this.showCount = Math.ceil(innerWidth / (this.sliderWidth + 15), 10);
            this.currentPage = 0;
            this.currentIndex = 0;
            if (this.showCount === 0) {
                this.showCount = 1;
            }
            this.maxPage = Math.ceil(this.getCrews.length / this.showCount);
            if (this.getCrews.length === this.showCount && this.maxPage === 1) {
                this.maxPage += 1;
            }
        },
        moveNextPage() {
            this.currentIndex = this.currentIndex + this.showCount - 1;
            if (this.getCrews && this.getCrews.length <= this.currentIndex) {
                this.currentIndex = this.currentIndex - this.getCrews.length;
            }
        },
        movePrevPage() {
            this.currentIndex = this.currentIndex - this.showCount + 1;
            if (this.getCrews && this.currentIndex < 0) {
                this.currentIndex = this.getCrews.length + this.currentIndex;
            }
        },
        moveTrailerPage() {
            window.open(`${this.getMovie.video}?autoplay=1`, '_blank');
        },
        getFacultyInform(obj) {
            if (obj.department) {
                return obj.department;
            }
            if (obj.character) {
                return obj.character;
            }
            return '';
        }
    }
};
</script>

<style lang="scss" scoped>
@import "@/style/font.scss";
@import "@/style/variables.scss";

$portfolio-item-info-offset: 0px;

$portfolio-link-dimensions: 35px;
$portfolio-link-offset: 10px;
$accent-theme-color2: #8D909B;
$light-theme-color: #fff;

$slider-width: 200px;
$slider-height: 284px;
$slider-scale: 1.3;
$button-height: 284px;
$button-width: 50px;

@function scale-value($value1, $value2) {
    @return $value1 * $value2;
}


//transitions mixin
@mixin transition-mix($property: all, $duration: 0.2s, $timing: linear, $delay: 0s) {
  transition-property: $property;
  transition-duration: $duration;
  transition-timing-function: $timing;
  transition-delay: $delay;
}

//position absolute mixin
@mixin position-absolute ($top: null, $left: null, $right: null, $bottom: null) {
  position: absolute;
  top: $top;
  left: $left;
  right: $right;
  bottom: $bottom;
}

.content-wrapper{
    margin: 0px 50px 0px 50px;
    // position: relative;
}

.detail-background{
    width: 400px;
}

.detail-title{
    color: $text-color;
    font-size: 2.5em;
    font-weight: bold;
}

.detail-feature{
    color: $text-gray-color;
    font-size: 1.2em;
}

.detail-content{
    color: $text-color;
}

.label-wrapper{
    margin: 10px 0;
    padding-left: 1em;
    color: white;
    .label{
        font-size: 1.2em;
        font-weight: bold;
        letter-spacing: 1px;
        display: block;
        text-transform: capitalize;
        margin-bottom: 5px;
    }
    span{
        margin-right: 5px;
    }
    // .content{
    //     color: gray;
    //     font-size: 1.2em;
    //     padding-left: 1em;
    // }
    .overview{
        color: white;
    }
    .genre-chip{
        margin: 10px;
        font-size: 1.2em;
    }
}

.detail-rating {
    height: 40px;
    font-size: 1.2em;
    font-weight: bold;
    .wrapper{
        width: 130px;
        height: 40px;
        position: relative;
        background-color: white;
        border: 3px solid white;
        margin-right: 20px;
        float: left;
        .label{
            background-color: black;
            position:absolute;
            padding-top: 5px;
            z-index: 25;
            left: 0%;
            width: 70%;
            height: 100%;
            top: 50%;
            color: white;
            transform: translateY(-50%);
            text-align: center;
            vertical-align: middle;
            text-transform: uppercase;
        }
        .score{
            text-align: center;
            background-color: white;
            position:absolute;
            z-index: 20;
            width: 25%;
            top: 50%;
            right: 0%;
            color: black;
            transform: translateY(-50%);
        }
    }

    &:after{
        clear: both;
    }
}

.detail-image {
    // width: 500px;
    width: 880px;
    height: 500px;
    box-sizing: border-box;
}

.detail-content {
    padding-left: 50px;
    // text-transform: ;
    // border-left: 1px solid white;
}


.detail-play{
    position: relative;
    min-height: 50px;
    margin: 10px;
}

.detail-play-content{
    position: relative;
    min-height: 60px;
    max-width: 200px;
    box-sizing: border-box;
    background-color: #e50914;
    color: white;
    cursor: pointer;

    span {
        position: absolute;
        top: 50%;
        right: 3.2em;
        font-size: 1.3em;
        transform: translateY(-50%);
    };
    i {
        position: absolute;
        min-height: 50px;
        font-size: 3em;
        right: 0.2em;
        top: 50%;
        transform: translateY(-50%);
    };
}

.slider-container {
    margin-top: 50px;
    position: relative;
    overflow: hidden;
    margin-bottom: 50px;
}

.slider{
    width: scale-value($slider-width, 1);
    height: scale-value($slider-height, 1);
    margin: 0;
    padding: 0;
    object-fit: fill;
    object-position: bottom;
    display: inline-block;
    position: relative;
    transform: translateY(0%);
    margin: 0px 15px 0px 0px;

    .crew-overlay{
        position: absolute;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.9);
        top: 200%;
        left: 0;
        opacity: 0;
        color: white;
        text-align: center;
        -webkit-transition: all .5s ease; /* For Safari 3.1 to 6.0 */
        transition: all .5s ease;
        // transform: translateY(0%);
        .name{
            font-size: 1.5em;
        }

        .department{
            font-size: 1.2em;
            color: gray;
        }
    }

    &:hover{
        .crew-overlay{
            opacity: 1;
            transform: translateY(-200%);
        }
    }
}


.slider-img {
    width: 100%;
    height: 100%;
}


.btn{
    width: $button-width;
    height: scale-value($button-height, 1);
    background: rgba(0,0,0,0.3);
    position: absolute;
    top: 0;
    z-index: 1000;
    &.prev{
        left: 0;
    }
    &.next{
        right: 50%;
        transform: translateX(-$scroll-width);
    }
}
</style>
