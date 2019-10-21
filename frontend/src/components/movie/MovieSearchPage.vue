<template>
    <v-container
        class="pa-2"
        fluid
        grid-list-md
    >
        <v-row
            align="center"
            justify="space-around"
            style="padding: 0px 50px 0px 50px;"
        >
            <MovieGridCard
                v-for="(movie, index) in movieListCardsSliced "
                :key="'movieSearchPage' + movie.id + index"
                :movie="movie"
            />
            <v-pagination
                v-if="maxPages > 1"
                v-model="page"
                :length="maxPages"
            />
        </v-row>
    </v-container>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';
import MovieGridCard from './MovieGridCard.vue';

const { mapState, mapActions } = createNamespacedHelpers('movies');

export default {
    components: {
        MovieGridCard
    },
    data: () => ({
        cardsPerPage: 15,
        page: 1
    }),
    computed: {
        ...mapState(['searchResultMovies']),
        // pagination related variables
        movies() {
            if (Object.keys(this.searchResultMovies).length !== 0) {
                return this.searchResultMovies.result;
            }
            return [];
        },
        movieListEmpty() {
            return this.movies.length === 0;
        },
        maxPages() {
            return Math.floor((this.movies.length + this.cardsPerPage - 1)
            / this.cardsPerPage);
        },
        movieListCardsSliced() {
            if (this.movies.length !== 0) {
                return this.movies.slice(
                    this.cardsPerPage * (this.page - 1),
                    this.cardsPerPage * this.page
                );
            }
            return [];
        }
    },
    mounted() {
        this.getMovieByConditions();
    },
    methods: {
        ...mapActions(['getMovieByConditions'])
    }
};
</script>
