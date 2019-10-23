<template>
    <v-container
        class="pa-2"
        fluid
        grid-list-md
    >
        <v-row
            align="stretch"
            justify="start"
            class="content-wrapper"
        >
            <template v-if="!isEmpty">
                <v-col cols="6">
                    <v-row>
                        <div class="detail-title">
                            {{ getMovie.title }}
                        </div>
                    </v-row>
                    <v-row align="stretch">
                        <v-col>
                            <template v-if="isVideo">
                                <div
                                    class="video-container"
                                >
                                    <iframe
                                        :src="getMovieTrailer"
                                        frameborder="0"
                                        allowfullscreen
                                    />
                                </div>
                            </template>
                            <template v-else>
                                <div class="image-container">
                                    <v-img
                                        class="detail-image"
                                        :src="getMovieTrailer"
                                    />
                                </div>
                            </template>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col>
                    <v-row>
                        <div class="detail-title">
                            {{ getMovie.original_title }}
                        </div>
                    </v-row>
                    <v-row>
                        <div class="detail-rating">
                            <div class="wrapper">
                                <span class="label">
                                    영화평점
                                </span>
                                <span class="score">
                                    3.4
                                </span>
                            </div>
                        </div>
                        <div class="detail-rating">
                            <div class="wrapper">
                                <span class="label">
                                    예측평점
                                </span>
                                <span class="score">
                                    3.4
                                </span>
                            </div>
                        </div>
                    </v-row>
                    <v-row>
                        <div>
                            <v-chip
                                v-for="(genre, index) in getMovie.genres"
                                :key="'MovieDetailPage' + genre + index"
                                class="genre-chip"
                                :color="chip_colors[index % chip_colors.length]"
                            >
                                {{ genre }}
                            </v-chip>
                        </div>
                    </v-row>
                    <v-row>
                        <div class="label-wrapper">
                            <span class="label">
                                release date
                            </span>
                            <span class="content">
                                {{ getMovie.release_date }}
                            </span>
                        </div>
                    </v-row>
                    <v-row>
                        <div>
                            {{ getMovie.overview }}
                        </div>
                    </v-row>
                </v-col>
            </template>
            <template v-else>
                욥욥
            </template>
        </v-row>
        <v-row>
            영화배우
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
            ]
        };
    },
    computed: {
        ...mapState(['selectedMovie']),
        getMovie() {
            return this.selectedMovie;
        },
        isEmpty() {
            if (this.getMovie && 'id' in this.getMovie) {
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
            this.getMovieById(this.id);
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

.content-wrapper{
    padding: 0px 50px 0px 50px;
    min-height: 90vh;

    .detail-title{
        color: white;
        font-size: 3em;
        font-weight: bold;
    }
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
    }
    span{
        margin-right: 5px;
    }
    .content{
        color: gray;
        font-size: 1.2em;
        font-weight: bold;
        padding-left: 1em;
    }
}

.detail-rating {
    height: 40px;
    margin: 10px;
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 30px;
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
}

.genre-chip{
    margin: 0 5px;
}
</style>
