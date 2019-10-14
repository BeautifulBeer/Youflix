<template>
    <div class="home">
        <LatestMovies />
        <RecommendMovies />
        <GenreMovies />
    </div>
</template>

<script>
// @ is an alias to /src
import LatestMovies from '@/components/movie/LatestMovies.vue';
import RecommendMovies from '@/components/movie/RecommendMovies.vue';
import GenreMovies from '@/components/movie/GenreMovies.vue';

import { mapActions } from 'vuex';

export default {
    name: 'HomePage',
    components: {
        LatestMovies,
        RecommendMovies,
        GenreMovies
    },
    methods: {
        ...mapActions('data', ['getSession', 'getUserBySession']),
        getUser() {
            const token = this.getSession();
            return this.getUserBySession(token);
        }
    }
};
</script>
