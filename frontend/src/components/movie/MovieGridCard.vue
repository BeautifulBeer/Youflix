<template>
    <AnimateWhenVisible name="fade">
        <div
            class="slider"
            @click="viewMovie()"
        >
            <v-img
                class="slider-img"
                :src="movie.backdrop_path | imagePath"
            />
            <div class="slider-overlay">
                <div class="position: relative;">
                    <div class="portfolio-item__info">
                        <h3 class="portfolio-item__header">
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
                    </div>
                </div>
            </div>
        </div>
    </AnimateWhenVisible>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapActions } = createNamespacedHelpers('users');

export default {
    filters: {
        genreConcat(list) {
            return list.join(' | ');
        },
        imagePath(value) {
            return value === '' ? '/static/img/no_image.jpg' : value;
        },
        extractYear(str) {
            return (new Date(str)).getFullYear();
        }
    },
    props: {
        movie: {
            type: Object,
            default: () => {}
        }
    },
    computed: {
        genresStr() {
            return this.movie.genres.join(' / ');
        }
    },
    methods: {
        ...mapActions(['addMovieView']),
        viewMovie() {
            this.addMovieView(this.movie.id);
            this.$router.push(`/movies/detail/${this.movie.id}`);
        }
    }
};
</script>

<style lang="scss" scoped>

@import '@/style/variables';

$portfolio-item-info-offset: 0px;

$portfolio-link-dimensions: 35px;
$portfolio-link-offset: 10px;
$accent-theme-color2: #8D909B;
$light-theme-color: #fff;

$slider-width: 340px;
$slider-height: 200px;

@function scale-value($value1, $value2) {
    @return $value1 * $value2;
}

//position absolute mixin
@mixin position-absolute ($top: null, $left: null, $right: null, $bottom: null) {
  position: absolute;
  top: $top;
  left: $left;
  right: $right;
  bottom: $bottom;
}


.slider{
    width: $slider-width;
    height: $slider-height;
    margin: 15px 10px 15px 10px;
    position: relative;
    transition: all 0.3s ease;
    -webkit-transition: all 0.3s ease;
    cursor: pointer;
}

.slider-img{
    width: 100%;
    height: 100%;
}

.slider-overlay{
    width: 100%;
    height: 100%;
    transition: .5s ease;
    opacity: 0;
    position: absolute;
    top: 0%;
    left: 0%;
}

.slider:hover{
    transform: scale(1.1);
    -webkit-transform: scale(1.1);
}

.slider:hover{
    .slider-img {
        opacity: 0.3;
    };
    .slider-overlay {
        opacity: 1;
    };
}

.portfolio-item__info {
  @include position-absolute($top: $portfolio-item-info-offset, $left: $portfolio-item-info-offset);
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
    font-size: 1.4em;
    line-height: 1em;
    color: white;
    span {
        color: gray;
        font-size: 0.8em;
    }

}

.portfolio-item__inform {
    font-size: 0.9em;
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

</style>
