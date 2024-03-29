<template>
    <v-container
        class="section"
        fluid
        pa-0
        ma-0
    >
        <v-row
            id="personalized-section"
            justify="center"
            class="title"
        >
            <v-col
                sm="8"
                xs="12"
            >
                <AnimateWhenVisible name="fadeDown">
                    <span
                        key="span1"
                        class="section-title deepshadow title-family"
                    >Personalized</span>
                    <span
                        key="span2"
                        class="section-content content-family"
                    >We provide best movies for you</span>
                </AnimateWhenVisible>
            </v-col>
        </v-row>
        <v-row
            id="slider-container"
            justify="start"
            align="end"
            class="slider-container"
        >
            <v-col style="padding: 0;">
                <AnimateWhenVisible name="fade">
                    <div style="position: relative;">
                        <div
                            class="btn prev"
                            @click="movePrevPage()"
                        />
                        <div
                            class="btn next"
                            @click="moveNextPage()"
                        />
                        <div
                            v-for="(movie, index) in currentMovies"
                            :key="'personalized' + movie.id + index"
                            class="slider"
                        >
                            <v-img
                                class="slider-img"
                                :src="movie.backdrop_path | imagePath"
                            />
                            <div
                                class="slider-overlay"
                            >
                                <div class="position: relative;">
                                    <div class="portfolio-item__info">
                                        <h3
                                            class="portfolio-item__header"
                                            @click.stop="viewMovie(movie.id)"
                                        >
                                            {{ movie.title }}<span>({{ movie.release_date | extractYear }})</span>
                                        </h3>
                                        <h4 class="portfolio-item__inform">
                                            {{ movie.genres | genreConcat }}
                                        </h4>
                                        <h4
                                            id="overview-content"
                                            class="portfolio-item__content"
                                        >
                                            {{ movie.overview }}
                                        </h4>
                                        <div class="portfolio-item__links">
                                            <div class="portfolio-item__link-block">
                                                <a
                                                    class="portfolio-item__link"
                                                    href="#movie-detail"
                                                    title="Link Title"
                                                    @click.stop="chooseDetail(index)"
                                                >
                                                    <i class="material-icons">keyboard_arrow_down</i>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </AnimateWhenVisible>
            </v-col>
        </v-row>
        <v-row
            id="movie-detail-row"
        >
            <MovieDetail
                :visible="visible"
                :pmovie="personalMovies[calcSelectedIndex]"
                :close="closeMovieDetail"
                :rating="0"
                :ratingWord="'이미 본 작품인가요?'"
            />
        </v-row>
    </v-container>
</template>

<script>
import $ from 'jquery';
import { createNamespacedHelpers } from 'vuex';
import MovieDetail from '@/components/movie/MovieDetail.vue';

const { mapState } = createNamespacedHelpers('users');
const movieMapActions = createNamespacedHelpers('movies').mapActions;
const movieMapState = createNamespacedHelpers('movies').mapState;

export default {
    components: {
        MovieDetail
    },
    filters: {
        imagePath(value) {
            return value === '' ? '/static/img/commingsoon.jpg' : value;
        },
        genreConcat(list) {
            return list.join(' | ');
        },
        extractYear(str) {
            return (new Date(str)).getFullYear();
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
            outlined: 'false',
            showCount: 0,
            currentIndex: 0,
            currentPage: 0,
            maxPage: 2,
            selectedIndex: 0,
            visible: false,
            isloaded: false,
            sliderWidth: 355,
            innerWidth: 0
        };
    },
    computed: {
        ...mapState(['user']),
        ...movieMapState(['personalMovies', 'rateAdditionalMovies']),
        currentMovies() {
            const start = this.currentIndex;
            const end = this.currentIndex + this.showCount;
            // console.log(start, end);
            let result = [];
            if (end >= this.personalMovies.length) {
                result = result.concat(this.personalMovies.slice(start));
                // console.log(result);
                result = result.concat(this.personalMovies.slice(0, end - this.personalMovies.length));
                // console.log(result);
            } else {
                result = result.concat(this.personalMovies.slice(start, end));
            }
            return result;
        },
        calcSelectedIndex() {
            return (this.selectedIndex + this.currentIndex) % this.personalMovies.length;
        },
        getUserPK() {
            if (this.user) {
                return this.user;
            }
            return null;
        },
        getStyle() {
            return {
                left: (this.innerWidth - 40)
            };
        },
        getRateAdditionalMovies() {
            return this.rateAdditionalMovies;
        }
    },
    watch: {
        // eslint-disable-next-line
        getUserPK: function (user) {
            if (user) {
                this.$log.debug('RecommendMovies.vue getUserPK watch', user);
                this.setLoaded(false);
                this.getMoviesByPersonal(user.id).then(() => {
                    this.$log.debug('RecommendMovies.vue getUserPK watch response');
                    this.setLoaded(true);
                });
            }
        },
        // eslint-disable-next-line
        getRateAdditionalMovies: function (val) {
            if (val) {
                this.setLoaded(false);
                this.getMoviesByPersonal(this.user.id).then(() => {
                    this.$log.debug('RecommendMovies.vue getUserPK watch response');
                    this.setLoaded(true);
                });
            }
        }
    },
    mounted() {
        this.$nextTick(() => {
            if (this.user && this.currentMovies.length === 0) {
                this.$log.debug('RecommendMovies.vue nextTick');
                this.setLoaded(false);
                this.getMoviesByPersonal(this.getUserPK.id).then(() => {
                    this.$log.debug('RecommendMovies.vue getMoviesByPersonal response');
                    this.setLoaded(true);
                });
            }
            this.loadSliderWidth();
            window.addEventListener('resize', () => {
                this.loadSliderWidth();
            });
        });
    },
    methods: {
        ...movieMapActions(['getMoviesByPersonal', 'addMovieView']),
        loadSliderWidth() {
            // const { innerWidth } = window;
            this.innerWidth = screen.width;
            this.$log.debug('RecoommendMovies.vue loadSliderWidth innerWidth', this.innerWidth);
            // const ratio = innerWidth / this.sliderWidth;
            // if (ratio <= 1.1) {
            //     this.showCount = 0;
            // } else {
            this.showCount = Math.ceil(this.innerWidth / this.sliderWidth, 10);
            // }
            this.currentPage = 0;
            this.currentIndex = 0;
            if (this.showCount === 0) {
                this.showCount = 1;
            }
            this.maxPage = Math.ceil(this.personalMovies.length / this.showCount);
            if (this.personalMovies.length === this.showCount && this.maxPage === 1) {
                this.maxPage += 1;
            }
        },
        moveNextPage() {
            this.currentIndex = this.currentIndex + this.showCount - 1;
            if (this.personalMovies.length <= this.currentIndex) {
                this.currentIndex = this.currentIndex - this.personalMovies.length;
            }
        },
        movePrevPage() {
            this.currentIndex = this.currentIndex - this.showCount + 1;
            if (this.currentIndex < 0) {
                this.currentIndex = this.personalMovies.length + this.currentIndex;
            }
        },
        chooseDetail(idx) {
            this.selectedIndex = idx;
            this.visible = !this.visible;
        },
        closeMovieDetail() {
            this.visible = false;
        },
        viewMovie(movieId) {
            this.addMovieView(movieId);
            this.$router.push(`/movies/detail/${movieId}`);
        }
    }
};
</script>


<style lang="scss" scoped>

@import '@/style/variables';
@import '@/style/font.scss';

$portfolio-item-info-offset: 0px;

$portfolio-link-dimensions: 35px;
$portfolio-link-offset: 10px;
$accent-theme-color2: #8D909B;
$light-theme-color: #fff;

$slider-width: 355px;
$slider-height: 200px;
$slider-scale: 1.3;
$button-height: 200px;

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

.section{
    min-height: 500px;
    background-color:transparent;
    color: $text-color;
    margin-right: 0px;
    margin-left: 0px;
}

.title{
    height: 100px;
    color: $text-color;
    padding-top: 50px;
    margin-bottom: 30px;
}

.slider-container {
    padding-top: 50px;
    display: relative;
    overflow: hidden;
    width: 200vw;
    // margin-bottom: 20px;
}

.btn{
    width: 40px;
    height: scale-value($button-height, 1);
    background: rgba(0,0,0,0.7);
    position: absolute;
    top: 0;
    z-index: 1000;
    &.prev{
        left: 0;
    }
    &.next{
        left: 100vw;
        transform: translateX(-50%);
    }
}

.slider{
    width: scale-value($slider-width, 1);
    height: scale-value($slider-height, 1);
    float: left;
    margin: 0;
    padding: 0;
    object-position: bottom;
    display: block;
    cursor: pointer;
    -webkit-transition: width .5s, height .5s, transform .5s ease; /* For Safari 3.1 to 6.0 */
    transition: width .5s, height .5s, transform .5s ease;
    transform: translateY(0%);
}


.sliderEnd{
    display: relative;
    width: scale-value($slider-width, 1);
    height: scale-value($slider-height, 1);
    float: left;
    margin: 0;
    padding: 0;
    object-fit: fill;
    object-position: bottom;
    display:block;
}


.slider-img {
    width: 100%;
    height: 100%;
}

.slider-overlay{
    width: 100%;
    height: 100%;
    transition: .5s ease;
    visibility: hidden;
    position: absolute;
    top: 0%;
    left: 0%;
    pointer-events: none;
}

.detail-container{
    position: absolute;
    left: 0%;
}

.section-title {
    font-size: 2.5em;
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
    position: absolute;
    width: 100%;
    margin-top: 10px;
}


.portfolio-item__info {
    @include position-absolute($top: $portfolio-item-info-offset,
        $left: $portfolio-item-info-offset);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 25px 20px 0px 20px;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0, .7);
}

.portfolio-item__header {
    position: relative;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 1.8em;
    line-height: 1em;
    span {
        color: $text-gray-color;
        font-size: 0.8em;
    }

    &:hover{
        color: darkslategray;
    }
}

.portfolio-item__inform {
    font-size: 1em;
    max-height: 50px;
    color: $accent-theme-color2;
    margin-bottom: 10px;
}

.portfolio-item__content {
    font-size: 1em;
    height: 150px;
    color: white;
    margin-bottom: 15px;
    overflow-y: scroll;
}

.portfolio-item__links {
    display: flex;
    margin: 0 auto;
    padding-bottom: 10px;
    visibility: hidden;
}

.portfolio-item__link-block {
   position: relative;
   width: $portfolio-link-dimensions;
   height: $portfolio-link-dimensions;
   margin-right: $portfolio-link-offset;

  &:last-child {
    margin-right: 0;
  }
}

.portfolio-item__link {
  @include transition-mix;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: $light-theme-color;
  text-decoration: none;
  border-radius: 50%;

  &:hover {
    color: $light-theme-color;

    background-color: $light-theme-color;
  }
}

/* EFFECT #1 STYLES */
.portfolio-item--eff1 {

  .portfolio-item__info {
    transform: scale(1.1);
    opacity: 0;
  }

  .portfolio-item__header {
    top: -10px;
    opacity: 0;

    &:after {
        transform: scaleX(0);
    }
  }

  .portfolio-item__link-block {
    top: 20px;

    opacity: 0;
  }
}

.portfolio-item--eff1:hover {

  .portfolio-item__info {
    @include transition-mix($duration: .4s);

    transform: scale(1);
    opacity: 1;
  }

  .portfolio-item__header {
    @include transition-mix($delay: .45s);

    top: 0;
    opacity: 1;

  }

  .portfolio-item__link-block {
    top: 0;
    opacity: 1;

    &:first-child {
      @include transition-mix($delay: .85s);
    }

    &:nth-child(2) {
      @include transition-mix($delay: .95s);
    }
  }
}


@media (max-width: $small-breakpoint){
    .slider:hover{
        .slider-img {
            opacity: 0.3;
        };
        .slider-overlay {
            visibility: visible;
            pointer-events: auto;
            opacity: 1;
        };
    }
}

@media (min-width: $small-breakpoint) and (max-width: $medium-breakpoint){
    .slider:hover{
        width: scale-value($slider-width, 1.2);
        height: scale-value($slider-height, 1.2);
        transform: translateY(-5%);
        .slider-img {
            opacity: 0.3;
        };
        .slider-overlay {
            opacity: 1;
            width: scale-value($slider-width, 1.2);
            height: scale-value($slider-height, 1.2);
            visibility: visible;
            pointer-events: auto;
        };
    }
}

@media (min-width: $medium-breakpoint) and (max-width: $large-breakpoint){
    .slider:hover{
        width: scale-value($slider-width, 1.3);
        height: scale-value($slider-height, 1.3);
        transform: translateY(-10%);
        .slider-img {
            opacity: 0.3;
        };
        .slider-overlay {
            opacity: 1;
            width: scale-value($slider-width, 1.3);
            height: scale-value($slider-height, 1.3);
            visibility: visible;
            pointer-events: auto;
        };
    }
    .btn{
            &.next{
            left: 100vw;
            transform: translateX(-40px);
        }
    }
}

@media (min-width: $large-breakpoint){
    .slider{
        width: scale-value($slider-width, 1.2);
        height: scale-value($slider-height, 1.2);
    }

    .btn{
        height: scale-value($button-height, 1.2);
    }

    .slider:hover{
        width: scale-value($slider-width, 1.4);
        height: scale-value($slider-height, 1.4);
        transform: translateY(-10%);
        .slider-img {
            opacity: 0.3;
        };
        .slider-overlay {
            opacity: 1;
            width: scale-value($slider-width, 1.4);
            height: scale-value($slider-height, 1.4);
            visibility: visible;
            pointer-events: auto;
        };
    }
    .btn{
            &.next{
            left: 100vw;
            transform: translateX(-40px);
        }
    }

    .portfolio-item__links {
        visibility: visible;
    }
}


#overview-content::-webkit-scrollbar-track
{
    box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    background-color: black;
}

#overview-content::-webkit-scrollbar
{
    width: 6px;
    background-color: black;
}

#overview-content::-webkit-scrollbar-thumb
{
background-color: black;
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
