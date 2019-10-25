<template>
    <v-container
        class="pa-2"
        fluid
        grid-list-md
    >
        <v-row style="height: 10vh;" />
        <v-row
            :align="rowAlign"
            :justify="rowAlign"
            class="content-wrapper"
        >
            <template v-if="!movieListEmpty">
                <MovieGridCard
                    v-for="(movie, index) in movieListCardsSliced "
                    :key="'movieSearchPage' + movie.id + index"
                    :movie="movie"
                />
            </template>
            <template v-else>
                <AnimateWhenVisible name="fade">
                    <span class="no-result-text">
                        검색한 결과가 없습니다.
                    </span>
                </AnimateWhenVisible>
            </template>
        </v-row>
        <v-row
            align="center"
            justify="center"
            style="min-height: 70px"
        >
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
            if (this.searchResultMovies && 'result' in this.searchResultMovies) {
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
            if (this.movies && this.movies.length > 0) {
                return this.movies.slice(
                    this.cardsPerPage * (this.page - 1),
                    this.cardsPerPage * this.page
                );
            }
            return [];
        },
        rowAlign() {
            return this.movieListEmpty ? 'center' : 'start';
        }
    },
    mounted() {
        this.getMovieByConditions().then(() => {
            this.$forceUpdate();
        });
        window.addEventListener('resize', () => {
            this.responsiveSlider();
        });
    },
    methods: {
        ...mapActions(['getMovieByConditions']),
        responsiveSlider() {
            const { innerWidth } = window;
            const containerWidth = innerWidth - 50 * 2;
            this.cardsPerPage = parseInt(containerWidth / 355, 10) * 3;
        }
    }
};
</script>

<style lang="scss" scoped>

.content-wrapper{
    padding: 0px 50px 0px 50px;
    min-height: 75vh;
}

.no-result-text{
    font-size: 4em;
    color: white;
}

</style>
