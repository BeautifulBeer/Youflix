<template>
    <v-card
        elevation="12"
        max-width="100%"
        max-height="100%"
        class="mx-auto"

        style="margin: 50px;"
    >
        <v-system-bar lights-out />
        <v-carousel
            :continuous="false"
            :show-arrows="false"
            hide-delimiter-background
            delimiter-icon="mdi-minus"
            height="700"
            cycle
        >
            <v-carousel-item
                v-for="index in similarMovieList.length > 12 ? 12 : similarMovieList.length"
                :key="index"
                :src="similarMovieList[index].poster_path"
                :value="similarMovieList[index].title"
            />
        </v-carousel>
    </v-card>
</template>

<script>
export default {
    name: 'SimilarMovieList',
    props: {

        similarMovieList: { type: Array },
    },
    methods: {
        reserve() {
            this.loading = true;

            setTimeout(() => (this.loading = false), 2000);
        },
    },
};
</script>
