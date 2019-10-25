<!-- 영화 검색 페이지 -->
<template>
    <v-container
        grid-list-md
        text-center
    >
        <v-layout
            justify-center
            wrap
        >
            <!-- 검색 폼 -->
            <v-flex xs6>
                <div class="display-2 pa-10">
                    영화 검색
                </div>
                <MovieSearchForm :submit="searchMovies" />
            </v-flex>
            <!-- 검색 결과 -->
            <v-flex xs12>
                <MovieList :movie-list-cards="movieList" />
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import MovieSearchForm from '../MovieSearchForm';
import MovieList from '../MovieList';

export default {
    components: {
        MovieList,
        MovieSearchForm,
    },
    data: () => ({}),
    computed: {
        ...mapState({
            movieList: (state) => state.movieSearchList
        })
    },
    methods: mapActions(['searchMovies'])
};
</script>
