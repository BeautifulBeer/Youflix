<template>
    <v-card class="mx-auto">
        <v-list-item>
            <v-list-item-avatar color="grey" />
            <v-list-item-content>
                <v-list-item-title
                    class="headline"
                    value="movieInfo.title"
                >
                    {{ movieInfo.title }}
                </v-list-item-title>
                <v-list-item-subtitle>Movie ID : {{ movieInfo.id }}</v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>

        <v-img
            src="https://cdn.vuetifyjs.com/images/cards/mountain.jpg"
            height="500"
            width="1000"
        />

        <v-card-text>
            Genre : {{ movieInfo.genres_array }}
            <br>
            View : {{ movieInfo.view_cnt }}
            <br>
            Watched User : {{ movieInfo.watched_user }}
        </v-card-text>

        <v-card-actions>
            <v-btn
                text
                color="deep-red accent-4"
                @click="back()"
            >
                Back
            </v-btn>
            <div class="flex-grow-1" />
            <v-btn icon>
                <v-icon>mdi-heart</v-icon>
            </v-btn>
            <v-btn icon>
                <v-icon>mdi-share-variant</v-icon>
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapMutations, mapState } = createNamespacedHelpers('movies');

export default {
    props: {
        movieId: {
            type: Number,
            default: 0
        }
    },
    data() {
        return {
            movieInfo: {}
        };
    },
    computed: {
        ...mapState({
            movieSearchList: (state) => state.movieSearchList,
            selectIndex: (state) => state.selectIndex
        })
    },
    mounted() {
        this.$store.commit('setViewCount');

        this.movieId = this.$route.params.movieId;

        this.addMovieView();
        this.getMovieInfo();
    },
    methods: {
        ...mapMutations(['setViewCount']),
        back() {
            this.$router.go(-1);
        }
    },
};
</script>
