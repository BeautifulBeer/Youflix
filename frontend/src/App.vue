<template>
    <v-app id="appContainer">
        <v-container
            fluid
            pa-0
        >
            <v-content>
                <Header />
                <keep-alive>
                    <router-view />
                </keep-alive>
                <template v-if="getlogoutflag">
                    <Footer />
                </template>
                <!-- <MoviePage /> -->
            </v-content>
            <!-- <LoadingPage/> -->
        </v-container>
        <Loading />
    </v-app>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';
// import LoadingPage from '@/components/pages/LoadingPage.vue';
import Header from '@/components/Header.vue';
// import MoviePage from '@/components/movie/MoviePage.vue';
import Footer from '@/components/Footer.vue';
import Loading from '@/components/base/Loading.vue';

const { mapState, mapActions, mapMutations } = createNamespacedHelpers('users');

export default {
    components: {
        Header,
        Footer,
        Loading
        // MoviePage
    },
    computed: {
        ...mapState({
            token: (state) => state.token,
            user: (state) => state.user,
            username: (state) => state.user.username
        }),
        getlogoutflag() {
            return (this.token !== null && this.token !== undefined);
        }
    },
    mounted() {
        this.$log.debug('App.vue Session Token from localStorage', localStorage.getItem('token'));
        this.$log.debug('App.vue Vuex getters getToken', this.token);
        this.setToken(localStorage.getItem('token'));
        if (localStorage.getItem('token')) {
            this.getUserBySession(localStorage.getItem('token')).then((ret) => {
                // 로그인 세션 얻기에 실패할 경우
                if (!ret) {
                    localStorage.removeItem('token');
                    this.$router.push('/');
                    this.setUser(null);
                    this.setToken(null);
                }
            });
        }
        if (this.user) {
            this.logoutflag = true;
        }
    },
    methods: {
        ...mapActions(['logout', 'getUserBySession']),
        ...mapMutations(['setToken', 'setUser']),
        logoutState() {
            this.logout(this.username);
        }
    }
};
</script>

<style lang="scss" scoped>
@import "@/style/variables.scss";

#appContainer{
    position: relative;
    background-color: $background-color;
    // overflow-x: hidden;
}

</style>
