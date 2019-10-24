<template>
    <v-container>
        <Loading :loading="loading" />
        <v-row
            justify="center"
            class="evaluate-header text-center"
        >
            <v-col
                cols="12"
                class="view-count"
            >
                152
            </v-col>

            <v-col
                cols="12"
                class="view-count-content"
            >
                오, 정말 많이 보셨네요. 인정합니다! :)
            </v-col>
            <v-col
                cols="7"
                style="width: 50%;"
            >
                <v-progress-linear
                    value="15"
                    color="white"
                />
            </v-col>
        </v-row>

        <v-row
            class="pa-2"
            fluid
            grid-list-md
        >
            <v-row
                align="center"
                justify="start"
                class="content-wrapper"
            >
                <MyTastes
                    v-for="(element, index) in movieList.data"
                    :key="index"
                    :element="element"
                />
            </v-row>
        </v-row>
    </v-container>
</template>

<script>
// import VUEX
import { createNamespacedHelpers } from 'vuex';

// import Component
import MyTastes from '../user/MyTastes.vue';
import Loading from '../base/Loading.vue';

const userMapState = createNamespacedHelpers('users').mapState;
const movieMapActions = createNamespacedHelpers('movies').mapActions;


export default {
    components: {
        MyTastes,
        Loading
    },
    data() {
        return {
            movieList: [],
            loading: true
        };
    },
    computed: {
        ...userMapState(['user'])
    },
    mounted() {
        this.getNeverSeenMovieList(this.user.email).then((ret) => {
            this.movieList = ret;
            this.loading = false;
        });
    },
    methods: {
        ...movieMapActions(['getNeverSeenMovieList']),
        urlMapping(value) {
            return `url(${value}) center / cover no-repeat`;
        }
    }
};
</script>

<style lang="scss" scoped>

* {
    color: white;
}

.evaluate-header {

    margin-top: 50px;
    margin-right: 100px;
    margin-left: 100px;
    margin-bottom: 50px;
}

.view-count {
    font-size: 1.7em;
    font-weight: bold;
}

.view-count-content {
    color: rgba(255, 255, 255, 0.7);
}

.content-wrapper{
    padding: 0px 100px 0px 100px;
    min-height: 75vh;
}

.no-result-text{
    font-size: 4em;
    color: white;
}

</style>
