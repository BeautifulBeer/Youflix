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
                    class="detail-background"
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
                                :color="chip_colors[index % chip_colors.length]"
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
                                v-for="(genre, index) in getMovie.genres"
                                :key="'MovieDetailPage' + genre + index"
                                class="genre-chip"
                                :color="chip_colors[index % chip_colors.length]"
                            >
                                {{ genre }}
                            </v-chip>
                        </div>
                    </div>
                </v-row>
            </v-col>
        </v-row>
        <v-row>
            ddd
        </v-row>
    </v-container>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapState, mapActions } = createNamespacedHelpers('movies');

export default {
    name: 'MovieDetailPage',
    props: {
        id: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            chip_colors: [
                'primary',
                'secondary',
                'red',
                'green',
                'yellow',
                'purple'
            ],
            rating: 0
        };
    },
    computed: {
        ...mapState(['selectedMovie']),
        getMovie() {
            return this.selectedMovie;
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
        }
    },
    mounted() {
        if (this.isEmpty) {
            this.getMovieById(this.id).then(() => {
                this.$forceUpdate();
            });
        }
    },
    methods: {
        ...mapActions(['getMovieById']),
        back() {
            this.$router.go(-1);
        }
    }
};
</script>

<style lang="scss" scoped>
@import "@/style/font.scss";
@import "@/style/variables.scss";

.content-wrapper{
    margin: 0px 50px 0px 50px;
    min-height: 90vh;
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

</style>
