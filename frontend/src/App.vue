<template>
    <v-app style=" position: relative; background-color: black">
        <v-container
            fluid
            pa-0
        >
            <v-content>
                <Header />
                <router-view />
                <Footer />
                <!-- <MoviePage /> -->
            </v-content>
            <!-- <LoadingPage/> -->
        </v-container>
    </v-app>
</template>

<script>
import $ from 'jquery';
import { createNamespacedHelpers } from 'vuex';
// import LoadingPage from '@/components/pages/LoadingPage.vue';
import Header from '@/components/Header.vue';
// import MoviePage from '@/components/movie/MoviePage.vue';
import Footer from '@/components/Footer.vue';

const { mapState, mapActions, mapMutations } = createNamespacedHelpers('users');

export default {
    components: {
        Header,
        Footer
        // MoviePage
    },
    computed: {
        ...mapState({
            token: (state) => state.token,
            user: (state) => state.user,
            username: (state) => state.user.username
        })
    },
    mounted() {
        this.$log.debug('App.vue Session Token from localStorage', localStorage.getItem('token'));
        this.$log.debug('App.vue Vuex getters getToken', this.token);
        this.setToken(localStorage.getItem('token'));
        if (localStorage.getItem('token')) {
            this.getUserBySession(localStorage.getItem('token'));
        }
        if (this.user) {
            this.logoutflag = true;
        }
    },
    methods: {
        ...mapActions(['logout', 'getUserBySession']),
        ...mapMutations(['setToken']),
        logoutState() {
            this.logout(this.username);
        }
    }
};
</script>
