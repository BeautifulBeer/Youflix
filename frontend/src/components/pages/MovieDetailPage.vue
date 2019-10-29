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
                cols="3"
            >
                <v-img
                    :src="getPoster"
                />
            </v-col>
            <v-col
                cols="8"
            >
                <v-row
                    class="label-row"
                >
                    <v-col
                        cols="8"
                    >
                        <v-row>
                            <v-col cols="12">
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
                                    {{ getMovie.production_companies[0] }} | {{ getMovie.runtime }}Min
                                </span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col
                        cols="4"
                    >
                        <v-row
                            justify="end"
                            align="center"
                        >
                            <v-col cols="10">
                                <div class="detail-rating">
                                    <AnimateWhenVisible name="fade">
                                        <div class="wrapper">
                                            <span class="label">
                                                예상별점
                                            </span>
                                            <span class="score">
                                                3.4
                                            </span>
                                        </div>
                                        <div class="wrapper">
                                            <span class="label">
                                                영화별점
                                            </span>
                                            <span class="score">
                                                3.2
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
                            <v-col cols="10">
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
                    <v-col cols="12">
                        <div class="detail-play">
                            <div class="detail-play-content">
                                <span>예고편 보기</span>
                                <i class="material-icons">play_circle_outline</i>
                            </div>
                        </div>
                    </v-col>
                </v-row>
                <v-row>
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
                <v-row>
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
            justify="center"
            align="center"
        >
            <v-col
                cols="10"
            >
                <span
                    class="detail-title title-family"
                >
                    Faculties
                </span>
            </v-col>
        </v-row>
        <v-row
            :style="getCrewStyle"
            class="slider-container"
        >
            <!-- <v-col
                align-self="center"
                style="padding: 0;"
            >
                <AnimateWhenVisible name="fade">
                    <div style="position: relative;"> -->
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
            </div>
                    <!-- </div>
                </AnimateWhenVisible>
            </v-col> -->
        </v-row>
        <v-row
            justify="center"
            align="center"
        >
            <v-col
                cols="10"
            >
                <span
                    class="detail-title title-family"
                >
                    Reviews
                </span>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapState, mapActions } = createNamespacedHelpers('movies');

export default {
    name: 'MovieDetailPage',
    filters: {
        profilePath(value) {
            const min = 0;
            const max = 2;
            const rand = Math.floor(Math.random() * (max - min)) + min;
            if (value && value !== '') {
                return value;
            }
            return `/static/img/no_profile_image${rand}.jpg`;
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
            ratingWord: '아직은 멀었지요',
            showCount: 0,
            currentIndex: 0,
            currentPage: 0,
            maxPage: 2,
            sliderWidth: 200,
            margin: 15
        };
    },
    computed: {
        ...mapState(['selectedMovie']),
        getMovie() {
            return this.selectedMovie.movie;
        },
        getCrews() {
            if (this.selectedMovie.crews) {
                return this.selectedMovie.crews;
            }
            return [];
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
            return '/static/img/no_image.jpg';
        },
        getPoster() {
            if (this.getMovie.poster_path) {
                return this.getMovie.poster_path;
            }
            return '/static/img/no_image.jpg';
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
            // console.log(start, end);
            let result = [];
            if (end >= this.getCrews.length) {
                result = result.concat(this.getCrews.slice(start));
                // console.log(result);
                result = result.concat(this.getCrews.slice(0, end - this.getCrews.length));
                // console.log(result);
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
        }
    },
    mounted() {
        this.$nextTick(() => {
            if (this.isEmpty) {
                this.getMovieById(this.id).then((ret) => {
                    if (ret) {
                        this.getMovieCrews(this.id).then(() => {
                            this.$forceUpdate();
                        });
                    } else {
                        this.$forceUpdate();
                    }
                });
            }
            this.loadSliderWidth();
            window.addEventListener('resize', () => {
                this.loadSliderWidth();
            });
        });
    },
    methods: {
        ...mapActions(['getMovieById', 'getMovieCrews']),
        back() {
            this.$router.go(-1);
        },
        loadSliderWidth() {
            const { innerWidth } = window;
            this.$log.debug('MovieDetailPage.vue loadSliderWidth innerWidth', innerWidth);
            this.showCount = parseInt(innerWidth / (this.sliderWidth + 15), 10) + 1;
            if (this.showCount >= this.getCrews.length) {
                this.showCount = this.getCrews.length;
            }
            this.currentPage = 0;
            if (this.showCount === 0) {
                this.showCount = 1;
            }
            this.maxPage = Math.ceil(this.getCrews.length / this.showCount);
        },
        moveNextPage() {
            this.currentIndex = this.currentIndex + this.showCount - 1;
            if (this.getCrews.length <= this.currentIndex) {
                this.currentIndex = this.currentIndex - this.getCrews.length;
            }
        },
        movePrevPage() {
            this.currentIndex = this.currentIndex - this.showCount + 1;
            if (this.currentIndex < 0) {
                this.currentIndex = this.getCrews.length + this.currentIndex;
            }
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
    -webkit-transition: width .5s, height .5s, transform .5s ease; /* For Safari 3.1 to 6.0 */
    transition: width .5s, height .5s, transform .5s ease;
    transform: translateY(0%);
    margin: 0px 15px 0px 0px;
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
