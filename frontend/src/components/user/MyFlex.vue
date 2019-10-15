<template>
    <v-container fluid>
        <v-row>
            <v-col
                style="min-height: 600px; margin-top: 65px;"
                cols="12"
            >
                <div id="background-img">
                    <v-container
                        fill-height
                        text-center
                        class="white--text"
                    >
                        <v-layout
                            row
                            wrap
                            align-center
                        >
                            <v-flex>
                                <h1>MYFLEX</h1>
                                <font>Taste Analysis</font>

                                <div>
                                    <v-avatar color="gray">
                                        <v-icon dark>
                                            mdi-account-circle
                                        </v-icon>
                                    </v-avatar>
                                </div>

                                <div>
                                    {{ username }}
                                </div>
                            </v-flex>
                        </v-layout>
                    </v-container>
                </div>
            </v-col>
        </v-row>

        <v-container fluid>
            <v-row style="background-color: white;">
                <v-col cols="12">
                    <v-row>
                        <v-col
                            style="min-height: 600px; position: relative;"
                            cols="12"
                        >
                            <h1>Number of Ratings</h1>

                            <RatingNumberGraph />
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
            <v-row style="background-color: white;">
                <v-col cols="12">
                    <v-row>
                        <v-col
                            style="min-height: 600px; position: relative;"
                            cols="12"
                        >
                            <h1>Rating Distribution</h1>

                            <GenreGraph />
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </v-container>
    </v-container>
</template>

<script>
// import VUEX
import { mapState, mapActions } from 'vuex';
// User API
// import UserAPI from '../../../api/user/userApi';
// Movie API
// import MovieAPI from '../../../api/movie/movieApi';

// COMPONENTS
import GenreGraph from './GenresGraph.vue';
import RatingNumberGraph from './RatingNumberGraph.vue';

export default {
    name: 'MyFlex',
    components: {
        GenreGraph,
        RatingNumberGraph
    },
    data() {
        return {
            username: ''
        };
    },
    computed: {
        ...mapState({
            token: (state) => state.data.token,
            user: (state) => state.data.user
        })
    },
    mounted() {
        if (this.user === null) {
            this.getUserBySession(this.token).then(() => {
                this.username = this.user.username;
            });
        } else {
            this.username = this.user.username;
        }
    },
    methods: {
        ...mapActions('data', ['getUserBySession'])
    }
};
</script>

<style scoped>

#background-img {

  background: url("../../assets/userDetail.jpg") no-repeat center center;
  height: 100%;
  background-size: cover;
}

#content {
  margin-top: 100px;
  padding: 50px;
}

#scroll-area {
  width: 100%;
  height: 300px;
}

#example-content {
  width: 100%;
  height: 2000px;
}

.section {
  margin: 15px;
}
</style>
