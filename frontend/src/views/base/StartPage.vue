<template>
    <div class="start-page">
        <div id="start-page-form">
            <div id="logo">
                YOUFLIX
            </div>

            <a class="start-page__sign-up--email">
                <div
                    class="btn-icon"
                    style="margin-top: 5px;"
                >
                    <i class="material-icons">
                        email
                    </i>
                </div>

                <router-link to="/register">
                    <div style="width: 80%; display:inline-block;">
                            <span class="register-text">
                                E-MAIL로 YOUFLIX 가입
                            </span>
                    </div>
                </router-link>
            </a><br>

            <a class="start-page__sign-up--facebook" @click="alert()">
                <div class="btn-icon">
                    <span class="mdi mdi-facebook-box mdi-24px" />
                </div>

                <div style="width: 80%; display:inline-block">
                    <span>
                        Facebook으로 가입
                    </span>
                </div>
            </a><br>

            <a class="start-page__sign-up--google" @click="alert()">
                <div class="btn-icon">
                    <span class="mdi mdi-google-plus mdi-24px" />
                </div>

                <div style="width: 80%; display:inline-block">
                    <span>
                        Google로 가입
                    </span>
                </div>
            </a><br>

            <p class="start-page__dont-worry">
                걱정마세요. 타임라인에 아무것도 올리지 않아요.
            </p>

            <div class="start-page__divider" />

            <p class="start-page__same-account">
                YOUFLIX에 접속해서 이용해보세요.
            </p>

            <router-link to="/login">
                <a class="start-page__sign-up--login">
                    <span style="textDecoration: none; color: white;">
                        LOGIN
                    </span>
                </a>
            </router-link><br>
        </div>
    </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapActions } = createNamespacedHelpers('infos');

export default {
    data() {
        return {
            uid: '',
            password: '',
            modalTitle: '',
            modalContent: ''
        };
    },
    methods: {
        ...mapActions(['commingSoon']),
        alert() {
            this.commingSoon();
        }
    }
};
</script>

<style lang="scss" scoped>

span {

    text-decoration: none;
}

p {
    display: block;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
}

.start-page {
    background: url("/static/img/chernobyl.jpg") no-repeat center center;
    background-size: cover;
    position: relative;
    height: 100vh;
}
.start-page:after {
    content: "";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: #121218;
    opacity: 0.8;
}

#start-page-form {

    position: absolute;
    top: 50%;
    left: 50%;

    -webkit-transform: translate(-50%, -50%);
    -khtml-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    z-index: 100;
    text-align: center;
}

#logo {

    font-size: 7em;
    color: white;
    font-weight: bold;
    letter-spacing: -1px;
    text-shadow: 1px 1px 1px black;
}

.btn {

    border-radius: 40px;
    width: 290px;
    height: 52px;
    line-height: 52px;
}

.button-div {

    margin-bottom: 12px;
}

.start-page__sign-up--email {
    margin-bottom: 12px;
    background-color: rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.3);
    color: rgba(255,255,255,0.8);
    display: inline-block;
    position: relative;
    text-align: center;
    -webkit-border-radius: 40px;
    -khtml-border-radius: 40px;
    -moz-border-radius: 40px;
    -ms-border-radius: 40px;
    -o-border-radius: 40px;
    border-radius: 40px;
    width: 290px;
    height: 52px;
    line-height: 52px;
    font-size: 15px;

    a {
        color: rgba(255,255,255,0.8);
        text-decoration: none;
    }

    &:hover {
        background-color: rgba(255, 255, 255);
        color: black;
        font-weight: bold;
        
        .register-text {
            color: black;
        }
    }
}

.start-page__sign-up--facebook {
    margin-bottom: 11px;
    background-color: #4065b3;
    color: #ffffff;

    display: inline-block;
    position: relative;
    text-align: center;
    vertical-align: middle;
    -webkit-border-radius: 40px;
    -khtml-border-radius: 40px;
    -moz-border-radius: 40px;
    -ms-border-radius: 40px;
    -o-border-radius: 40px;
    border-radius: 40px;
    width: 290px;
    height: 52px;
    line-height: 52px;
    font-size: 15px;
}

.start-page__sign-up--google {
    margin-bottom: 11px;
    background-color: #FF3376;
    color: #ffffff;

    display: inline-block;
    position: relative;
    text-align: center;
    vertical-align: middle;
    -webkit-border-radius: 40px;
    -khtml-border-radius: 40px;
    -moz-border-radius: 40px;
    -ms-border-radius: 40px;
    -o-border-radius: 40px;
    border-radius: 40px;
    width: 290px;
    height: 52px;
    line-height: 52px;
    font-size: 15px;
}

.start-page__sign-up--login {
    margin-bottom: 11px;
    background-color: #E50914;
    color: #ffffff;

    display: inline-block;
    position: relative;
    text-align: center;
    vertical-align: middle;
    -webkit-border-radius: 40px;
    -khtml-border-radius: 40px;
    -moz-border-radius: 40px;
    -ms-border-radius: 40px;
    -o-border-radius: 40px;
    border-radius: 40px;
    width: 290px;
    height: 52px;
    line-height: 52px;
    font-size: 15px;
}

.btn-icon {
    width: 20%;
    text-align: right;
    vertical-align: middle;
    display:inline-block;
}

.start-page__dont-worry {
    padding: 0px;
    margin: 0px;
    font-size: 12px;
    color: #ffffff;
    letter-spacing: -.5px;
    opacity: 0.5;
    filter: alpha(opacity=50);
}

.start-page__same-account {
    font-size: 14px;
    color: #ffffff;
    margin-bottom: 20px;
    letter-spacing: -.5px;
    opacity: 0.6;
    filter: alpha(opacity=60);
}

.start-page__divider {
    display: block;
    width: 260px;
    height: 1px;
    background-color: rgba(154,151,161,0.3);
    margin: 0 auto 20px;
    margin-top: 10px;
}
</style>
