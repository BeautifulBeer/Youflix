<template>
    <div class="vld-parent">
        <Loading
            loader="dots"
            color="#E50914"
            :active.sync="isLoading"
            :is-full-page="fullPage"
        />
        <v-row class="mb-3">
            <v-col>
                <v-combobox
                    v-model="selectedGenre"
                    style="margin: 15px;"
                    :items="genres"
                    label="SELECT GENRES"
                />
            </v-col>
            <v-col>
                <v-combobox
                    v-model="selectedSorting"
                    style="margin: 15px;"
                    :items="sortingMethods"
                    label="SELECT SORTING"
                />
            </v-col>
        </v-row>
        <v-container
            class="pa-4 text-center"
        >
            <v-row
                class="fill-height"
                align="center"
                justify="center"
            >
                <template
                    v-for="(movie, i) in movieList"
                >
                    <v-col
                        :key="i"
                        cols="12"
                        md="2"
                    >
                        <v-hover v-slot:default="{ hover }">
                            <v-card
                                id="movieCard"
                                :elevation="hover ? 12 : 2"
                                :class="{ 'on-hover': hover }"
                                @click="clickMovie(i)"
                            >
                                <v-img
                                    :src="movie.backdrop_path | staticPath"
                                    height="225px"
                                >
                                    <v-card-title class="title white--text">
                                        <v-row
                                            class="fill-height flex-column"
                                            justify="space-between"
                                        >
                                            <p
                                                class="mt-4 subheading text-left"
                                            >
                                                {{ movie.title }}
                                            </p>
                                            <p
                                                class="caption font-weight-medium font-italic text-left"
                                            >
                                                Average Rating : {{ movie.average_rating }}
                                            </p>
                                        </v-row>
                                    </v-card-title>
                                </v-img>
                            </v-card>
                        </v-hover>
                    </v-col>
                </template>
            </v-row>
            <v-dialog
                v-if="!isLoading"
                v-model="dialog"
                width="700"
            >
                <v-card>
                    <v-card-title
                        v-if="!modifyFlag"
                        id="originTitle"
                        class="display-1 black lighten-2 white--text"
                        primary-title
                    >
                        {{ movieList[clickedIndex].title }}
                    </v-card-title>
                    <div v-else>
                        <v-text-field
                            v-model="movieList[clickedIndex].title"
                            label="Input Title"
                            outlined
                        />
                    </div>

                    <v-img :src="movieList[clickedIndex].poster_path" />

                    <v-card-text
                        v-if="movieList[clickedIndex].video != ''"
                        class="text--primary black text-center white--text"
                    >
                        <iframe
                            width="100%"
                            height="500"
                            :src="movieList[clickedIndex].video"
                            alt="require('/static/img/commingsoon.jpg')"
                        />
                    </v-card-text>

                    <v-card-text
                        v-if="!modifyFlag"
                        id="originOverview"
                        class="text--primary"
                        style="margin: 10px;"
                    >
                        {{ movieList[clickedIndex].overview == "" ? "There is no plot information." : movieList[clickedIndex].overview }}
                    </v-card-text>
                    <v-textarea
                        v-else
                        v-model="movieList[clickedIndex].overview"
                        label="Input Overview"
                        outlined
                    />
                    <v-divider />
                    <v-card-text v-if="!modifyFlag">
                        Genre : {{ movieList[clickedIndex].genres_array }}
                    </v-card-text>
                    <v-combobox
                        v-else
                        v-model="movieList[clickedIndex].genres_array"
                        :items="genres"
                        multiple
                        chips
                    />
                    <v-divider />
                    <v-card-text v-if="!modifyFlag">
                        Runtime : {{ movieList[clickedIndex].runtime }}
                    </v-card-text>
                    <v-text-field
                        v-else
                        v-model="movieList[clickedIndex].runtime"
                        label="Input Runtime"
                        outlined
                    />

                    <v-divider />

                    <div class="text-center mt-12">
                        <v-rating
                            v-model="movieList[clickedIndex].average_rating"
                            color="yellow darken-3"
                            background-color="grey darken-1"
                            empty-icon="$vuetify.icons.ratingFull"
                            half-increments
                            hover
                            readonly
                        />
                        {{ movieList[clickedIndex].average_rating }}
                    </div>
                    <v-card-actions class="text-center">
                        <v-row>
                            <v-col v-if="!modifyFlag">
                                <v-btn
                                    color="error"
                                    text
                                    @click="modifyFlag = true"
                                >
                                    MODIFY
                                </v-btn>
                            </v-col>
                            <v-col v-else>
                                <v-btn
                                    color="error"
                                    text
                                    @click="modifyMovie()"
                                >
                                    SAVE
                                </v-btn>
                            </v-col>
                            <v-col v-if="!modifyFlag">
                                <v-btn
                                    color="primary"
                                    text
                                    @click="dialog = false"
                                >
                                    CLOSE
                                </v-btn>
                            </v-col>
                            <v-col v-else>
                                <v-btn
                                    color="primary"
                                    text
                                    @click="cancel()"
                                >
                                    CANCEL
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <v-row>
                <v-col>
                    <v-btn @click="loadMore()">
                        더보기
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import Loading from 'vue-loading-overlay';
import API from '../../../api/movie/movieApi';

// import loading animations
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
    components: {
        Loading
    },
    filters: {
        staticPath(backdropPath) {
            if (
                backdropPath === 'https://image.tmdb.org/t/p/originalNone'
                || backdropPath === undefined
                || backdropPath === ''
            ) return '/static/img/commingsoon.jpg';
            return backdropPath;
        }
    },
    data: () => ({
        selectedSorting: '평균평점 순',
        selectedGenre: 'Total',
        sortingMethods: ['평균평점 순', '조회 순', '최신 순'],
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
        movieInfo: {
            title: { type: String },
            overview: { type: String },
            genres_array: { type: Array },
            runtime: { type: Number }
        },
        modifyFlag: false,

        fullPage: true,
        isLoading: true,
        page: 1,

        dialog: false,
        clickedIndex: 0,

        movieList: [],
        transparent: 'rgba(255, 255, 255, 0)'
    }),
    watch: {
        modifyFlag() {
            this.movieInfo.title = this.movieList[this.clickedIndex].title;
            this.movieInfo.overview = this.movieList[this.clickedIndex].overview;

            this.movieInfo.genres_array = [];

            this.movieInfo.genres_array = this.movieList[
                this.clickedIndex
            ].genres_array;
            this.movieInfo.runtime = this.movieList[this.clickedIndex].runtime;
        },

        selectedSorting() {
            this.page = 1;
            this.movieList = [];
            this.getAllMovies();
        },

        selectedGenre() {
            this.page = 1;
            this.movieList = [];
            this.getAllMovies();
        }
    },
    mounted() {
        this.getAllMovies();
    },
    methods: {
        async getAllMovies() {
            this.isLoading = true;

            let method;

            if (this.selectedSorting === '평균평점 순') method = 1;
            else if (this.selectedSorting == '조회 순') method = 2;
            else method = 3;

            await API.getAllMovies({
                page: this.page,
                sort: method,
                genres: this.selectedGenre
            }).then((ret) => {
                if (ret.data === undefined || ret.data.length === 0) return;

                if (this.movieList.length !== 0) {
                    this.movieList.push.spread(this.movieList, ret.data);
                } else {
                    this.movieList = ret.data;
                }
                this.isLoading = false;
            });
        },
        clickMovie(index) {
            this.clickedIndex = index;
            this.dialog = !this.dialog;
        },
        loadMore() {
            this.page += 1;
            this.getAllMovies();
        },
        async modifyMovie() {
            const data = {
                id: this.movieList[this.clickedIndex].id,
                title: this.movieList[this.clickedIndex].title,
                overview: this.movieList[this.clickedIndex].overview,
                genres_array: this.movieList[this.clickedIndex].genres_array,
                runtime: this.movieList[this.clickedIndex].runtime
            };
            this.isLoading = true;

            await API.modifyMovie(data).then(() => {
                this.isLoading = false;
                this.modifyFlag = false;
            });
        },
        cancel() {
            this.movieList[this.clickedIndex].title = this.movieInfo.title;
            this.movieList[this.clickedIndex].overview = this.movieInfo.overview;
            this.movieList[
                this.clickedIndex
            ].genres_array = this.movieInfo.genres_array;
            this.movieList[this.clickedIndex].runtime = this.movieInfo.runtime;

            this.modifyFlag = false;
        }
    }
};
</script>

<style scoped>
* {
  font-family: 'Oswald', sans-serif;
}
#movieCard {
  transition: opacity 0.4s ease-in-out;
}

#movieCard:not(.on-hover) {
  opacity: 0.6;
}

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
</style>