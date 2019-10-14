<template>
    <div>
        <div
            v-if="getlogoutflag"
            style="height: 10vh;"
        />
        <nav id="header">
            <v-row class="wrapper">
                <v-col
                    cols="1"
                    class="wrapper"
                >
                    <v-row
                        justify="start"
                        style="height: 100%;"
                    >
                        <v-col
                            cols="12"
                            class="wrapper"
                        >
                            <v-btn
                                text
                                :to="getlogoutflag ? '/home' : '/'"
                                class="btn-link"
                                style="height: 100%;"
                            >
                                <span
                                    style="line-height: 10vh"
                                    class="log-font"
                                >
                                    YOUFLEX
                                </span>
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col
                    v-if="getlogoutflag"
                    cols="11"
                    class="wrapper"
                >
                    <v-row
                        align="center"
                        justify="end"
                        class="wrapper"
                    >
                        <v-col cols="4">
                            <div class="search">
                                <div
                                    id="header-search-effect"
                                    class="search-effect"
                                />
                                <input
                                    id="header-search-input"
                                    v-model="keyword"
                                    type="search"
                                    class="search-box"
                                    placeholder="장르, 영화명, 배우"
                                >
                                <span
                                    class="search-button"
                                    @click="searchKeyword()"
                                >
                                    <span
                                        id="header-search-icon"
                                        class="search-icon"
                                    />
                                </span>
                            </div>
                        </v-col>
                        <v-col cols="1">
                            <div class="dropdown">
                                <v-btn
                                    text
                                >
                                    <span class="menu-font">
                                        {{ getUserName }}
                                        <i class="fa fa-angle-down" />
                                    </span>
                                </v-btn>
                                <div class="dropdown-content">
                                    <router-link to="/myflex">myflex</router-link>
                                    <a href="#">likes</a>
                                    <router-link to="/adminPage">admin</router-link>
                                    <a
                                        href="#"
                                        @click="logoutState()"
                                    >
                                        logout
                                    </a>
                                </div>
                            </div>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </nav>
    </div>
</template>

<script>
import $ from 'jquery';
import swal from 'sweetalert';
import { mapActions, mapGetters } from 'vuex';


export default {
    name: 'Header',
    data() {
        return {
            keyword: '',
            effect: null,
            icon: null,
            keyword_input: null,
            mouseOver: false,
            prevOffset: 0
        };
    },
    mounted() {
        window.addEventListener('DOMContentLoaded', function() {
            document.getElementById('header-search-icon').addEventListener('mouseenter', () => {
                this.mouseOver = true;
            });

            document.getElementById('header-search-icon').addEventListener('mouseleave', () => {
                this.mouseOver = false;
            });

            document.getElementById('header-search-input').addEventListener('focusout', () => {
                if (!this.mouseOver) {
                    this.effect.classList.remove('open');
                    this.icon.classList.remove('open');
                    this.keyword_input.value = '';
                }
            });
            if (this.getUser) {
                this.logoutflag = true;
            }
        })
            
        window.addEventListener('scroll', (e) => {
            const header = document.getElementById('header');
            if (parseInt(window.scrollY) < this.prevOffset) {
                header.style.transform = 'translate(0,0)';
                header.style['-webkit-transform'] = 'translate(0,0)';
                header.style['-moz-transform'] = 'translate(0,0)';
                header.style['-ms-transform'] = 'translate(0,0)';
                header.style['-o-transform'] = 'translate(0,0)';
            } else {
                header.style.transform = 'translate(0,-100px)';
                header.style['-webkit-transform'] = 'translate(0,-100px)';
                header.style['-moz-transform'] = 'translate(0,-100px)';
                header.style['-ms-transform'] = 'translate(0,-100px)';
                header.style['-o-transform'] = 'translate(0,-100px)';
            }
            this.prevOffset = window.scrollY;
        });
    },
    methods: {
        ...mapActions('data', ['logout', 'getSession']),
        changeFlag() {
            if (this.getLoginModalOpen === true) {
                this.$store.commit('data/setLoginModalOpen', false);
            } else {
                this.$store.commit('data/setLoginModalOpen', true);
            }
        },
        logoutState() {
            this.getSession().then((ret) => {
                if (ret === true) {
                    this.logout().then(() => {
                        swal({
                            title: 'GoodBye',
                            text: '다음에 또 만나요.',
                            icon: 'info',
                            button: false
                        }).then(() => {
                            window.location = '/';
                        });
                    });
                } else {
                    swal({
                        title: 'Error',
                        text: 'Server Error, 관리자에게 문의하세요.',
                        icon: 'error',
                        button: false
                    }).then(() => {
                        window.location = '/';
                    });
                }
            });
        },
        searchKeyword() {
            this.effect = document.getElementById('header-search-effect');
            this.keyword_input = document.getElementById('header-search-input');
            this.icon = document.getElementById('header-search-icon');
            if (this.effect.classList.contains('open')) {
                // search function trigger
                this.effect.classList.remove('open');
                this.icon.classList.remove('open');
                this.keyword_input.value = '';
            } else {
                this.effect.classList.add('open');
                this.icon.classList.add('open');
                this.keyword_input.focus();
            }
        }
    },
    computed: {
        ...mapGetters({
            getUser: 'data/getUser'
        }),
        getLoginModalOpen() {
            return this.$store.state.data.isLoginModalOpen;
        },
        getUserModalOpen() {
            return this.$store.state.data.user;
        },
        getlogoutflag() {
            return (this.$store.state.data.token !== null);
        },
        getUserName() {
            if (this.$store.state.data.user === undefined || this.$store.state.data.user === null) {
                return 'GUEST';
            }
            return this.$store.state.data.user.username;
        }
    }
};
</script>

<style lang="scss" scoped>

$search-bg-color: transparent;
$icon-color: #e50914;
$transition: all .5s ease;

//variables
$background-purple: #EEEEEE;
$subtle-white: #f9f9f9;
$subtle-grey: #f2f2f2;
$masked-grey: #333;
$blue: #F03861;

$open-sans: 'Open Sans', sans-serif;

#header{
    top: 0;
    left: 0;
    position: fixed;
    width: 100%;
    height: 10vh;
    padding: 0 50px;
    background-position: right bottom;
    z-index: 100;
    color: transparent;
    transition: transform 1s ease, background-position 5s ease;
    -webkit-transition: -webkit-transform 1s ease, background-position 2s;
    transform:translate(0,0);
    -webkit-transform:translate(0,0);
    -moz-transform:translate(0,0);
    -ms-transform:translate(0,0);
    -o-transform:translate(0,0);
    .wrapper{
        padding: 0;
        margin: auto 0;
        height: 100%;
    }
    .menu-font{
        font-size: 1.2em;
        color: white;
        text-transform: uppercase;
    }
    .log-font{
        font-size: 2.5em;
        color: #e50914;
        font-weight: bold;
        letter-spacing: -1px;
        text-shadow: 1px 1px 1px black;
    }

    .search, .search-box, .search-button, .search-icon {
        box-sizing: border-box;
    }
    .search {
        width: 420px;
        height: 40px;
        float: right;
        background-color: $search-bg-color;
        position: relative;
        overflow: hidden;
        transition: $transition;

    }

    .search-box {
        width: 100%;
        height: 100%;
        box-shadow: none;
        border: none;
        background: transparent;
        color: white;
        position: absolute;
        top: 0;
        left: 0;
        padding-left: 10px;
        font-size: 1.2em;
        opacity: 0;
        transition: all 1s ease;
        &:focus {
            outline: none;
            opacity: 1;
        }
    }

    .search-effect{
        position: relative;
        width: 380px;
        height: 100%;
        // background: #221f1f;
        background: transparent;
        transition: $transition;
        z-index: 10;

        &:after {
            content: '';
            display: block;
            width: 3px;
            height: 100%;
            position: absolute;
            right: 0;
            background-color: $icon-color;
            transition: $transition;
        }

        &.open{
            width: 3px;
        }
    }


    .search-button {
        width: 30px;
        height: 30px;
        display: block;
        position: absolute;
        right: 5px;
        top: 0;
        padding-top: 5px;
        cursor: pointer;
    }

    .search-icon {
        width: 25px;
        height: 25px;
        border-radius: 25px;
        border: 3px solid $icon-color;
        display: block;
        position: relative;
        margin-left: 5px;
        transition: $transition;
        &:before {
            content: '';
            width: 3px;
            height: 5px;
            position: absolute;
            right: -2px;
            top: 17px;
            display: block;
            background-color: $icon-color;
            transform: rotate(-45deg);
            transition: $transition;
        }
        &:after {
            content: '';
            width: 3px;
            height: 8px;
            position: absolute;
            right: -5px;
            top: 19px;
            display: block;
            background-color: $icon-color;
            transform: rotate(-45deg);
            transition: $transition;
        }
        &.open {
            width: 30px;
            height: 30px;
            border-radius: 30px;
            &:before {
            transform: rotate(52deg);
            right: 10px;
            top: 10px;
            height: 10px;
            }
            &:after {
            transform: rotate(-230deg);
            right: 10px;
            top: 5px;
            height: 10px;
            }
        }
    }
}

.btn-link:link {
    color: transparent;
}

.dropdown {
    position: relative;
    display: inline-block;
}


.dropdown-content {
    display: none;
    position: absolute;
    background-color: #221f1f;
    min-width: 110px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 20;
    -webkit-animation-name: dropdown-animation;
    -webkit-animation-duration: 1s;
    animation-name: dropdown-animation;
    animation-duration: 1s;
}

@-webkit-keyframes dropdown-animation {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes dropdown-animation {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

.dropdown-content a {
    color: white;
    padding: 10px 16px;
    text-decoration: none;
    display: block;
    font-size: 1em;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.dropdown-content a:hover {
    color: white;
}

.dropdown:hover .dropdown-content{
    display: block;
}

</style>
