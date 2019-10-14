<template>
    <v-container class="pa-2" fluid grid-list-md>
        <v-layout row>
            <v-flex v-for="(card, index) in movieListCardsSliced" :key="index" xs12 md3 sm6 pa-3>
                <MovieListCard
                    :id="card.id"
                    :img="card.img"
                    :title="card.title"
                    :genres="card.genres"
                    :rating="card.rating"
                    :view-cnt="card.viewCnt"
                    :index="index"
                />
            </v-flex>
            <v-pagination v-if="maxPages > 1" v-model="page" :length="maxPages" />
        </v-layout>
    </v-container>
</template>

<script>
import MovieListCard from './MovieListCard.vue';

export default {
    components: {
        MovieListCard,
    },
    props: {
        movieListCards: {
            type: Array,
            default: () => [],
        },
    },
    data: () => ({
        cardsPerPage: 12,
        page: 1,
    }),
    computed: {
        // pagination related variables
        movieListEmpty() {
            return this.movieListCards.length === 0;
        },
        maxPages() {
            return Math.floor((this.movieListCards.length + this.cardsPerPage - 1) / 
            this.cardsPerPage);
        },
        movieListCardsSliced() {
            return this.movieListCards.slice(
                this.cardsPerPage * (this.page - 1),
                this.cardsPerPage * this.page);
        },
    },
};
</script>
