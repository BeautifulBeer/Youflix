import Vue from 'vue';
import Router from 'vue-router';
import HomePage from './views/HomePage.vue';

// MAIN PAGE
import Start from './views/base/StartPage.vue';
import Login from './views/base/LoginPage.vue';
import Register from './views/base/Register.vue';
import LoginHelp from './views/base/LoginHelp.vue';

// ADMIN PAGE
import AdminPage from './views/admin/AdminPage.vue';
import DashBoard from './components/admin/DashBoard.vue';
import MovieList from './components/admin/MovieList.vue';
import UserList from './components/admin/UserList.vue';

// USER PAGE
import MyFlex from './components/user/MyFlex.vue';
import UserSetting from './components/user/UserSetting.vue';


Vue.use(Router);

export default new Router({
    mode: 'history',
    base: '/',
    routes: [
        {
            path: '*',
            redirect: '/'
        },
        {
            path: '/',
            name: 'start',
            component: Start
        },
        {
            path: '/home',
            name: 'homepage',
            component: HomePage,
            meta: {
                authRequired: true
            }
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: {
                authRequired: false
            }
        },
        {
            path: '/register',
            name: 'register',
            component: Register,
            meta: {
                authRequired: false
            }
        },
        {
            path: '/loginhelp',
            name: 'loginhelp',
            component: LoginHelp,
            meta: {
                authRequired: false
            }
        },
        {
            path: '/myflex',
            name: 'myflex',
            component: MyFlex,
            meta: {
                authRequired: true
            }
        },
        {
            path: '/setting',
            name: 'setting',
            component: UserSetting,
            meta: {
                authRequired: true
            }
        },
        {
            path: '/adminPage',
            name: 'adminPage',
            redirect: '/adminPage/dashboard',
            component: AdminPage,
            children: [

                {
                    path: 'dashboard',
                    name: 'dashboard',
                    component: DashBoard,
                    meta: {
                        authRequired: true
                    }
                },
                {
                    path: 'movielist',
                    name: 'movielist',
                    component: MovieList,
                    meta: {
                        authRequired: true
                    }
                },
                {
                    path: 'userlist',
                    name: 'userlist',
                    component: UserList,
                    meta: {
                        authRequired: true
                    }
                }
            ],
            meta: {
                authRequired: true
            }
        }
    ]
});
