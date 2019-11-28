<template>
    <div class="home">
        <LatestMovies />
        <RecommendMovies :setLoaded="setRecommendLoaded" />
        <GenreMovies :setLoaded="setGenresLoaded" />
        <TasteMovies :setLoaded="setGenresLoaded" />
    </div>
</template>

<script>
import $ from 'jquery';
import { createNamespacedHelpers } from 'vuex';
// @ is an alias to /src
import LatestMovies from '@/components/movie/LatestMovies.vue';
import RecommendMovies from '@/components/movie/RecommendMovies.vue';
import GenreMovies from '@/components/movie/GenreMovies.vue';
import TasteMovies from '@/components/movie/TasteMovies.vue';

const { mapMutations } = createNamespacedHelpers('movies');

export default {
    name: 'HomePage',
    components: {
        LatestMovies,
        RecommendMovies,
        GenreMovies,
        TasteMovies
    },
    data() {
        return {
            recommendLoaded: false,
            genresLoaded: false
        };
    },
    computed: {
        bothLoaded() {
            return this.recommendLoaded && this.genresLoaded;
        }
    },
    watch: {
        // eslint-disable-next-line
        bothLoaded: function(val) {
            this.setIsLoaded(val);
        }
    },
    methods: {
        ...mapMutations(['setIsLoaded']),
        setRecommendLoaded(flag) {
            this.recommendLoaded = flag;
        },
        setGenresLoaded(flag) {
            this.genresLoaded = flag;
        }
    }
};
</script>
