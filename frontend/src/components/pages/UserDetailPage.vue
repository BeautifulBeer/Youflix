<template>
    <v-container fluid>
        <v-row justify="center">
            <v-expansion-panels popout>
                <v-expansion-panel
                    v-for="(profile, i) in profileList"
                    :key="i"
                    hide-actions
                >
                    <v-expansion-panel-header>
                        <v-row
                            align="center"
                            class="spacer"
                            no-gutters
                        >
                            <v-col
                                cols="4"
                                sm="2"
                                md="1"
                            >
                                <v-avatar size="36px">
                                    <v-icon
                                        v-if="profile.is_staff"
                                        color="red"
                                    >
                                        mdi-account-box
                                    </v-icon>
                                    <v-icon
                                        v-else
                                        color="blue"
                                    >
                                        mdi-account-box-outline
                                    </v-icon>
                                </v-avatar>
                            </v-col>

                            <v-col
                                class="hidden-xs-only"
                                sm="5"
                                md="3"
                            >
                                <strong v-html="profile.username" />
                            </v-col>

                            <v-col
                                class="text-no-wrap"
                                cols="5"
                                sm="3"
                            >
                                <v-icon v-if="profile.gender == 'M'">
                                    mdi-human-male
                                </v-icon>
                                <v-icon v-else>
                                    mdi-human-female
                                </v-icon>
                            </v-col>

                            <v-col
                                class="hidden-xs-only"
                                sm="5"
                                md="3"
                            >
                                age :
                                <strong v-html="profile.age" />
                            </v-col>
                        </v-row>
                    </v-expansion-panel-header>

                    <v-expansion-panel-content>
                        <v-divider />
                        <strong>OCCUPATION</strong>
                        <v-card-text v-text="profile.occupation" />
                        <strong>Watched MOVIE</strong>

                        <v-card>
                            <v-container fluid>
                                <v-row>
                                    <v-col
                                        v-for="(movie, index) in profile.watched_movie"
                                        :key="index"
                                        cols="4"
                                    >
                                        <v-card
                                            flat
                                            tile
                                        >
                                            <v-img
                                                :src="`https://unsplash.it/400/300?image=${Math.floor(Math.random() * 100) + 1}`"
                                                height="150px"
                                                @click="viewMovie(movie.id)"
                                            />
                                            <v-card-title>{{ movie.title }}</v-card-title>
                                        </v-card>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card>

                        <v-divider />
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-row>
    </v-container>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
    computed: {
        ...mapState({
            profileList: (state) => state.profileList
        })
    },
    mounted() {
        this.getUsers();
    },
    methods: {
        ...mapActions(['getUsers']),

        viewMovie(index) {
            // this.$store.commit("setSelectIndex", index);
            this.$router.push(`/movies/detail/${index}`);
        }
    }
};
</script>
