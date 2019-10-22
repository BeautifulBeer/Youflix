<template>
    <v-container
        class="container-settting"
        fluid
    >
        <v-row>
            <v-col
                style="min-height: 500px; padding: 0px;"
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

        <v-container
            class="container-settting area"
            fluid
        >
            <v-row style="background-color: white;">
                <v-col cols="12">
                    <h1>MyFlix Dash Board</h1>
                    <v-row>
                        <v-col
                            style="min-height: 600px; position: relative;"
                            sm="12"
                            md="6"
                        >
                            <RatingNumberGraph />
                        </v-col>
                        <v-col
                            sm="12"
                            md="6"
                        >
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
                class="rating-section"
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
        ...userMapState(['user'])
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

.container-settting {

    padding: 0px;
}

.area {

    background-color: white;
    padding: 100px;
}

#background-img {

  background: url("../../assets/userDetail.jpg") no-repeat center center;
  height: 100%;
  background-size: cover;
}

.rating-section {

    background-color: white;
    padding: 50px 50px;
    padding-left: 135px;
    padding-right: 135px;
}
</style>
