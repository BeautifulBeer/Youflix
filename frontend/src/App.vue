<template>
    <v-app style=" position: relative; background-color: #221f1f">
        <v-container
            fluid
            pa-0
        >
            <v-content>
                <Header />
                <router-view />
                <Footer />
                <MoviePage />
            </v-content>
            <!-- <LoadingPage/> -->
        </v-container>
    </v-app>
</template>

<script>
import $ from 'jquery';
import { mapActions } from 'vuex';
// import LoadingPage from '@/components/pages/LoadingPage.vue';
import Header from '@/components/Header.vue';
import MoviePage from '@/components/movie/MoviePage.vue';
import Footer from '@/components/Footer.vue';

export default {
    components: {
        Header,
        Footer,
        MoviePage
    },
    computed: {

        getlogoutflag() {
            return this.$store.state.data.token !== null;
        }
    },
    mounted() {
        this.$log.debug('App.vue Session Token from localStorage', localStorage.getItem('token'));
        this.$log.debug('App.vue Vuex getters getToken', this.$store.getters.getToken);
        this.$store.commit('data/setToken', localStorage.getItem('token'));
        this.$store.dispatch(
            'data/getUserBySession',
            localStorage.getItem('token'),
        );
        if (this.$store.state.user != null) {
            this.logoutflag = true;
        }
    },
    methods: {
        ...mapActions('data', ['logout']),
        logoutState() {
            this.logout(this.$store.state.data.user.username);
        }
    }
};
</script>
