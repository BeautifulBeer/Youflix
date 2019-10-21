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
                                <h1>MYFLIX</h1>
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
            <v-row style="background-color: white;">
                <v-col cols="12">
                    <h1>My Movie Tastes</h1>
                </v-col>
            </v-row>
            <v-row
                style="background-color: white; padding: 50px;"
                justify="start"
            >
                <MyTastes
                    v-for="(element, index) in ratingList"
                    :key="index"
                    :element="element"
                />
            </v-row>
        </v-container>
    </v-container>
</template>

<script>
// import VUEX
import { createNamespacedHelpers } from 'vuex';

// COMPONENTS
import GenreGraph from './GenresGraph.vue';
import RatingNumberGraph from './RatingNumberGraph.vue';
import MyTastes from './MyTastes.vue';

const userMapState = createNamespacedHelpers('users').mapState;
const userMapActions = createNamespacedHelpers('users').mapActions;
const ratingMapActions = createNamespacedHelpers('ratings').mapActions;

export default {
    name: 'MyFlix',
    components: {
        GenreGraph,
        RatingNumberGraph,
        MyTastes
    },
    data() {
        return {
            ratingList: [],
            username: ''
        };
    },
    computed: {
        ...userMapState(['token', 'user'])
    },
    mounted() {
        if (this.user === null) {
            this.getSession().then(() => {
                this.username = this.user.username;
                this.getRating(this.user.email).then((ret) => {
                    this.setRatingList(ret);
                });
            });
        } else {
            this.getRating(this.user.email).then((ret) => {
                this.username = this.user.username;
                this.setRatingList(ret);
            });
        }
    },
    methods: {
        ...userMapActions(['getUserBySession', 'getSession']),
        ...ratingMapActions(['getRating']),
        setRatingList(list) {
            list.forEach((element) => {
                this.ratingList.push(element);
            });
        }
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
