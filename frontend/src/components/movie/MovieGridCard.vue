<template>
    <v-hover v-slot:default="{ hover }">
        <v-card
            :elevation="hover ? 8 : 2"
            @click="viewMovie()"
        >
            <v-layout
                align-center
                py-4
                pl-4
            >
                <v-flex text-center>
                    <v-container
                        grid-list-lg
                        pa-0
                    >
                        <v-layout column>
                            <v-list-item>
                                <v-list-item-content>
                                    <v-list-item-title
                                        class="headline"
                                    >
                                        {{ title }}
                                    </v-list-item-title>
                                    <v-list-item-subtitle>{{ genresStr }}</v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>
                            <v-card-text>
                                <v-layout justify-center>
                                    <v-rating
                                        :value="rating"
                                        color="indigo"
                                        background-color="indigo"
                                        half-increments
                                        dense
                                        readonly
                                    />
                                    <div class="grey--text ml-4">
                                        {{ rating.toFixed(1) }}
                                    </div>
                                </v-layout>
                            </v-card-text>
                            <v-card-text>
                                <v-layout justify-center>
                                    <v-icon color="black">
                                        mdi-eye
                                    </v-icon>
                                    <div class="grey--text ml-4">
                                        {{ viewCnt }}
                                    </div>
                                </v-layout>
                            </v-card-text>
                        </v-layout>
                    </v-container>
                </v-flex>
            </v-layout>
        </v-card>
    </v-hover>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapState, mapMutations } = createNamespacedHelpers('users');

export default {
    props: {
        id: {
            type: Number,
            default: 0
        },
        title: {
            type: String,
            default: ''
        },
        genres: {
            type: Array,
            default: () => []
        },
        img: {
            type: String,
            default: ''
        },
        rating: {
            type: Number,
            default: 0.0
        },
        viewCnt: {
            type: Number,
            default: 0
        },
        index: {
            type: Number,
            default: 0
        }
    },
    computed: {
        ...mapState(['selectIndex']),
        genresStr() {
            return this.genres.join(' / ');
        }
    },
    methods: {
        ...mapMutations(['setSelectIndex']),
        viewMovie() {
            this.setSelectIndex(this.index);
            this.$router.push(`/movies/detail/${this.id}`);
        }
    }
};
</script>
